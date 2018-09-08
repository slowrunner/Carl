#!/usr/bin/env python
#
# driveEndTest.py		TEST HOW STRAIGHT Drive_cm() STOPS
#
#
# Results:  The GoPiGo3 will drive_cm(DRIVE_DIST) repeatedly until cntrl-c is pressed, each time it stops for DRIVE_DISTs, 
#           the GoPiGo3 Motors' position will be printed.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

from time import sleep        # import sleep() from the time library
import easygopigo3            # import the EasyGoPiGo3 class

egpg = easygopigo3.EasyGoPiGo3() # Create an instance of the GoPiGo3 class. egpg will be the GoPiGo3 object.
DRIVE_DIST=20.0

try:
    while True:
	egpg.reset_encoders()
        print("Encoders Before drive_cm(%.1f)   - L: %6d  R: %6d" % (DRIVE_DIST, egpg.read_encoders()[0], egpg.read_encoders()[1]))
	sleep(3)
	egpg.drive_cm(DRIVE_DIST,blocking=True)
        print("Encoders After drive_cm(%.1f)    - L: %6d  R: %6d" % (DRIVE_DIST, egpg.read_encoders()[0], egpg.read_encoders()[1]))
        sleep(3.0)
        print("Encoders 3s after drive_cm(%.1f) - L: %6d  R: %6d" % (DRIVE_DIST, egpg.read_encoders()[0], egpg.read_encoders()[1]))
	sleep(3)

except KeyboardInterrupt:  # quit by Ctrl+C on the keyboard.
    egpg.stop()            # stop the motors
    print("Ctrl-C Detected - Finishing up")
