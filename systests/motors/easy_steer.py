#!/usr/bin/env python3

# easy_steer.py
'''
# Routine for testing EasyGoPiGo  steer(left_percent,right_percent) method
# Test Variables:
#   left_percent                - change with lNNN command
#   right_percent               - change with rNNN command
#   max_speed (150 DPS)         - change with mNNN command
#
#  Operation:  Return starts execution, ctrl-c to stop, x to exit ? gives help
#
#
'''

from __future__ import print_function
from __future__ import division

import time
import easygopigo3
import sys
from math import pi
import sys

egpg = easygopigo3.EasyGoPiGo3(use_mutex = True)


python_version = sys.version_info[0]
print("Python Version:",python_version)

max_speed = 150
left_percent = 50.0
right_percent = 50.0

while True:
    print ("\nsteer( {}, {} )?  (? for help)".format(left_percent,right_percent))
    if python_version < 3: i = raw_input()
    else: 
        try:
            i = input()
        except KeyboardInterrupt:
            egpg.stop()
            print("Enter x to exit")
    if len(i) == 0:
        try:
            print ("\n===== Steer( {:.1f}%, {:.1f}% ) of {} dps ========".format(left_percent,right_percent,max_speed))
            egpg.set_speed(max_speed)  # DPS  (degrees per second rotation of wheels)
            egpg.steer(left_percent,right_percent)
            time.sleep(5)
        except KeyboardInterrupt:
            print("\nStopping")
            egpg.stop()
    elif i[0] == "l":
        left_percent  = float(i[1:])
        print("New left_percent:{:.1f}".format(left_percent))
        continue
    elif i[0] == "r":
        right_percent  = float(i[1:])
        print("New right_percent:{:.1f}".format(right_percent))
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
    else:
        print("Type ? for help")
        continue



print("Exiting...")
time.sleep(0.5)
