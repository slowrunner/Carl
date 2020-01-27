#!/usr/bin/env python3
#
# wheellog.py

"""
Documentation:
  Detects wheel movement, logs results at end of movement to wheel.log
  End_time, duration, d_left_enc, d_right_enc, travel, rotation
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

# VARIABLES
motion_state = MOTION_UNKNOWN
strt_l_enc = 0
strt_r_enc = 0
curr_l_enc = 0
curr_r_enc = 0
move_l_enc = 0
move_r_enc = 0
strt_time  = 0
stop_time  = 0
motion_sec  = 0

# METHODS

# create logger
wheelLog = logging.getLogger('wheelLog')
wheelLog.setLevel(logging.INFO)

loghandler = logging.FileHandler('/home/pi/Carl/wheel.log')

logformatter = logging.Formatter('%(asctime)s|[%(filename)s.%(funcName)s]%(message)s',"%Y-%m-%d %H:%M")
loghandler.setFormatter(logformatter)
wheelLog.addHandler(loghandler)


# motionChange(egpg)
#
# reads encoders, returns one of [MOTION_NONE, MOTION_START, MOTION_MOVING, MOTION_STOP, MOTION_UNKNOWN)
#
def motionChange(egpg):
    global motion_state, curr_l_enc, curr_r_enc, strt_l_enc, strt_r_enc, move_l_enc, move_r_enc, strt_time, stop_time, motion_sec
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
    curr_l_enc, curr_r_enc = egpg.read_encoders()
    # print("curr_l_enc: {} cur_r_enc: {}".format(curr_l_enc, curr_r_enc))

    if (motion_state == MOTION_UNKNOWN):
        strt_l_enc == curr_l_enc
        strt_r_enc == curr_r_enc
        if motors_running:
            motion_state = MOTION_MOVING
            start_time = time.time()
        else:
            motion_state = MOTION_NONE
    elif (motion_state == MOTION_NONE):
        if motors_running:
            strt_time = time.time()
            strt_l_enc = curr_l_enc
            strt_r_enc = curr_r_enc
            motion_state = MOTION_MOVING
    elif (motion_state == MOTION_MOVING):
        if (motors_running == 0):
            stop_time = time.time()
            move_l_enc = curr_l_enc - strt_l_enc
            move_r_enc = curr_r_enc - strt_r_enc
            motion_sec = stop_time - strt_time
            motion_state = MOTION_STOP
    elif (motion_state == MOTION_STOP):
        motion_state = MOTION_NONE
    return motion_state

def enc_to_dist_mm(egpg,enc_l,enc_r):
    enc_ave = (enc_l + enc_r) / 2.0
    return egpg.WHEEL_DIAMETER * pi * enc_ave / 360.0

def enc_to_angle_deg(egpg,enc_l,enc_r):
    enc_diff = (enc_l - enc_r) / 2.0
    return egpg.WHEEL_DIAMETER * enc_diff / egpg.WHEEL_BASE_WIDTH


def logMotion(egpg):
    global motion_state, curr_l_enc, curr_r_enc, strt_l_enc, strt_r_enc, move_l_enc, move_r_enc, strt_time, stop_time, motion_sec
    print("motion_state: {} curr enc: ({},{}) strt enc: ({},{}) strt_time: {} motion_sec: {} ".format(motion_state,curr_l_enc,curr_r_enc,strt_l_enc,strt_r_enc,stop_time,motion_sec))

def logMotionStop(egpg):
    global motion_state, curr_l_enc, curr_r_enc, strt_l_enc, strt_r_enc, move_l_enc, move_r_enc, strt_time, stop_time, motion_sec

    travel_mm = enc_to_dist_mm(egpg,move_l_enc,move_r_enc)
    rotate_deg = enc_to_angle_deg(egpg,move_l_enc,move_r_enc)
    strToLog = "travel: {:> 7.1f} rotation: {:> 7.1f} motion: {:> 7.1f} sec".format(travel_mm,rotate_deg,motion_sec)
    print("{} move enc: ({},{}) {} ".format(time.ctime(stop_time),move_l_enc,move_r_enc,strToLog))
    # print(strToLog)
    wheelLog.info(strToLog)

# MAIN

def main():
    global motion_state, curr_l_enc, curr_r_enc, strt_l_enc, strt_r_enc, move_l_enc, move_r_enc, strt_time, stop_time, motion_sec

    # if Carl: wheelLog.info("Started")
    try:
        egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    except:
        strToLog = "Could not instantiate an EasyGoPiGo3"
        print(strToLog)
        if Carl: wheelLog.info(strToLog)
        exit(1)
    if Carl:
        myconfig.setParameters(egpg)
        # tp = tiltpan.TiltPan(egpg)
        # tp.tiltpan_center()
        # tp.off()

    try:

        """
        # Testing
        move_l_enc = 166
        move_r_enc = 164
        motion_sec = 1.1
        logMotionStop(egpg)

        move_l_enc = 312
        move_r_enc = -311
        motion_sec = 1.1
        logMotionStop(egpg)

        move_l_enc = -163
        move_r_enc = -162
        motion_sec = 1.1
        logMotionStop(egpg)
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
    # if Carl: wheelLog.info("Finished")
    time.sleep(1)


if (__name__ == '__main__'):  main()
