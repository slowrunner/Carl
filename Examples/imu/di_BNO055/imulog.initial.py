#!/usr/bin/env python3
#
# imulog.py

"""
Documentation:
  Detects rotation, logs results at end of movement to imu.log
  End_time, duration,start_heading, end_heading, rotation
"""

# from __future__ import print_function # use python 3 syntax but make it compatible with python 2
# from __future__ import division       #                           ''

import sys
import logging

try:
    sys.path.append('/home/pi/Carl/plib')
    # import speak
    # import tiltpan
    # import status
    # import battery
    # import myDistSensor
    # import lifeLog
    # import runLog
    import myconfig
    # import myimutils   # display(windowname, image, scale_percent=30)
    Carl = True
except:
    Carl = False
import easygopigo3 # import the EasyGoPiGo3 class
import numpy as np
import datetime as dt
from math import pi
# import argparse
import time
from my_safe_inertial_measurement_unit import SafeIMUSensor
import myBNO055 as BNO055

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
MOTION_NONE    = 0
MOTION_START   = 1
MOTION_MOVING  = 2
MOTION_STOP    = 3
MOTION_UNKNOWN = 4

# Port must be "AD1" or "AD2" to force software I2C that properly implements clock stretch
IMUPORT = "AD1"


# VARIABLES
motion_state = MOTION_UNKNOWN
strt_heading = 0
curr_heading = 0
delta_heading = 0
strt_time  = 0
stop_time  = 0
motion_sec  = 0
lst_heading = 999
zero_crossed = 0  # + CW  - CCW

# METHODS

# create logger
imuLog = logging.getLogger('imuLog')
imuLog.setLevel(logging.INFO)

loghandler = logging.FileHandler('/home/pi/Carl/imu.log')

logformatter = logging.Formatter('%(asctime)s|[%(filename)s.%(funcName)s]%(message)s',"%Y-%m-%d %H:%M")
loghandler.setFormatter(logformatter)
imuLog.addHandler(loghandler)


# motionChange(egpg)
#
# reads imu, returns one of [MOTION_NONE, MOTION_START, MOTION_MOVING, MOTION_STOP, MOTION_UNKNOWN)
#
def motionChange(egpg):
    global motion_state, curr_heading, strt_heading, delta_heading, lst_heading, zero_crossed, strt_time, stop_time, motion_sec
    global MOTION_NONE, MOTION_START, MOTION_STOP, MOTION_MOVING, MOTION_UNKNOWN

    # list
    #   flags bit 0 -- motors are disabled due to low battery voltage
    #         bit 1 -- motors are not close to target or dps speed control
    #   power -- raw PWM power -100 to 100 percent
    #   encoder position
    #   dps -- speed in degrees per second
    motor_state_l = egpg.get_motor_status(egpg.MOTOR_LEFT)
    # print("motor_state_l: ", motor_state_l)

    motor_state_r = egpg.get_motor_status(egpg.MOTOR_RIGHT)
    # print("motor_state_r: ", motor_state_r)

    # Just before motors start moving, the dps value may be out of permitted range ( e.g. 6267 or -6276 )
    # Motors are not running (yet) - ignore
    if ((abs(motor_state_l[3]) < 1000) and (abs(motor_state_r[3]) < 1000)):
         motors_running = motor_state_l[3] | motor_state_r[3]
    else:
         motors_running = 0
    # print("motors_running: ", motors_running)
    # print("motion_state: ", motion_state)

    # print("left:{} right:{} running:{} state:{}".format(motor_state_l,motor_state_r,motors_running,motion_state))
    curr_heading = egpg.imu.safe_read_euler()[0]
    # print("curr_heading: {}".format(curr_heading))

    if (motion_state == MOTION_UNKNOWN):
        if motors_running:
            strt_time = time.time()
            strt_heading = curr_heading
            lst_heading = curr_heading
            zero_crossed = 0
            motion_state = MOTION_MOVING
        else:
            motion_state = MOTION_NONE
    elif (motion_state == MOTION_NONE):
        if motors_running:
            strt_time = time.time()
            strt_heading = curr_heading
            lst_heading = curr_heading
            zero_crossed = 0
            motion_state = MOTION_MOVING
    elif (motion_state == MOTION_MOVING):
        if (motors_running == 0):
            stop_time = time.time()
            # This is some tricky logic to account for crossing heading of zero, even multiple times
            if zero_crossed == 0:
                # zero not crossed (or crossed and returned)
                delta_heading = curr_heading - strt_heading
            else:
                # zero crossed (CW if positive, CCW if negative)
                # For case start 355 end 5:  1*360  - (355-5) so 360-350 = 10 deg
                # For case start 355 end 5 but also turned full circle getting there:  2*360 - (355-5) so 720-350=360+10=370
                # For case start 5 end 355:  -1*360 - (5-355) so -360+350 = -10 deg
                # For case start 5 end 355 but also turned full circle getting there:  -2*360 - (5-355) so -720+350=-360+ -10=-370
                delta_heading = (zero_crossed * 360.0) - ( strt_heading - curr_heading)
            motion_sec = stop_time - strt_time
            motion_state = MOTION_STOP
        else:  # still moving detect 0 crossing
            if (lst_heading > 350) and (curr_heading < 10):
                zero_crossed += 1
            elif (lst_heading < 10) and (curr_heading > 350):
                zero_crossed -= 1
            lst_heading = curr_heading
    elif (motion_state == MOTION_STOP):
        motion_state = MOTION_NONE
    return motion_state


def logMotion(egpg):
    global motion_state, curr_heading, strt_heading, delta_heading, zero_crossed, strt_time, stop_time, motion_sec
    print("motion_state: {}  HEADINGS  current: {}  start: {} zero_crossed: {} strt_time: {} motion_sec: {} ".format(motion_state,curr_heading,zero_crossed,strt_heading,stop_time,motion_sec))

def logMotionStop(egpg):
    global motion_state, curr_heading, strt_heading, delta_heading, zero_crossed, strt_time, stop_time, motion_sec

    rotate_deg = delta_heading
    strToLog = "heading: {:>7.1f}  rotation: {:> 7.1f} motion: {:> 7.1f} sec errors: {}".format(
                round(curr_heading,1), round(rotate_deg,1), round(motion_sec,1), egpg.imu.getExceptionCount())
    # print("{} {}".format(time.ctime(stop_time),strToLog))
    # print(strToLog)
    imuLog.info(strToLog)

# MAIN

def main():
    global motion_state, curr_heading, strt_heading, delta_heading, zero_crossed, strt_time, stop_time, motion_sec

    # if Carl: imuLog.info("Started")
    try:
        egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    except:
        strToLog = "Could not instantiate an EasyGoPiGo3"
        print(strToLog)
        if Carl: imuLog.info(strToLog)
        exit(1)
    if Carl:
        myconfig.setParameters(egpg)
        egpg.imu = SafeIMUSensor(port = IMUPORT, use_mutex = True, mode=BNO055.OPERATION_MODE_IMUPLUS)
        time.sleep(1.0)  # allow measurements to init
    try:


        # Testing
        # logMotionStop(egpg)

        """
        curr_heading = 5
        delta_heading = 10
        motion_sec = 1.1
        logMotionStop(egpg)

        curr_heading = 0
        delta_heading = 180
        motion_sec = 1.1
        logMotionStop(egpg)
        exit(0)
        """

        # Do Somthing in a Loop
        loopSleep = 0.05 # second (20 times / second)
        loopCount = 0
        keepLooping = True
        while keepLooping:
            loopCount += 1
            # do something
            if (motionChange(egpg) == MOTION_STOP):
                logMotionStop(egpg)
            else:
                # logMotion()
                pass
            time.sleep(loopSleep)

        # Do Something Once


    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            time.sleep(1)
    if (egpg != None): egpg.stop()
    # if Carl: imuLog.info("Finished")
    time.sleep(1)


if (__name__ == '__main__'):  main()
