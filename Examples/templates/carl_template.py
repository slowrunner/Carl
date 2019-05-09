#!/usr/bin/env python3
#
# filename.py

"""
Documentation:

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
# import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", help="path to input file")
ap.add_argument("-n", "--num", type=int, default=5, help="number")
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
        while True:
            loopCount += 1



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
