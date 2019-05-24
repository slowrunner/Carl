#!/usr/bin/env python3
#
# PPOCV/C3/load_display_save.py

"""
Documentation:
  Practical Python and Open CV Chapter 3

  Load an image, display it, save it in different format

"""

# from __future__ import print_function # use python 3 syntax but make it compatible with python 2
# from __future__ import division       #                           ''

import sys
sys.path.append('/home/pi/Carl/plib')
import easygopigo3 # import the GoPiGo3 class
import tiltpan
#import status
#import battery
import numpy as np
import datetime as dt
#import speak
#import myDistSensor
import lifeLog
import argparse
from time import sleep
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image file")
args = vars(ap.parse_args())
print("Started with args:",args)


# constants


# varibles


def main():
    lifeLog.logger.info("Started")
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
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

            image = cv2.imread(args["image"])
            print("width:  {} pixels".format(image.shape[1]))
            print("height: {} pixels".format(image.shape[0]))
            cv2.imshow("Image", image)
            cv2.waitKey(0)
            cv2.imwrite("newimage.jpg", image)



            keepLooping = False
            sleep(loopSleep)
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    lifeLog.logger.info("Finished")
    sleep(1)

if __name__ == "__main__":
	main()





if (__name__ == 'main'):  main()
