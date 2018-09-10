#!/usr/bin/env python
############################################################################################
# This example creates LIDAR like map using an ultrasonic sensor and a servo with the GoPiGo
#
# http://www.dexterindustries.com/GoPiGo/
# History
# ------------------------------------------------
# Author     	Date      		Comments
# McDonley              10 Sept 18      Update to EasyGoPiGo3, DI TOF Distance Sensor
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
REVERSE_AXIS=False		# Need to reverse axis if rotate_servo(0) points right for your configuration
PERSONAL_SPACE=10		# Stop when nearest object is within this distance in cm


# Create an instance egpg of the GoPiGo3 class.
egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)    # use_mutex=True for "thread-safety"

# Create an instance of the Distance Sensor class.
# I2C1 and I2C2 are the two ports through which sensors can connect to the I2C bus
# The sensor can be connected to either port to be "on the I2C bus" so no port id is needed
# The EasyDistanceSensor will return trusted readings out to roughly 230 cm
#                                    and returns 300 when no obstacle seen

distance_sensor = egpg.init_distance_sensor()
servo = egpg.init_servo("SERVO1")

delay=.02			# give servo time to finish moving


#
#   ds_map()	SCAN FOR MAP DATA
#	sector=180		size of scan (centered around center-forward)
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
def ds_map(sector=180,limit=300,num_of_readings=18,samples=1,rev_axis=False):
	half_sector = int(sector/2)
	incr = half_sector/int(num_of_readings/2)
	ang = 90 - half_sector
        right_angle = 90 + half_sector
	ang_l = [0]*(num_of_readings+1)		# list to hold the angle of each trusted readings
	dist_l = [0]*(num_of_readings+1)	# list to hold the distance (trusted_reading) at each angle
	index=0
	buf=[0]*samples		# buffer to hold sample readings at one angle




	print("\n*** SCANNING ***")

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
			if max[i][0] <> limit and max[i][0] <> 0:
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

#
# view180()      Print a "forward 180 view" with GoPiGo3 at middle of x-axis grid
#                0 deg = left 90 deg center 180 deg right
#		 Scale is adjusted to farthest valid reading
#	Parmaeters:
#		dist_l		# required list of range values  e.g. [20, 30, 20] facing into corner
#		ang_l		# required list of reading angle (0=left) e.g. [0,90,180]
#		grid_width=80	# optional printout chars to fit map into
#		units="cm"	# optional label for range units
#		ignore_over=300 # use to ignore readings beyond valid sensor detection range
#				  or if sensor returns a particular value if nothing detected
#
def view180(dist_l,ang_l,grid_width=80,units="cm",ignore_over=300):
        CHAR_ASPECT_RATIO=2.12
        if debug: print("view180() called with grid_width:",grid_width)
        if not(grid_width % 2): grid_width -=1
        if debug: print("using grid_width:",grid_width)
        index_list_valid_readings = [i for i, x in enumerate(dist_l) if dist_l[i] < ignore_over]
	valid_dist_l = [dist_l[i] for i in index_list_valid_readings]
        valid_ang_l  = [ang_l[i] for i in index_list_valid_readings]
        num_of_readings = len(valid_dist_l)
        x=[0]*(num_of_readings+1)       # list to hold the x coordinate of each point
        y=[0]*(num_of_readings+1)       # list to hold the y coordinate of each point
        grid_height = int( int((grid_width-3)/2) / CHAR_ASPECT_RATIO)
	max_valid = max(valid_dist_l)
        X_SCALE_FACTOR=max_valid/int((grid_width-3)/2)
        Y_SCALE_FACTOR=X_SCALE_FACTOR * CHAR_ASPECT_RATIO
        if debug:
            print("Farthest reading:{} ".format(max(dist_l)),end='')
            print("Farthest_valid:{} ".format(max_valid),end='')
            print("X_SCALE_FACTOR:{} Y_SCALE_FACTOR:{}".format(X_SCALE_FACTOR,Y_SCALE_FACTOR))
            print("grid_width: {} grid_height: {}".format(grid_width,grid_height))
        #Convert the distance and angle to (x,y) coordinates and scale it down
        if debug:  print("Scaled Cartesian Data (0deg=left)")
        for i in range(num_of_readings):
                x[i] = -int( valid_dist_l[i] * math.cos(math.radians(valid_ang_l[i]) )/X_SCALE_FACTOR )
                y[i] =  int( valid_dist_l[i] * math.sin(math.radians(valid_ang_l[i]) )/Y_SCALE_FACTOR )
                if debug:
                   print("x[{}] y[{}]=[{} {}]".format(i,i,x[i],y[i]))

 
        #Create a grid  [ [top row] , [next lower] ... [bottom (y=0) row] ]
        grid = [[0 for a in xrange(grid_width-2)] for a in xrange(grid_height+1)]
        if debug:
            print("grid[0]:",grid[0])
            print("len(grid):",len(grid))

        if debug:  print("Put value 1 in grid for each trusted_reading")
        for i in range (num_of_readings):
                grid_x = int((grid_width-3)/2 + x[i])
                #if x[i] > 0: grid_x +=1
                grid_y = grid_height-y[i]
                if debug:
                    print("x[{0}]:{1} grid_x: {2}  y[{0}]:{3} grid_y: {4}".format(i,x[i],grid_x, y[i], grid_y))
                grid[grid_y][grid_x] = 1

        bot_fence=" "+'-'*int((grid_width-3)/2)+"0"+'-'*int((grid_width-3)/2)
        top_fence=" "+'-'*(grid_width-2)


        #Print the map
        label=("{:.0f} {}".format(int((grid_width-3)/2)*X_SCALE_FACTOR,units))
        print("\nMap:"+" "*int((grid_width-12)/2),label)
        print(top_fence)
        for i in range(grid_height+1):
                if debug:
                    print("|", end='')
                    for j in range (grid_width-2):
                        print(grid[i][j], end='')
                    print("|")
                print("|", end='')
                for j in range (grid_width-2):
                        if (j==int((grid_width-3)/2)) and i == grid_height:
                                print("+", end='')
                        elif grid[i][j]==0:
                                print(" ", end='')
                        else:
                                print("o", end='')
                print("|")
        print(bot_fence, label)
        closest_obj=min(valid_dist_l)
        farthest_reading=max(dist_l)
        print("Each '-' is {:.1f} {}      ".format(X_SCALE_FACTOR,units),end='')
        print("Each '|' is {:.1f} {}".format(Y_SCALE_FACTOR,units))
        print("Closest Object: {0:.0f} {1}  ".format(closest_obj,units),end='')
        print("Farthest Valid Object: {} {}".format(max_valid,units))
        print("Farthest Reading: {} {}".format(farthest_reading,units))
        return closest_obj      #Return the closest distance in all directions

# END view180()


# MAIN
def main():
		#Make Map, GoPiGo move forward if no object within , stops makes a map and again moves forward
    try:
	egpg.stop()
	while True:
		# Scan in front of GoPiGo3
		dist_l,ang_l=ds_map(sector=160,rev_axis=REVERSE_AXIS)
		closest_object = min(dist_l)
		servo.reset_servo()

		# Print scan data on terminal
		view180(dist_l,ang_l,grid_width=80,units="cm",ignore_over=230)

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
	servo.reset_servo()
	sleep(2)
	servo.disable_servo()


if __name__ == "__main__":
	main()
