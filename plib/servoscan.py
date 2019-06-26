#!/usr/bin/env python
############################################################################################
# This example creates LIDAR like map using an ultrasonic sensor and a servo with the GoPiGo
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
try:
  sys.path.append('/home/pi/Carl/plib')
  carl = True
  import runLog
except:
  carl = False
from collections import Counter
import math
from time import sleep
import printmaps

debug = False			# True to print all raw values
REVERSE_AXIS=True		# Need to reverse axis if rotate_servo(0) points right for your configuration



delay=.02			# give servo time to finish moving


#
#   ds_map()	SCAN FOR MAP DATA
#	sector=160		size of scan (centered around center-forward)
#	limit=230		sensor trusted reading limit
#	num_of_readings=18	number of angles to take readings at in sector
#	samples=1		number of readings to take at each angle to improve reading reliability
#
#	returns valid_dist_list,valid_angle_list  (r-theta lists)
#
# Example:
#
# Map:         230 cm
#  ---------------------------
# |             o             |
# |       o  o     o  o       |
# |    o                 o    |
# |  o                     o  |
# |                           |
# |                           |
# |             +             |
#  -------------0------------- 230 cm
# Each '-' is 17.7 cm      Each '|' is 37.5 cm
# Closest Object: 230 cm
# Farthest: 230 cm
# Farthest Valid: 230 cm
#
def ds_map(distance_sensor, servo, sector=160,limit=300,num_of_readings=18,samples=1,rev_axis=False):
	half_sector = int(sector/2)
	incr = half_sector/int(num_of_readings/2)
	ang = 90 - half_sector
        right_angle = 90 + half_sector
	ang_l = [0]*(num_of_readings+1)		# list to hold the angle of each trusted readings
	dist_l = [0]*(num_of_readings+1)	# list to hold the distance (trusted_reading) at each angle
	index=0
	buf=[0]*samples		# buffer to hold sample readings at one angle




	print("\n*** SCANNING {} DEGREE SECTOR ***".format(sector))

	while True:
		if debug:
		    print("\nAngle: {:.1f} deg".format(ang))
		#Move the servo to the next angle
		if not rev_axis:
			servo.rotate_servo(ang)		# DI Servo Package has shaft up, 0 = left
		else:
			servo.rotate_servo(180-ang)	# Shaft down servo configuration 0 = right
		sleep(delay)

		#Take the readings from the Distance sensor for this angle, validate within limit
		for i in range(samples):
			dist=distance_sensor.read()  # in cm
			if dist<limit and dist>=0:
				buf[i]=dist
			else:
				buf[i]=limit

		#Find the sample that is most common among all the samples for this angle
		max=Counter(buf).most_common()
		trusted_reading=-1
		for i in range (len(max)):
			if max[i][0] != limit and max[i][0] != 0:
				trusted_reading=max[i][0]
				break
		if trusted_reading==-1:
			trusted_reading=limit

		if debug:
                        print("Index:{} Angle:{:.1f} deg Distance:{} cm ".format(index,ang,trusted_reading))
			# print index,ang,trusted_reading
		ang_l[index]=ang
		dist_l[index]=trusted_reading
		index+=1

		#Move the servo to the next angle
		if not rev_axis:
			servo.rotate_servo(ang)		# DI Servo Package has shaft up, 0 = left
		else:
			servo.rotate_servo(180-ang)	# Shaft down servo configuration 0 = right
		sleep(delay)
		ang+=incr
		if ang>right_angle:
			break
	return dist_l,ang_l
# END ds_map()


# MAIN
def main():
    #Make Map, GoPiGo move forward if no object within , stops makes a map and again moves forward

    PERSONAL_SPACE = 25  #cm

    # Create an instance egpg of the GoPiGo3 class.
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)    # use_mutex=True for "thread-safety"
    if carl: runLog.logger.info("Starting servoscan.py at {0:0.2f}v".format(egpg.volt()))

    # Create an instance of the Distance Sensor class.
    # I2C1 and I2C2 are the two ports through which sensors can connect to the I2C bus
    # The sensor can be connected to either port to be "on the I2C bus" so no port id is needed
    # The EasyDistanceSensor will return trusted readings out to roughly 230 cm
    #                                    and returns 300 when no obstacle seen

    ds = egpg.init_distance_sensor()
    servo = egpg.init_servo("SERVO1")

    try:
	egpg.stop()
	while True:
		# Scan in front of GoPiGo3
		dist_l,ang_l=ds_map(ds, servo, sector=160,rev_axis=REVERSE_AXIS)
		closest_object = min(dist_l)
		servo.reset_servo()

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
		egpg.drive_cm(dist_to_drive,blocking = True)	# drive 1/3 of the distance to closest object

	# Continue here when object within personal space
	servo.reset_servo()
	sleep(2)
	servo.disable_servo()

    except KeyboardInterrupt:
	print("**** Ctrl-C detected.  Finishing Up ****")
        if carl: runLog.logger.info("Exiting  servoscan.py at {0:0.2f}v".format(egpg.volt()))
	servo.reset_servo()
	sleep(2)
	servo.disable_servo()


if __name__ == "__main__":
	main()
