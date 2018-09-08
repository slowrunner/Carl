#!/usr/bin/env python
#
# https://www.dexterindustries.com/GoPiGo/
# https://github.com/DexterInd/GoPiGo3
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md
#
# This code is an example for making the GoPiGo3 turn accurately using EasyGoPiGo3 class
#
# Results:  When you run this program, the GoPiGo3 should 
#                     turn 90 degrees to the right, 180 to the left, and then 90 to the right, ending where it started.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time    # import the time library for the sleep function
import easygopigo3 # import the GoPiGo3 class

SPIN_SPEED = 100

egpg = easygopigo3.EasyGoPiGo3() # Create an instance of the EasyGoPiGo3 class. egpg will be the EasyGoPiGo3 object.

def TurnDegrees(degrees, speed):
    # get the starting position of each motor
    StartPositionLeft, StartPositionRight = egpg.read_encoders()

    # Limit the speed
    egpg.set_speed(speed)

    # execute the spin
    egpg.turn_degrees(degrees)
try:
    TurnDegrees(90, SPIN_SPEED)   # turn 90 degrees to the right, at a wheel speed of SPIN_SPEED degrees per second
    time.sleep(7)
    TurnDegrees(-180, SPIN_SPEED) # turn 180 degrees to the left, at a wheel speed of SPIN_SPEED degrees per second
    time.sleep(8)
    TurnDegrees(90, SPIN_SPEED)   # turn 90 degrees to the right, at a wheel speed of SPIN_SPEED degrees per second
    time.sleep(3)
    egpg.stop()

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    egpg.stop()           # stop motors 
    print("Ctrl-C detected - Finishing up")
