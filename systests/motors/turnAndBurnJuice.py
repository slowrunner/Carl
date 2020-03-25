#!/usr/bin/env python3
#
# File: turnAndBurnJuice.py  Run Down the Battery
# Results:  When you run this program, the GoPiGo3 should 
#                     turn 90 degrees to the right, 180 to the left, and then 90 to the right, ending where it started.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time    # import the time library for the sleep function
import easygopigo3 # import the GoPiGo3 class
import sys
sys.path.append('/home/pi/Carl/plib')
import myconfig
from datetime import datetime as dt

SPIN_SPEED = 150  # Carl's most accurate
SPIN_SPEED = 500  # Eat a lot of juice

egpg = easygopigo3.EasyGoPiGo3() # Create an instance of the EasyGoPiGo3 class. egpg will be the EasyGoPiGo3 object.
myconfig.setParameters(egpg)

def TurnDegrees(degrees, speed):
    # get the starting position of each motor
    StartPositionLeft, StartPositionRight = egpg.read_encoders()

    # Limit the speed
    egpg.set_speed(speed)

    # execute the spin
    egpg.turn_degrees(degrees)

while (egpg.volt() > 8.3):
    try:
        TurnDegrees(90, SPIN_SPEED)   # turn 90 degrees to the right, at a wheel speed of SPIN_SPEED degrees per second
        time.sleep(1)
        TurnDegrees(-180, SPIN_SPEED) # turn 180 degrees to the left, at a wheel speed of SPIN_SPEED degrees per second
        time.sleep(1)
        TurnDegrees(90, SPIN_SPEED)   # turn 90 degrees to the right, at a wheel speed of SPIN_SPEED degrees per second
        time.sleep(1)
        TurnDegrees(360, SPIN_SPEED)   # turn full spin to the right, at a wheel speed of SPIN_SPEED degrees per second
        time.sleep(1)
        egpg.stop()
        print("{} Battery Voltage: {:.1f}v".format(dt.now().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3], egpg.volt()))

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        egpg.stop()           # stop motors 
        print("Ctrl-C detected - Finishing up")
        break

print("Resetting Carl's parameters from config")
myconfig.setParameters(egpg)
time.sleep(1)
print("Done")

