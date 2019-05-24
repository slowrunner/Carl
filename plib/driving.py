#!/usr/bin/env python3
#
# driving.py

"""
Documentation:  Driving Methods
  
  translatePos(distance_mm=5.0)

"""

# from __future__ import print_function # use python 3 syntax but make it compatible with python 2
# from __future__ import division       #                           ''

import sys
try:
    sys.path.append('/home/pi/Carl/plib')
    #import speak
    import tiltpan
    #import status
    #import battery
    #import myDistSensor
    import lifeLog
    import myconfig
    Carl = True
except:
    Carl = False
import easygopigo3 # import the GoPiGo3 class
import numpy as np
#import datetime as dt
#import argparse
from time import sleep
import math
# import cv2

# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--file", required=True, help="path to input file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
# args = vars(ap.parse_args())
# print("Started with args:",args)


# constants


# varibles



# TRANSLATE POSITION
#     executes two forward S-turns and then drives back to starting line
def translatePos(egpg=None,dist_mm=5.0,turns_behind_line = False):
    if (abs(dist_mm) > egpg.WHEEL_BASE_WIDTH):
        translatePos(egpg, dist_mm / 2.0, turns_behind_line)
        translatePos(egpg, dist_mm / 2.0, turns_behind_line)
    ORBIT_SPEED = 120
    egpg.set_speed(ORBIT_SPEED)
    cosTheta = (egpg.WHEEL_BASE_WIDTH - abs(dist_mm)) / egpg.WHEEL_BASE_WIDTH
    orbitAngle = math.degrees( math.acos(cosTheta) )
    orbitRadius_cm = egpg.WHEEL_BASE_WIDTH / 20
    egpg.orbit(degrees= np.sign(dist_mm) * orbitAngle, radius_cm=orbitRadius_cm, blocking=True)
    sleep(0.5)
    egpg.orbit(degrees= -np.sign(dist_mm) * orbitAngle, radius_cm=orbitRadius_cm, blocking=True)
    sleep(0.5)
    backup_cm = (egpg.WHEEL_BASE_WIDTH * -math.sin( math.radians(orbitAngle) )) / 10.0
    egpg.drive_cm(dist=backup_cm,blocking=True)

def main():
    if Carl: lifeLog.logger.info("Started")
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    if Carl:
        myconfig.setParameters(egpg)   # configure custom wheel dia and base
        print("centering")
        tiltpan.tiltpan_center()
        print("centered")
        sleep(0.5)
        tiltpan.off()
        print("tiltpan.off() complete")

    try:
        #  loop
        loopSleep = 10 # second
        loopCount = 0
        keepLooping = True
        while keepLooping:
            loopCount += 1
            orbit_in_reverse(egpg, degrees= 45, radius_cm= egpg.WHEEL_BASE_WIDTH/2.0, blocking=True)
            exit(0)

            for dist_10x_mm in range(762, 0, -254):
                dist_mm = dist_10x_mm / 10.0
                print("TranslatePos({:.2f})".format(dist_mm))
                translatePos(egpg,dist_mm)  # to the left
                sleep(5)
                print("TranslatePos({:.2f})".format(-dist_mm))
                translatePos(egpg, -dist_mm)  # to the righ
                sleep(5)
            for dist_100x_mm in range(2540, 0, -635):
                dist_mm = dist_100x_mm / 100.0
                print("TranslatePos({:.2f})".format(dist_mm))
                translatePos(egpg, dist_mm)  # to the left
                sleep(5)
                print("TranslatePos({:.2f})".format(-dist_mm))
                translatePos(egpg, -dist_mm)  # to the righ
                sleep(5)
            keepLooping = False
            sleep(loopSleep)
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: lifeLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
