#!/usr/bin/env python
############################################################################################
# This example creates LIDAR like map using an ultrasonic sensor and a servo with the GoPiGo
# Uses my plib 
#
# http://www.dexterindustries.com/GoPiGo/
# History
# ------------------------------------------------
# Author     	Date      		Comments
# McDonley                 Sept 18      Update to EasyGoPiGo3, DI TOF Distance Sensor
#					New ScaleFactor based on farthest object, if debug
# Karan		  	13 June 14  	Initial Authoring for GoPiGo with ultrasonic sensor
#
'''
## License
 GoPiGo3 for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
 Copyright (C) 2018  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''
#
############################################################################################
#
# ! Attach DI Distance Sensor (VL53L0X based) to either GoPiGo3 I2C port.
# ! Attach DI Servo Pkg to GoPiGo3 SERVO1 Port.
#   (Alan's version: pan servo to SERVO1 port, set REVERSE_AXIS=True)
############################################################################################

#
from __future__ import print_function
from __future__ import division
#
import easygopigo3

import sys
sys.path.append('/home/pi/Carl/plib')

import lifeLog
from collections import Counter
import math
from time import sleep
import printmaps
import servoscan


debug = False			# True to print all raw values
REVERSE_AXIS=True		# Need to reverse axis if rotate_servo(0) points right for your configuration
PERSONAL_SPACE=10		# Stop when nearest object is within this distance in cm


# Create an instance egpg of the GoPiGo3 class.
egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)    # use_mutex=True for "thread-safety"

# Create an instance of the Distance Sensor class.
# I2C1 and I2C2 are the two ports through which sensors can connect to the I2C bus
# The sensor can be connected to either port to be "on the I2C bus" so no port id is needed
# The EasyDistanceSensor will return trusted readings out to roughly 230 cm
#                                    and returns 300 when no obstacle seen

ds = egpg.init_distance_sensor()
ps = egpg.init_servo("SERVO1")

delay=.02			# give servo time to finish moving



# MAIN
def main():
    lifeLog.logger.info("Starting plibServoScan.py at {0:0.2f}v".format(egpg.volt()))
		#Make Map, GoPiGo move forward if no object within , stops makes a map and again moves forward
    try:
	egpg.stop()
	while True:
		# Scan in front of GoPiGo3
		dist_l,ang_l=servoscan.ds_map(ds,ps,sector=160,rev_axis=REVERSE_AXIS)
		closest_object = min(dist_l)
		ps.reset_servo()

		# Print scan data on terminal
		printmaps.view180(dist_l,ang_l,grid_width=80,units="cm",ignore_over=230)

		# Decide if can move forward
		if (closest_object < PERSONAL_SPACE):	#If any obstacle is closer than desired, stop
			print("\n!!! FREEZE - THERE IS SOMETHING INSIDE MY PERSONAL SPACE !!!\n")
			break
		print("\n*** PAUSING TO ENJOY THE VIEW ***")
		sleep(5)

		# We have clearance to move
		dist_to_drive = (closest_object * 0.3)
		print("\n*** WE HAVE CLEARANCE TO MOVE {:.1f}cm ***".format(dist_to_drive))
		egpg.set_speed(200)  # not so fast to cause rocking when stopping
		egpg.drive_cm(dist_to_drive,blocking = True)	# drive 1/3 of the distance to closest object

	# Continue here when object within personal space
	ps.reset_servo()
	sleep(2)
	ps.disable_servo()

    except KeyboardInterrupt:
	print("**** Ctrl-C detected.  Finishing Up ****")
        lifeLog.logger.info("Exiting  plibServoScan.py at {0:0.2f}v".format(egpg.volt()))

	ps.reset_servo()
	sleep(2)
	ps.disable_servo()


if __name__ == "__main__":
	main()
