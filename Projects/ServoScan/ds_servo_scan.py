#!/usr/bin/env python
############################################################################################                                                                
# This example creates LIDAR like map using an ultrasonic sensor and a servo with the GoPiGo
#                                
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     	Date      		Comments
# McDonley               5 Sept 18      Update to EasyGoPiGo3 with TOF Distance Sensor
# Karan		  	13 June 14  	Initial Authoring           
#                                       
'''
## License
 GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
 Copyright (C) 2017  Dexter Industries

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
# ! Attach DI Distance Sensor (VL53L0X based) to GoPiGo3 SERVO1 Port.
#
############################################################################################
import easygopigo3
import sys
from collections import Counter
import math

#
from __future__ import print_function
from __future__ import division


# Create an instance egpg of the GoPiGo3 class.
egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)    # use_mutex=True for "thread-safety"

# Create an instance of the Distance Sensor class.
# I2C1 and I2C2 are the two ports through which sensors can connect to the I2C bus
# The sensor can be connected to either port to be "on the I2C bus" so no port id is needed
# The EasyDistanceSensor will return trusted readings out to roughly 230 cm and returns 300 when no obstacle seen

distance_sensor = egpg.init_distance_sensor()

PERSONAL_SPACE=25			# Stop when nearest object is within this distance in cm

#
# Scan for map data
#
def ds_map():
	delay=.02
	debug = True			# True to print all raw values
	num_of_readings=45		# Number of trusted readings to use 
	incr=180/num_of_readings	# increment of angle in servo
	ang_l=[0]*(num_of_readings+1)	# list to hold the angle of each trusted readings
	dist_l=[0]*(num_of_readings+1)	# list to hold the distance (trusted_reading) at each angle
	x=[0]*(num_of_readings+1)	# list to hold the x coordinate of each point
	y=[0]*(num_of_readings+1)	# list to hold the y coordinate of each point

	ang=0
	lim=230			# trust limit of distance sensor in cm (any sample over this which be set to the limit value)
	index=0
	samples=5		# Number of samples for each angle (more samples yields more trust, but takes more time)
	buf=[0]*samples		# buffer to hold sample readings at one angle




	print "*** SCANNING ***"
	
	while True:
		#Take the readings from the Ultrasonic sensor and process them to get the correct values
		for i in range(samples):
			dist=ds.read_cm()
			if dist<lim and dist>=0:
				buf[i]=dist
			else:
				buf[i]=lim
		
		#Find the sample that is most common among all the samples for a particular angle
		max=Counter(buf).most_common()	
		trusted_reading=-1
		for i in range (len(max)):
			if max[i][0] <> lim and max[i][0] <> 0:
				trusted_reading=max[i][0]
				break
		if trusted_reading==-1:
			trusted_reading=lim
		
		if debug==1:
                        print("Distance Sensor:{} deg {} mm ".format(index,ang,trusted_reading))
			# print index,ang,trusted_reading
		ang_l[index]=ang
		dist_l[index]=trusted_reading
		index+=1

		#Move the servo to the next angle
		servo(ang)	
		time.sleep(delay)
		ang+=incr
		if debug:
		    print("Angle: {} deg".format(ang))
		if ang>180:
			break

# END ds_map()

#
# Print map data
#
def print_map():	
	#Print the values in a grid of 51x51 on the terminal
	grid_size=51
	
	#Convert the distance and angle to (x,y) coordinates and scale it down
	for i in range(num_of_readings+1):	
		x[i]=(int(dist_l[i]*math.cos(math.pi*(ang_l[i])/180))/10)
		y[i]=int(dist_l[i]*math.sin(math.pi*ang_l[i]/180))/10
	
	#Rotate the readings so that it is printed in the correct manner
	for i in range(num_of_readings+1):	
		x[i]=(grid_size/2)-x[i]
		y[i]=(grid_size/2)-y[i]

	#Create a grid
	grid = [[0 for a in xrange(grid_size)] for a in xrange(grid_size)] 
	for i in range (num_of_readings+1):
		if dist_l[i]<>lim:
			grid[y[i]][x[i]]=1	
	fence='-'*(grid_size+1)
	
	#Print the map
	print "Map:"
	print fence*2
	for i in range(grid_size/2):
		print "|",
		for j in range (grid_size):
			if (j==grid_size/2)and i==(grid_size/2)-1:
				print 'x',
			elif grid[i][j]==0:
				print ' ',
			else:
				print 'o',
		print "|"
	print fence*2
	closest_obj=min(dist_l)
        print("Closest Object: {} cm".format(closest_obj))
	return closest_obj	#Return the closest distance in all directions
# END print_map()


# MAIN
try:	
	egpg.stop()
	while True:
		#Make Map, GoPiGo move forward if no object within , stops makes a map and again moves forward
		closest_object=ds_map()
		print_map()
		if (closest_object < PERSONAL_SPACE):	#If any obstacle is closer than desired, stop
			print("!!! FREEZE - THERE IS SOMETHING INSIDE MY PERSONAL SPACE !!!")
			break
		# We have clearance to move
		print("*** WE HAVE CLEARANCE TO MOVE ***") 
		egpg.drive_cm(closest_object * 0.3)	# drive 1/3 of the distance to closest object

		print("*** STOPPING TO ENJOY THE VIEW ***")		
		time.sleep(5)

except KeyboardInterrupt:
	print("**** Ctrl-C detected.  Finishing Up ****")