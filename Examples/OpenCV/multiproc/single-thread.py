#!/usr/bin/env python3
#
# single-thread.py

"""
Documentation:


Demonstrate find_lane_in(image) using a single thread with PiCamera

One process captures images and calls find_lane_in(image)
    (nothing is done with the result, unless the write-result-to-timestamped-file line is uncommented)
    (can write-input-frame-to-file if line is uuncommented)

lanes.find_lane_in(image) performs the following:

  1) create a grayscale image copy
  2) blur the grayscale image
  3) apply Canny edge detect to blurred grayscale image
     return edge mask
  4) crop edge mask to triangular region of interest
  5) use Hough transform (binned r,theta normal to len/gap qualifed lines) to find lines
  6) average left and right lane lines down to one left of lane, one right of lane line
  7) create lane lines overlay
  8) combine lane lines overlay over original image
  returns image with lane lines drawn in bottom 40%

  (can uncomment write-edge-detect-image)

Results:  640x480 7-9 fps 35% cpu (desktop meter) compute only, 3 fps with imshow
          320x240 21-26 fps 50% cpu (desktop meter) compute only, 7 fps with imshow
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
    Carl = True
except:
    Carl = False
import easygopigo3 # import the EasyGoPiGo3 class
import numpy as np
import datetime as dt
import argparse
from time import sleep
import os
import cv2
import time
import picamera
from picamera.array import PiRGBArray
import lanes

# ARGUMENT PARSER
ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--file", required=True, help="path to input file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
ap.add_argument("-v", "--visual", default=False, action='store_true', help="optional show video result")
args = vars(ap.parse_args())
# print("Started with args:",args)
# filename = args['file']
showVisual = args['visual']

# CONSTANTS
HRES = 320
VRES = 240
# HRES = 640
# VRES = 480
FRAMERATE = 30
WARMUPSLEEP = 5

# VARIABLES


# METHODS


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

    dtstart = None

    try:
        # Do Somthing in a Loop
        loopCount = 0

        # init the camera
        print("PiCamera Started and Stabilizing")
        camera = picamera.PiCamera()
        camera.resolution = (HRES, VRES)
        camera.framerate = FRAMERATE
        # allow camera to warmup
        time.sleep(WARMUPSLEEP)

        # PiRGBArray allows read frames from camera in NumPy format, compat with OpenCV
        rawCapture = PiRGBArray(camera, size=(HRES, VRES))

        dtStart = dt.datetime.now()
        print("Capturing Frames")
        # capture frames from the camera
        # use_video_port = True tells to treat the stream as video
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

            loopCount += 1
            # grab the raw NumPy array image
            # array is 3-dim (width, height, numChannels)
            image = rawCapture.array

            #strTime = dt.datetime.now().strftime('%H:%M:%S.%f')[:-3]
            #print('%s Processing %dx%d frame, loop %d' % (
            #    strTime, frame.shape[0], frame.shape[1], loopCount))

            #cv2.imwrite("st_carls_lane-{}.jpg".format(strTime), frame)
            combo_image = lanes.find_lane_in(image)
            #cv2.imwrite("result-{}.jpg".format(strTime),combo_image)

            if showVisual:
                cv2.imshow("image",combo_image)
                if cv2.waitKey(1) == ord("q"):
                    cv2.destroyAllWindows()
                    break

            # clear the stream in prep for next frame
            rawCapture.truncate(0)


        # Do Something Once


    #except PiCameraValueError:   # expected error when interrupt the capture_continuous
    except picamera.PiCameraError:   # expected error when interrupt the capture_continuous
        print("\nStopping capture_continuous")

    except KeyboardInterrupt:
        print("\n*** Ctrl-C detected - Finishing up")
        camera.close()
        time.sleep(1)
    finally:
        dtEnd = dt.datetime.now()
        captureDuration = (dtEnd - dtStart).total_seconds()
        fps = loopCount/captureDuration
        print("Captured {} {}x{} frames in {:.1f} seconds - Average FPS: {:.1f}".format(loopCount, HRES, VRES, captureDuration, fps))





    if Carl: runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
