#!/usr/bin/env python
#
# https://www.dexterindustries.com/GoPiGo/
# https://github.com/DexterInd/GoPiGo3
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md
#
# This code tests the imu output when GoPiGo3 turns
#
# Results:  When you run this program, the GoPiGo3 should turn 90 degrees to the right, 180 to the left, and then 90 to the right, ending where it started.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time    # import the time library for the sleep function
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
    Carl = True
except:
    Carl = False

import easygopigo3 # import the EasyGoPiGo3 class

try:
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    myconfig.setParameters(egpg)

#    TurnDegrees(90, 150)   # turn 90 degrees to the right, at a wheel speed of 100 degrees per second
    egpg.orbit(90)
    time.sleep(7)
#    TurnDegrees(-180, 150) # turn 180 degrees to the left, at a wheel speed of 100 degrees per second
    egpg.orbit(-180)
    time.sleep(8)
#    TurnDegrees(90, 150)   # turn 90 degrees to the right, at a wheel speed of 100 degrees per second
    egpg.orbit(90)
    time.sleep(3)
#    GPG.reset_all()

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    egpg.stop()
