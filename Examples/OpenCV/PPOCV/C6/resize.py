#!/usr/bin/env python3
#
# resize.py

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

        # aspect ratio = new width over orig width
        r = 150 / image.shape[1]
        # new dimensions will be (new width, orig_height * aspect ratio)
        dim = (150, int(image.shape[0] * r))

        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        cv2.imshow("Resized Width", resized)

        # aspect ratio = new height over orig height
        r = 50.0 / image.shape[0]
        # new dimesion = adjust width by aspect ratio
        dim = (int(image.shape[1] * r), 50)
        # Adrian says INTER_AREA is best resize interpolation type, lets try cubic
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_CUBIC)
        cv2.imshow("Resized Height w/cubic", resized)


        resized = imutils.resize(image, width = 100)
        cv2.imshow("imutils.resize width", resized)

        resized = imutils.resize(image, height = 50)
        cv2.imshow("imutils.resize height w/area interp", resized)

        resized = imutils.resize(image, width = 120, height = 60)
        cv2.imshow("imutils.resize w120 h60", resized)

        cv2.waitKey(0)
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: lifeLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
