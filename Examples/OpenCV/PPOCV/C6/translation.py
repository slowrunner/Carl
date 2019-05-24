#!/usr/bin/env python3
#
# translation.py

"""
Documentation:
    PPOCV C6 

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
    Carl = True
except:
    Carl = False
import easygopigo3 # import the GoPiGo3 class
import numpy as np
import datetime as dt
import argparse
from time import sleep

import imutils
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to image file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
args = vars(ap.parse_args())
# print("Started with args:",args)


# constants


# varibles


def main():
    if Carl: lifeLog.logger.info("Started")
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    if Carl: 
        tiltpan.tiltpan_center()
        sleep(0.5)
        tiltpan.off()

    try:
        image = cv2.imread(args["image"])
        cv2.imshow("Original", image)

        M = np.float32([[1, 0, 25], [0, 1, 50]])
        shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
        cv2.imshow("Shifted Down and Right", shifted)

        M = np.float32([[1, 0, -50], [0, 1, -90]])
        shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
        cv2.imshow("Shifted Up and Left", shifted)

        shifted = imutils.translate(image, 0, 100)
        cv2.imshow("imutils.translate() Down 100",shifted)

        cv2.waitKey(0)
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: lifeLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
