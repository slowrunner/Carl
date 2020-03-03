#!/usr/bin/env python3
#
# followWall.py

"""
Documentation:
    follow_right_wall(): follows the wall on right side until opening or obstruction

"""

import sys
try:
    sys.path.append('/home/pi/Carl/plib')
    import speak
    import tiltpan
    import status
    import battery
    import myDistSensor
#    import lifeLog
#    import runLog
    import myconfig
    import myimutils   # display(windowname, image, scale_percent=30)
    Carl = True
except:
    Carl = False
import easygopigo3 # import the EasyGoPiGo3 class
# import numpy as np
import datetime as dt
# import argparse
from time import sleep

# import cv2

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
# follow_right_wall(egpg)  returns distance traveled
#
# requires egpg.ds be initialized
# quit_follow = False
# pan to 45 right  - pan(135)
# if distance less than 11 inches, turn left till 11.5, (or 45 degrees)
# if distance more than 12 inches, turn right till 11.5 (or 45 degrees)
# if initial conditions not met, set quit_follow
# get initial encoder readings
# Take initial distance measurement
# loop until distance < 10.5 or quit_follow is true
#   forward at cautious speed
#   Take Distance Measurement
#   If distance > 12 inches or distance < 11 inches: set quit_follow
#   if distance < 11.25 set bias left
#   if distance < 11.75 set bias right
#   if not quit_follow: adjust direction
#   else: stop and return

def follow_right_wall(egpg):



# MAIN

def main():
    # if Carl: runLog.logger.info("Started")
    try:
        egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    except:
        strToLog = "Could not instantiate an EasyGoPiGo3"
        print(strToLog)
        # if Carl: lifeLog.logger.info(strToLog)
        exit(1)
    if Carl:
        myconfig.setParameters(egpg)
        tp = tiltpan.TiltPan(egpg)
        tp.tiltpan_center()
        tp.off()
        egpg.ds = myDistSensor.init(egpg)

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
        follow_right_wall(egpg)

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
