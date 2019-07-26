#!/usr/bin/env python3
#
# threshold.py

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

# ARGUMENT PARSER
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to iaage file")
ap.add_argument("-t", "--threshold", type=int, default=128, help="Threshold value")
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
        # load the image and convert to grayscale
        image = cv2.imread(args["image"])
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # initialize the list of threshold methods
        methods = [
            ("THRESH_BINARY", cv2.THRESH_BINARY),
            ("THRESH_BINARY_INV", cv2.THRESH_BINARY_INV),
            ("THRESH_TRUNC", cv2.THRESH_TRUNC),
            ("THRESH_TOZERO", cv2.THRESH_TOZERO),
            ("THRESH_TOZERO_INV", cv2.THRESH_TOZERO_INV)]

        # loop over the threshold methods
        for (threshName, threshMethod) in methods:
            # threshold the image and show it
            (T, thresh) = cv2.threshold(gray, args["threshold"], 255, threshMethod)
            cv2.imshow(threshName, thresh)
            cv2.waitKey(0)


    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
