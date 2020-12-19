#!/usr/bin/env python3

# FILE: easy_steer.py

# AUTHOR: Alan McDonley
'''
# Routine for testing EasyGoPiGo  steer(left_percent,right_percent) method
# Test Variables:
#   left_percent                - change with lNNN command
#   right_percent               - change with rNNN command
#   max_speed (150 DPS)         - change with mNNN command
#   test_duration(3 seconds)    - change with tNN  command
#
#  Operation:  Return starts execution, ctrl-c to stop early, x to exit ? gives help
#              Reports distance along path and effective DPS when stopped
#
'''

from __future__ import print_function
from __future__ import division

import easygopigo3
from math import pi
import time
import sys

egpg = easygopigo3.EasyGoPiGo3(use_mutex = True)


python_version = sys.version_info[0]
print("Python Version:",python_version)

max_speed = 150
left_percent = 50
right_percent = 50
test_duration = 3  # seconds to test steer()

def enc_to_distance_inches(enc):
    return egpg.WHEEL_CIRCUMFERENCE * enc/360.0 * 0.0393701

def do_steer_test():
    try:
        print ("\n===== Steer({}%,{}%) of {} dps for {} seconds ========".format(left_percent,right_percent,max_speed,test_duration))
        egpg.set_speed(max_speed)  # DPS  (degrees per second rotation of wheels)
        encoderStartLeft, encoderStartRight = egpg.read_encoders()
        starttime  = time.time()
        egpg.steer(left_percent,right_percent)
        time.sleep(test_duration)
        egpg.stop()
    except KeyboardInterrupt:
        egpg.stop()
        print(" .. Stopping early")
    finally:
        dist_wall_time = time.time() - starttime
        time.sleep(1)		# to be sure totally stopped
        encoderEndLeft, encoderEndRight = egpg.read_encoders()
        deltaLeft = abs(encoderEndLeft - encoderStartLeft) 
        deltaRight = abs(encoderEndRight - encoderStartRight)
        deltaAve = (deltaLeft + deltaRight)/2.0
        path_dist = enc_to_distance_inches(deltaAve)
        wheelrate = deltaAve/dist_wall_time
        print ("Distance (along path): {:.0f}mm for {:.1f} sec at dps: {:.0f} (inc start/stop effect)\n".format(deltaAve, dist_wall_time, wheelrate))


while True:
    print ("\nsteer({:.0f}%,{:.0f}%) at {} dps for {} seconds?  (Return to execute, ? for help)".format(left_percent,right_percent,max_speed,test_duration))
    if python_version < 3: i = raw_input()
    else: 
        try:
            i = input()
        except KeyboardInterrupt:
            egpg.stop()
            print("Enter x to exit")
            continue
    if len(i) == 0:
        try:
            do_steer_test()
        except KeyboardInterrupt:
            print("\nStopping")
            print("Press x to exit")
            egpg.stop()
    elif i[0] == "l":
        left_percent  = int(i[1:])
        print("New left_percent:{}".format(left_percent))
        continue
    elif i[0] == "r":
        right_percent  = int(i[1:])
        print("New right_percent:{}".format(right_percent))
        continue
    elif i == "?":
        print("return starts executiion with stated values")
        print("then ctrl-c stops robot")
        print("lNNN   set left_percent")
        print("rNNN   set right_percent") 
        print("mNNN   set max speed in dps")
        print("?      print this help")
        print("x      to exit program")
        print("Current left:{} right:{} percent".format(left_percent,right_percent))
        print("Current max_speed: {}".format(max_speed))
        continue
    elif i[0] == "x":
        egpg.stop()
        break
    elif i[0] == "m":
        max_speed = int(float(i[1:]))
        print("New max_speed:{}".format(max_speed))
        egpg.set_speed(max_speed)
        continue
    elif i[0] == "t":
        test_duration = int(float(i[1:]))
        print("New test_duration: {} seconds".format(test_duration))
        continue
    else:
        print("Type ? for help")
        continue



print("Exiting...")
time.sleep(0.5)
