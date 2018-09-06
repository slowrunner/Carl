#!/usr/bin/env python
############################################################################################
# This example creates LIDAR like map using an ultrasonic sensor and a servo with the GoPiGo
#
# http://www.dexterindustries.com/GoPiGo/
# History
# ------------------------------------------------
# Author     	Date      		Comments
# McDonley               5 Sept 18      Update to EasyGoPiGo3, DI TOF Distance Sensor
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
# ! Attach DI Distance Sensor (VL53L0X based) to either I2C port.
# ! Attach DI Servo Package to GoPiGo3 SERVO1 Port.
#
############################################################################################

#
from __future__ import print_function
from __future__ import division
#
import easygopigo3
import sys
from collections import Counter
import math
from time import sleep

debug = False			# True to print all raw values


# Create an instance egpg of the GoPiGo3 class.
egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)    # use_mutex=True for "thread-safety"

# Create an instance of the Distance Sensor class.
# I2C1 and I2C2 are the two ports through which sensors can connect to the I2C bus
# The sensor can be connected to either port to be "on the I2C bus" so no port id is needed
# The EasyDistanceSensor will return trusted readings out to roughly 230 cm
#                                    and returns 300 when no obstacle seen

distance_sensor = egpg.init_distance_sensor()
servo = egpg.init_servo("SERVO1")

REVERSE_AXIS=False		# May need to set REVERSE_AXIS True for micro servo of tilt/pan assemblies
PERSONAL_SPACE=10		# Stop when nearest object is within this distance in cm
samples=3			# Number of samples for each angle. Suggest 1-5 (more samples, more trust, more time)
num_of_readings=45		# Number of trusted readings to use
incr=180/num_of_readings	# increment of angle in servo
ang_l=[0]*(num_of_readings+1)	# list to hold the angle of each trusted readings
dist_l=[0]*(num_of_readings+1)	# list to hold the distance (trusted_reading) at each angle
x=[0]*(num_of_readings+1)	# list to hold the x coordinate of each point
y=[0]*(num_of_readings+1)	# list to hold the y coordinate of each point
lim=230				# trust limit of distance sensor in cm (sample over lim set to lim))
delay=.02			# give servo time to finish moving


#
# Scan for map data
#
def ds_map():

	ang=0
	index=0
	buf=[0]*samples		# buffer to hold sample readings at one angle




	print("\n*** SCANNING ***")

	while True:
		if debug:
		    print("\nAngle: {} deg".format(ang))

		#Take the readings from the Distance sensor for this angle, validate within limit
		for i in range(samples):
			dist=distance_sensor.read()  # in cm
			if dist<lim and dist>=0:
				buf[i]=dist
			else:
				buf[i]=lim

		#Find the sample that is most common among all the samples for this angle
		max=Counter(buf).most_common()
		trusted_reading=-1
		for i in range (len(max)):
			if max[i][0] <> lim and max[i][0] <> 0:
				trusted_reading=max[i][0]
				break
		if trusted_reading==-1:
			trusted_reading=lim

		if debug:
                        print("Index:{} Angle:{} deg Distance:{} cm ".format(index,ang,trusted_reading))
			# print index,ang,trusted_reading
		ang_l[index]=ang
		dist_l[index]=trusted_reading
		index+=1

		#Move the servo to the next angle
		if not REVERSE_AXIS:
			servo.rotate_servo(ang)		# DI Servo Package has shaft up, 0 = left
		else:
			servo.rotate_servo(180-ang)	# Shaft down servo configuration 0 = right
		sleep(delay)
		ang+=incr
		if ang>180:
			break
	closest_obj=min(dist_l)
	return closest_obj
# END ds_map()

#
# Print map data
#
def print_map():
	#Print the values in a grid of 51x51 on the terminal
	grid_size=51
        SCALE_FACTOR=math.ceil(max(dist_l)*2/(grid_size-1))
        if debug: print("Farthest object:{} SCALE_FACTOR:{}".format(max(dist_l),SCALE_FACTOR))
	#Convert the distance and angle to (x,y) coordinates and scale it down
	if debug:  print("Scaled Cartesian Data")
	for i in range(num_of_readings+1):
		x[i]=(int(dist_l[i]*math.cos(math.pi*(ang_l[i])/180))/SCALE_FACTOR)
		y[i]=int(dist_l[i]*math.sin(math.pi*ang_l[i]/180))/SCALE_FACTOR
		if debug:
		   print("x[{}] y[{}]=[{} {}]".format(i,i,x[i],y[i]))

	#Rotate the readings so that it is printed in the correct manner
	if debug:  print("Rotated for printing")
	for i in range(num_of_readings+1):
		x[i]=(grid_size/2)-x[i]
		y[i]=(grid_size/2)-y[i]
		if debug:
		   print("x[{}] y[{}]=[{} {}]".format(i,i,x[i],y[i]))

	#Create a grid
	grid = [[0 for a in xrange(grid_size)] for a in xrange(grid_size)]
	if debug:  print("Put value 1 in grid for each trusted_reading")
	for i in range (num_of_readings+1):
		if dist_l[i]<>lim:
			if debug:
			    print("y[{}]:{} x[{}]:{}".format(i,y[i],i,x[i]))
			grid[int(y[i])][int(x[i])]=1
	fence='-'*(grid_size)
        fence=" "+fence

	#Print the map
	label=("{:.0f} cm".format(int(grid_size/2)*SCALE_FACTOR))
        print("Map:"," "*(int(grid_size/2)-8),label)
	print(fence)
	for i in range(int(grid_size/2)):
                if debug:
                    print("|", end='')
		    for j in range (grid_size):
		        print(grid[i][j], end='')
		    print("|")
		print("|", end='')
		for j in range (grid_size):
			if (j==int(grid_size/2)) and i==(int(grid_size/2)-1):
				print("+", end='')
			elif grid[i][j]==0:
				print(" ", end='')
			else:
				print("o", end='')
		print("|")
	print(fence, label)
	closest_obj=min(dist_l)
        print("Closest Object: {:.0f} cm, Each '-' is {:.0f} cm".format(closest_obj,SCALE_FACTOR))
	return closest_obj	#Return the closest distance in all directions
# END print_map()


# MAIN
try:
	egpg.stop()
	while True:
		#Make Map, GoPiGo move forward if no object within , stops makes a map and again moves forward
		closest_object=ds_map()
		servo.reset_servo()
		print_map()
		if (closest_object < PERSONAL_SPACE):	#If any obstacle is closer than desired, stop
			print("\n!!! FREEZE - THERE IS SOMETHING INSIDE MY PERSONAL SPACE !!!\n")
			break
		print("\n*** PAUSING TO ENJOY THE VIEW ***")
		sleep(5)
		# We have clearance to move
		dist_to_drive = (closest_object * 0.3)
		print("\n*** WE HAVE CLEARANCE TO MOVE {:.1f}cm ***".format(dist_to_drive))
		egpg.drive_cm(dist_to_drive,blocking = True)	# drive 1/3 of the distance to closest object

	servo.reset_servo()
	sleep(2)
	servo.disable_servo()

except KeyboardInterrupt:
	print("**** Ctrl-C detected.  Finishing Up ****")
	servo.reset_servo()
	sleep(2)
	servo.disable_servo()
