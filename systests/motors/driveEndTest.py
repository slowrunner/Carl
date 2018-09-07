#!/usr/bin/env python
#
# driveEndTest.py		TEST HOW STRAIGHT Drive_cm() STOPS
#
#
# Results:  The GoPiGo3 will drive_cm(10) repeatedly until cntrl-c is pressed, each time it stops for 10s, 
#           the GoPiGo3 Motors' position will be printed.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import gopigo3 # import the GoPiGo3 drivers

egpg = gopigo3.GoPiGo3() # Create an instance of the GoPiGo3 class. egpg will be the GoPiGo3 object.

try:
    while True:
	egpg.offset_motor_encoder(egpg.MOTOR_LEFT, egpg.get_motor_encoder(egpg.MOTOR_LEFT))
	egpg.offset_motor_encoder(egpg.MOTOR_RIGHT, egpg.get_motor_encoder(egpg.MOTOR_RIGHT))
        print("Encoders Before drive_cm(10)   - L: %6d  R: %6d" % (egpg.get_motor_encoder(egpg.MOTOR_LEFT), egpg.get_motor_encoder(egpg.MOTOR_RIGHT)))
	time.sleep(3)
	egpg.drive_cm(10.0,blocking=True)
        print("Encoders After drive_cm(10)    - L: %6d  R: %6d" % (egpg.get_motor_encoder(egpg.MOTOR_LEFT), egpg.get_motor_encoder(egpg.MOTOR_RIGHT)))
        time.sleep(3.0)
        print("Encoders 3s after drive_cm(10) - L: %6d  R: %6d" % (egpg.get_motor_encoder(egpg.MOTOR_LEFT), egpg.get_motor_encoder(egpg.MOTOR_RIGHT)))
	time.sleep(3)

except KeyboardInterrupt:  # quit by Ctrl+C on the keyboard.
    egpg.stop()        # stop the motors
    print("Ctrl-C Detected - Finishing up")
