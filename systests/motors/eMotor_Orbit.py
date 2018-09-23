#!/usr/bin/env python
#
#
# Test new EasyGoPiGo3.orbit() method
#
# Results:  When you run this program, the GoPiGo3 should drive a complete circle about 12 inches in diameter
#				(center of GoPiGo3 is commanded to 30 cm for 11.8 inch orbit)
#

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import math
import easygopigo3 # import the GoPiGo3 class

ORBIT_SPEED = 240
ORBIT_ANGLE = 360
ORBIT_RADIUS = 6    # inches
ORBIT_RAD_CM = int(ORBIT_RADIUS * 2.54)   # 6 inches = 15.24 cm ~ 15 cm = 11.8 inch orbit
MY_WHEEL_DIA = 63.7   # default 66.5mm - empirical value that yields more accurate response

try:
    egpg = easygopigo3.EasyGoPiGo3() # Create an instance of the EasyGoPiGo3 class. egpg will be the EasyGoPiGo3 object.

    # adjust to my GoPiGo3
    egpg.WHEEL_DIAMETER = MY_WHEEL_DIA
    egpg.WHEEL_CIRCUMFERENCE = egpg.WHEEL_DIAMETER * math.pi

    egpg.set_speed(ORBIT_SPEED)

    # execute the spin
    egpg.orbit(degrees=ORBIT_ANGLE, radius_cm=ORBIT_RAD_CM, blocking=True)


except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    egpg.stop()           # stop motors
    print("Ctrl-C detected - Finishing up")
