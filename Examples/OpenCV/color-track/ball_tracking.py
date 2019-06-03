#!/usr/bin/env python3
#
# ball_tracking.py

"""
Documentation:

  pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/

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
    import myconfig
    import myimutils   # display(windowname, image, scale_percent=30)
    Carl = True
except:
    Carl = False
import easygopigo3 # import the EasyGoPiGo3 class
import numpy as np
import datetime as dt
import argparse
import time

import cv2
from collections import deque
from imutils.video import VideoStream
import imutils
import picamera
import io

# ARGUMENT PARSER
ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", help="path to video file instead of using camera")
ap.add_argument("-b", "--buffer", type=int, default=4, help="max buffer size")
args = vars(ap.parse_args())
# print("Started with args:",args)


# CONSTANTS

# define the lower and upper boundaries of the "green" ball
# in the HSV color space
# tennis ball
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)


# VARIABLES

# init a list of tracked points
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the ref to the webcam
#if not args.get("video", False):
#    vs = VideoStream(src=0).start()
#else:
#    vs = cv2.VideoCapture(args["video"])

# allow the camera or fideo file to warm up
#time.sleep(2.0)


# METHODS 



# MAIN

def main():

    global pts

    if Carl: lifeLog.logger.info("Started")
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    if Carl:
        myconfig.setParameters(egpg)
        tiltpan.tiltpan_center()
        time.sleep(0.5)
        tiltpan.off()

    try:
        #  loop
        keepLooping = True
        while keepLooping:

            stream = io.BytesIO()


            # capture a frame from camera to the streem
            with picamera.PiCamera() as camera:
                # camera.resolution = (320, 240)
                camera.resolution = (640, 480)
                camera.capture(stream, format='jpeg')

            frame_time = dt.datetime.now().strftime("%H:%M:%S.%f")[:12]

            # convert pic into numpy array
            buff = np.fromstring(stream.getvalue(), dtype=np.uint8)

            # create an OpenCV image
            frame = cv2.imdecode(buff, 1)

            # grab the current frame
            #frame = vs.read()

            # handle the frame from VideoCapture or VideoStream
            #frame = frame[1] if args.get("video", False) else frame

            # if we are viewing a video and did not grab a frame, 
            # then have reached the end of the video
            if frame is None:
                break

            # resize the frame, blure it, and convert it to HSV color space
            frame = imutils.resize(frame, width=600)
            blurred = cv2.GaussianBlur(frame, (11,11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            # construct a mask for the color "green", 
            # then dilate and erode to remove small blobs left in mask
            mask = cv2.inRange(hsv, greenLower, greenUpper)
            #cv2.imshow("mask",mask)
            #cv2.waitKey(0)
            mask = cv2.erode(mask, None, iterations=2)
            #cv2.imshow("mask",mask)
            #cv2.waitKey(0)
            mask = cv2.dilate(mask, None, iterations=2)
            cv2.imshow("mask",mask)
            # cv2.waitKey(0)

            # find contours in the mask and init the current (x, y) center of ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            center = None

            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, 
                # use it to compute minimum enclosing circle and centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # only proceed if the radius meets a minimum size
                if radius > 10:
                    # draw the circle and centroid on the frame,
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)

            # update the points queue
            pts.appendleft(center)

            # loop over the set of tracked points
            for i in range(1, len(pts)):
                # if either the current point or last point are None, ignore
                if pts[i -1] is None or pts[i] is None:
                    continue

                # otherwise, compute thickness of line and draw connecting lines
                thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                cv2.line(frame, pts[i - 1], pts[i], (0,0,255), thickness)

            # show the frame with markup
            cv2.imshow("Frame",frame)
            key = cv2.waitKey(1) & 0xFF

            # if 'q' key is pressed, stop the loop
            if key == ord("q"):
               keepLooping = False
               cv2.destroyAllWindows()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            time.sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: lifeLog.logger.info("Finished")
    time.sleep(1)


if (__name__ == '__main__'):  main()
