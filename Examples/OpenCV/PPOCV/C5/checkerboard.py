#!/usr/bin/env python3
#
# checkerboard.py

"""
Documentation:
    PPOCV C5 - Challenge: create checkerboard of 15 red and 15 black squares with green circle 
        create a black image (canvas to draw on)
        draw red squares
        find center of image
        draw filled ircle
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
import cv2

# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--file", required=True, help="path to input file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
# args = vars(ap.parse_args())
# print("Started with args:",args)


# constants


# varibles


def main():
    if Carl: lifeLog.logger.info("Started")

    # PPOCV START
    canvas = np.zeros((300, 300, 3), dtype = "uint8")    # black canvas image

    green = (0, 255, 0)
    red = (0, 0, 255)

    (centerX, centerY) = (canvas.shape[1] // 2, canvas.shape[0] // 2)    # find center of image


    for y in range(0, 300, 20):
        for x in range(0, 300, 20):
            cv2.rectangle(canvas, (x, y), (x+9, y+9), red, -1)  # filled
            cv2.rectangle(canvas, (x+10,y+10), (x+19,y+19), red, -1)
    radius = 50
    cv2.circle(canvas, (centerX, centerY), radius, green, -1)   # cv2 x,y  numpy y,x
    cv2.imshow("Canvas", canvas)
    cv2.waitKey(0)



    # PPOCV END
    """
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)

    if Carl: 
        tiltpan.tiltpan_center()
        sleep(0.5)
        tiltpan.off()

    try:
        #  loop
        loopSleep = 1 # second
        loopCount = 0
        keepLooping = True
        while keepLooping:
            loopCount += 1



            sleep(loopSleep)
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    """
    if Carl: lifeLog.logger.info("Finished")

    sleep(1)


if (__name__ == '__main__'):  main()
