#!/usr/bin/env python3
#
# bitwise.py

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
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True, help="path to image file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
#args = vars(ap.parse_args())
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
        #image = cv2.imread(args["image"])
        #cv2.imshow("Original", image)

        rectangle = np.zeros((300, 300), dtype = "uint8")
        cv2.rectangle( rectangle, (25,25), (275,275), 255, -1)
        cv2.imshow("Rectangle", rectangle)

        circle = np.zeros((300,300), dtype = "uint8")
        cv2.circle(circle, (150,150), 150, 255, -1)
        cv2.imshow("Circle", circle)

        bitwiseAnd = cv2.bitwise_and(rectangle, circle)
        cv2.imshow("AND", bitwiseAnd)


        bitwiseOr = cv2.bitwise_or(rectangle,circle)
        cv2.imshow("OR", bitwiseOr)

        bitwiseXor = cv2.bitwise_xor(rectangle, circle)
        cv2.imshow("XOR", bitwiseXor)

        bitwiseNot = cv2.bitwise_not(circle)
        cv2.imshow("NOT", bitwiseNot)




        cv2.waitKey(0)
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: lifeLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
