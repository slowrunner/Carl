#!/usr/bin/env python3
#
# findDock.py

"""
Documentation:
   Uses OpenCV on successive images captured by the PyCam to find the recharging dock.
   Algorithm:
   1) Capture an image
   2) Mask for green LED(s) of the dock
   3) Find number and position in the image of green LED(s)
   4) If no LEDs and number of captures < "360 degrees of captures": 
          turn capture width and continue from step 1
      else if no LEDs in 360 degrees: declare "dock not visible (at this location)"
   4) Calculate dock angle relative to heading angle
   5) Estimate dock distance based on vertical LED position in image
   6) Point distance sensor toward dock, take distance reading
   7) Fuse estimate and reading for distance to dock
   6) Point distance sensor fwd and 10" away (for U turn clearance plus 1")
   7) If distance to dock GE 30" turn to face dock, otherwise turn away from dock
   8) While distance sensor reading > 9" (U turn clearance), drive to point 30" from dock
   9) If drove away from dock, turn to face dock
  10) Perform wall_scan() returns distance to wall, angle to wall normal
  11) Calculate turn angle to intersect wall normal from dock at 90 degrees
  12) Calculate distance from current position to dock wall normal
  11) Turn to intersect wall normal from dock at 90 degrees
  12) While distance sensor reading > 9", drive to dock wall normal
  13) Turn to face dock

  Followed by approach_dock(), and then dock()

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
# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--file", required=True, help="path to input file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
# ap.add_argument("-l", "--loop", default=False, action='store_true', help="optional loop mode")
# args = vars(ap.parse_args())
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
    if Carl: runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
