#!/usr/bin/env python3
#
# play_game.py

"""
Documentation:

Carl dialog with himself

I want to play a game.
How about global thermonuclear war?
No, not that one.  Nobody wins that one.
Ok.  Lets play cat and mouse.
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
        tp = tiltpan.TiltPan(egpg)
        tp.tiltpan_center()
        tp.off()

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
        s1 = "I want to play a game."
        s2 = "How about global thermonuclear war?"
        s3 = "No, not that one.  Nobody wins that one."
        s4 = "Ok.  Lets play cat and mouse."

        sleep(5)
        speak.say(s1,anytime=True)
        sleep(1)
        speak.say(s2,anytime=True)
        sleep(1)
        speak.say(s3,anytime=True)
        sleep(3)
        speak.say(s4,anytime=True)


    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
