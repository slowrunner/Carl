#!/usr/bin/env python3
#
# driving.py

"""
Documentation:  Driving Methods

  translateMm(distance_mm=1.0)

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
    import runLog
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



# TRANSLATE Sideways in millimeters
#     executes two forward S-turns and then drives back to starting line
#     1-3mm requires about an inch front clearance and 1.5 inches side clearance
#     1 inch requires about 3 inches front clearance and about 4 inches side clearance
#     3 inches requires about 4.5 inches front clearance and 6 inches side clearance
def translateMm(egpg=None,dist_mm=1.0,debug=False):
    if (abs(dist_mm) > egpg.WHEEL_BASE_WIDTH):
        translateMm(egpg, dist_mm / 2.0)
        translateMm(egpg, dist_mm / 2.0)
    ORBIT_SPEED = 120
    egpg.set_speed(ORBIT_SPEED)
    cosTheta = (egpg.WHEEL_BASE_WIDTH - abs(dist_mm)) / egpg.WHEEL_BASE_WIDTH
    orbitAngle = math.degrees( math.acos(cosTheta) )
    orbitRadius_cm = egpg.WHEEL_BASE_WIDTH / 20
    if debug: print("orbit {:.0f} deg, {:.1f} cm radius".format(orbitAngle, orbitRadius_cm))
    egpg.orbit(degrees= np.sign(dist_mm) * orbitAngle, radius_cm=orbitRadius_cm, blocking=True)
    sleep(0.5)
    egpg.orbit(degrees= -np.sign(dist_mm) * orbitAngle, radius_cm=orbitRadius_cm, blocking=True)
    sleep(0.5)
    backup_cm = (egpg.WHEEL_BASE_WIDTH * -math.sin( math.radians(orbitAngle) )) / 10.0
    if debug: print("backing {:.1f} cm {:.1f} inches".format(backup_cm, backup_cm/2.54))
    egpg.drive_cm(dist=backup_cm,blocking=True)

def main():
    if Carl: runLog.logger.info("Started")
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    if Carl:
        myconfig.setParameters(egpg)   # configure custom wheel dia and base
        tp = tiltpan.TiltPan(egpg)     # init tiltpan
        print("centering")
        tp.tiltpan_center()
        print("centered")
        sleep(0.5)
        tp.off()
        print("tiltpan.off() complete")

    try:
        #  loop
        loopSleep = 10 # second
        loopCount = 0
        keepLooping = True
        while keepLooping:
            loopCount += 1
            # orbit_in_reverse(egpg, degrees= 45, radius_cm= egpg.WHEEL_BASE_WIDTH/2.0, blocking=True)
            # exit(0)

            print("\nTranslate 1 to 4 mm")
            for dist_mm in range(1, 5, 1):  # 1, 2, 3, 4 mm
                print("\nTranslateMm({:.0f}) {:.2f} inches".format(dist_mm, dist_mm/25.4))
                translateMm(egpg, dist_mm,debug = True)  # to the left
                sleep(5)
                print("\nTranslateMm({:.0f}) {:.2f} inches".format(-dist_mm, -dist_mm/25.4))
                translateMm(egpg, -dist_mm)  # to the right
                sleep(5)


            print("\nTranslate 3, 2, 1 inches")
            for dist_10x_mm in range(762, 0, -254):   # 3, 2, 1 inch
                dist_mm = dist_10x_mm / 10.0
                print("\nTranslateMm({:.0f}) {:.0f} inches".format(dist_mm, dist_mm/25.4))
                translateMm(egpg,dist_mm, debug = True)  # to the left
                sleep(5)
                print("\nTranslateMm({:.0f}) {:.0f} inches".format(-dist_mm, -dist_mm/25.4))
                translateMm(egpg, -dist_mm)  # to the right
                sleep(5)

            keepLooping = False
            #sleep(loopSleep)
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
