#!/usr/bin/env python3
#
# blurring.py

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
ap.add_argument("-i", "--image", required=True, help="path to image file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
args = vars(ap.parse_args())
# print("Started with args:",args)


# CONSTANTS


# VARIABLES


# METHODS 



# MAIN

def main():
    if Carl: runLog.logger.info("Started")
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    if Carl:
        myconfig.setParameters(egpg)
        tp = tiltpan.TiltPan(egpg)
        tp.tiltpan_center()
        tp.off()

    try:
        image =cv2.imread(args["image"])
        cv2.imshow("Original", image)
        blurred = np.hstack([
            cv2.blur(image, (3, 3)),
            cv2.blur(image, (5, 5)),
            cv2.blur(image, (7, 7))])
        cv2.imshow("Averaged", blurred)

        blurred2 = np.hstack([
            cv2.GaussianBlur(image, (3, 3), 0),
            cv2.GaussianBlur(image, (5, 5), 0),
            cv2.GaussianBlur(image, (7, 7), 0)])
        cv2.imshow("Gaussian", blurred2)

        blurred3 = np.hstack([
            cv2.medianBlur(image, 3),
            cv2.medianBlur(image, 5),
            cv2.medianBlur(image, 7)])
        cv2.imshow("Median", blurred3)

        blurred4 = np.hstack([
            cv2.bilateralFilter(image, 5, 21, 21),
            cv2.bilateralFilter(image, 7, 31, 31),
            cv2.bilateralFilter(image, 9, 41, 41)])
        cv2.imshow("Bilateral", blurred4)

        cv2.waitKey(0)







    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
