#!/usr/bin/env python3
#
# followLight.py

"""
Documentation:

based on https://botforge.wordpress.com/2016/07/25/torchflashlight-tracker-using-python-and-opencv/
"""

# from __future__ import print_function # use python 3 syntax but make it compatible with python 2
# from __future__ import division       #                           ''

import sys
try:
    sys.path.append('/home/pi/Carl/plib')
    import speak
    import tiltpan
    import status
    import battery
    import myDistSensor
    import lifeLog
    import runLog
    import myconfig
    import myimutils   # display(windowname, image, scale_percent=30)
    import camUtils
    Carl = True
except:
    Carl = False
import easygopigo3 # import the EasyGoPiGo3 class
import numpy as np
import datetime as dt
import argparse
from time import sleep

import cv2
import io
import picamera

# ARGUMENT PARSER
ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--file", required=True, help="path to input file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
ap.add_argument("-v", "--view", default=False, action='store_true', help="view image and mask")
args = vars(ap.parse_args())
# print("Started with args:",args)
# filename = args['file']
viewFlag = args['view']

# CONSTANTS


# VARIABLES


# METHODS
def topMask(image,maskoff_top_percent=50):
    # Desired object will not be in upper portion of image, so mask out small Y values
    mask = np.zeros(image.shape[:2], dtype = "uint8")  # build mask the size of image

    # compute highest Y (smallest value) valid LEDs can appear in an image
    notMaskV = int(maskoff_top_percent/100.0 * image.shape[0])

    # create a notMasked area from notMaskV to bottom of image
    cv2.rectangle(mask, (0,notMaskV), (image.shape[1], image.shape[0]), 255, -1)

    # apply the mask to the image (leaving only the lower portion of the image)
    maskedImage = cv2.bitwise_and(image, image, mask = mask)
    # cv2.imshow("top masked image",maskedImage)
    return maskedImage



# MAIN

def main():
    if Carl: runLog.logger.info("Started")
    try:
        egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    except:
        strToLog = "Could not instantiate an EasyGoPiGo3"
        print(strToLog)
        if Carl: lifeLog.logger.info(strToLog)
        exit(1)
    if Carl:
        myconfig.setParameters(egpg)
        tp = tiltpan.TiltPan(egpg)
        tp.tiltpan_center()
        tp.off()

    try:
        # Do Somthing in a Loop
        loopSleep = 1 # second
        loopCount = 0
        keepLooping = True
        while keepLooping:
            loopCount += 1
            # do something
            stream = io.BytesIO()
            # capture a frame from camera to the streem
            with picamera.PiCamera() as camera:
                # camera.resolution = (320, 240)
                camera.resolution = (640, 480)
                camera.brightness = 70   # default 50
                camera.contrast = 70     # default 0
                camera.sharpness = 75    # default 0
                camera.awb_mode = 'incandescent'
                camera.capture(stream, format='jpeg')

            frame_time = dt.datetime.now().strftime("%H:%M:%S.%f")[:12]


            # convert pic into numpy array
            buff = np.fromstring(stream.getvalue(), dtype=np.uint8)

            # create an OpenCV image
            frame = cv2.imdecode(buff, 1)

            # Fix camera tilt
            tiltfixed = camUtils.fixTiltOCV(frame)

            # get image dimensions
            frameWidth = tiltfixed.shape[1]
            frameHeight = tiltfixed.shape[0]

            # convert to mono and blur
            gray = cv2.cvtColor(tiltfixed, cv2.COLOR_BGR2GRAY)

            # mask off top part of image, leave only light shining on floor
            bottom = topMask(gray,maskoff_top_percent=70)   # floor is bottom 30% approx

            # blur to avoid noise
            blur = cv2.GaussianBlur(bottom, (9,9), 0)

            # identify threshold intensities and locations
            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(blur)

            # print("maxVal:",maxVal)
            # if maxVal < 140:  maxVal = 140  # flashlight circle will be bright

            # threshold the blurred frame accordingly
            hi, threshold = cv2.threshold(blur, maxVal-20, 230, cv2.THRESH_BINARY)

            # find contours in thresholded frame
            edged = cv2.Canny(threshold, 50, 200)     # was 50,150
            edges = edged.copy()

            # resize frame for ease
            cv2.resize(edges, (300,300))


            _ , lightcontours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)



            # find the circle created by the light
            circles = cv2.HoughCircles(threshold, cv2.HOUGH_GRADIENT, 1.0, 20,
                param1=200,                 # high threshold for canny, was 10
                param2=1,                   # accumulator threshold - smaller = more false circles, was 15
                minRadius=5,                # was 20
                maxRadius=100,)             # was 100

            print("{} {} contours, ".format(frame_time, len(lightcontours) ),end="")
            if circles is not None:
                print("circles: {}".format(len(circles)))
                #print("Circle[0]:",circles[0])
            else:
                print("circles: 0")

            # got light?
            if len(lightcontours) > 0 and circles is not None:
                #Find the biggest light
                maxcontour = max(lightcontours, key=cv2.contourArea)
                # make sure it is reasonable size
                if cv2.contourArea(maxcontour) > 100:   # was 2000:
                    (x, final_y), radius = cv2.minEnclosingCircle(maxcontour)
                    cv2.circle(tiltfixed, (int(x), int(final_y)), int(radius), (0, 255, 0), 4)
                    cv2.rectangle(tiltfixed, (int(x) - 5, int(final_y) - 5), (int(x) + 5, int(final_y) + 5), (0, 128, 255), -1)
                    beamXY = (int(x), int(final_y))
                    h_angle = camUtils.hAngle(beamXY[0],frameWidth)  #  hFOV=DEFAULT_H_FOV
                    tp.pan(90+h_angle)
            # display
            if viewFlag:
                cv2.imshow('edges', edges)
                cv2.imshow('frame', tiltfixed)
                cv2.waitKey(1)


            # sleep(loopSleep)

        # Do Something Once


    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
