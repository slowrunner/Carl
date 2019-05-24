#!/usr/bin/env python3
#
# filename.py

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
# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--file", required=True, help="path to input file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
# args = vars(ap.parse_args())
# print("Started with args:",args)


# CONSTANTS


# VARIABLES


# METHODS 



# MAIN

def main():
    if Carl: lifeLog.logger.info("Started")
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    if Carl:
        myconfig.setParameters(egpg)
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
    if Carl: lifeLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
