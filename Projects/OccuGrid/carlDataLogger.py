#!/usr/bin/env python3
#
# carlDataLogger.py

"""
Documentation:

    Records Camera at 320x240 at 5 fps to datetime_str/datetime.mp4
    Records l_enc, r_enc, imu_heading, range for each frame
    Quits on Keyboard Interrupt

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
    from my_safe_inertial_measurement_unit import SafeIMUSensor
    from my_easygopigo3 import EasyGoPiGo3
    Carl = True
except:
    Carl = False
# import easygopigo3 # import the EasyGoPiGo3 class
import os
import numpy as np
import datetime as dt
import argparse
from time import sleep

import cv2

# ARGUMENT PARSER
ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--file", required=True, help="path to input file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
# ap.add_argument("-l", "--loop", default=False, action='store_true', help="optional loop mode")
ap.add_argument("-fps", "--fps", type=int, default=5, help="video frames with data capture per second")
args = vars(ap.parse_args())
print("carlDataLogger.py Started with args:",args)
# filename = args['file']
# loopFlag = args['loop']
fps = args['fps']

# CONSTANTS
IMUPORT = "AD1"

# VARIABLES
start_dt = dt.datetime.now()
l_enc = 0
r_enc = 0
imu_heading = 0
fwd_range = 9999
data_f = None



# METHODS

def do_setup():
    global data_f
    timestr = start_dt.strftime("%Y%m%d-%H%M%S")
    print("carlDataLogger started at {}".format(timestr))
    try:
        os.mkdir(timestr, 0o777)
    except OSError:
        print("Could not create {}/".format(timestr))
        exit(1)
    os.chdir(timestr)
    data_f = open("Data.txt", 'w')

def do_teardown():
    global data_f

    # close data file
    data_f.close()
    print("carlDataLogger: Teardown complete")

# MAIN

def main():

    if Carl: runLog.logger.info("Started")
    try:
        egpg = EasyGoPiGo3(use_mutex=True)
    except Exception as e:
        strToLog = "Could not instantiate an EasyGoPiGo3"
        print(strToLog)
        print("Exception:", str(e))
        # if Carl: lifeLog.logger.info(strToLog)
        exit(1)
    if Carl:
        myconfig.setParameters(egpg)
        tp = tiltpan.TiltPan(egpg)
        tp.tiltpan_center()
        tp.off()
        try:
            egpg.imu = SafeIMUSensor(port = IMUPORT, use_mutex=True, init=False)
        except Exception as e:
            strToLog = "Could not instantiate SafeIMUSensor"
            print(strToLog)
            print("Exception:",str(e))
            exit(1)

    do_setup()

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


    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            do_teardown()
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
