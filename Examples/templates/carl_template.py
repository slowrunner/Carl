#!/usr/bin/env python3
#
# filename.py

"""
Documentation:

"""

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
    # import myimutils   # display(windowname, image, scale_percent=30)
    Carl = True
except:
    Carl = False
import easygopigo3 # import the EasyGoPiGo3 class
import numpy as np
import datetime as dt
import argparse
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
docking_approach_dist_in_mm = 444
fine_adjust_drive_in_mm = 10

# VARIABLES


# METHODS 

# 
def do_something(egpg):
    speak.say("Preparing to do something")
    dist_to_something = egpg.ds.read_mm()
    dist_to_something = adjustReadingInMMForError(dist_to_something)
    alert = "Something is {:.0f} centimeters away".format(dist_to_something/10)
    speak.say(alert)
    runLog.entry(alert)
    sleep(2)

# MAIN
@runLog.logRun
def main():
    try:
        egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    except:
        strToLog = "Could not instantiate an EasyGoPiGo3"
        print(strToLog)
        if Carl: runLog.entry(strToLog)
        exit(1)
    if Carl:
        myconfig.setParameters(egpg)       # set speed, wheel base and dia. for best accuracy
        egpg.ds = myDistSensor.init(egpg)  # Add distance sensor to egpg object
        egpg.tp = tiltpan.TiltPan(egpg)    # Add tiltpan to egpg object
        egpg.tp.tiltpan_center()
        egpg.tp.off()

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
        do_something(egpg)

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    sleep(1)


if (__name__ == '__main__'):  main()
