#!/usr/bin/env python3
#
# contour_only.py

"""
Documentation:

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

import cv2
import imutils

# ARGUMENT PARSER
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to iaage file")
# ap.add_argument("-t", "--threshold", type=int, default=128, help="Threshold value")
# ap.add_argument("-l", "--loop", default=False, action='store_true', help="optional loop mode")
args = vars(ap.parse_args())
# print("Started with args:",args)
# filename = args['file']
# loopFlag = args['loop']

# CONSTANTS


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

    try:
        # Do Somthing in a Loop
        loopSleep = 1 # second
        loopCount = 0
        keepLooping = False
        while keepLooping:
            loopCount += 1
            # do something
            sleep(loopSleep)

        # Do Something Once
        # load the image and apply pyramid mean shift filtering
        # to assist the thresholding that follows
        image = cv2.imread(args["image"])
        shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)
        stack = np.hstack([image,shifted])
        cv2.imshow("Image and Shifted", stack)

        # convert the mean shift image to grayscale
        gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
        # apply Otsu thresholding
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        cv2.imshow("Thresh", thresh)

        # find contours in the thresholded image
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        print("[INFO] {} unique contours found".format(len(cnts)))

        # loop over the contours
        for (i, c) in enumerate(cnts):
            # draw the contour
            ((x, y), _) = cv2.minEnclosingCircle(c)
            cv2.putText(image, "#{}".format(i + 1), (int(x) - 10, int(y)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)

        # show the result
        cv2.imshow("shifted, thresholded, contours",image)





        cv2.waitKey(0)

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
