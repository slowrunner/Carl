#!/usr/bin/env python3
############################################################################################
# Create LIDAR like map using DI TOF Distance Sensor on tiltpan mount with the GoPiGo
#
# History
# ------------------------------------------------
# Author     	Date      		Comments
# McDonley	July 2019		Convert to Carl's tiltpan class
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
  import myDistSensor
  import tiltpan
  import myconfig
  import argparse

except:
  carl = False
from collections import Counter
import math
from time import sleep
import printmaps
import numpy as np

debug = False			# True to print all raw values

delay = 0.02			# give servo time to finish moving


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
def ds_map(ds, tp, sector=160,limit=300,num_of_readings=18,samples=1,rev_axis=False):
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
			tp.pan(ang)		# DI Servo Package has shaft up, 0 = left
		else:
			tp.pan(180-ang)	# Shaft down servo configuration 0 = right
		sleep(delay)

		#Take the readings from the Distance sensor for this angle, validate within limit
		for i in range(samples):
			dist = myDistSensor.adjustReadingInMMForError(ds.read_mm()) / 10.0  # in cm
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
			tp.pan(ang)		# DI Servo Package has shaft up, 0 = left
		else:
			tp.pan(180-ang)	# Shaft down servo configuration 0 = right
		sleep(delay)
		ang+=incr
		if ang>right_angle:
			break
	return dist_l,ang_l
# END ds_map()

IGNORE_OVER_CM = 230


# returns r, theta_degrees
def cart2polar(x,y):
    return np.hypot(x,y), math.degrees(math.atan2(y,x))

def cartl2polarl(xl,yl):
    rl = []
    tl = []
    if 0 < len(xl) == len(yl):
        for x,y in zip(xl,yl):
            r,t = cart2polar(x,y)
            rl += [r]
            tl += [t]
    return rl,tl

# polar2cart(r,theta) returns x,y
def polar2cart(r,theta_deg):
    return r * math.cos(math.radians(theta_deg)), r * math.sin(math.radians(theta_deg))

def polarl2cartl(rl, theta_degl):
    xl = []
    yl = []
    if 0 < len(rl) == len(theta_degl):
        for r,theta in zip(rl,theta_degl):
            x,y = polar2cart(r,theta)
            xl += [x]
            yl += [y]
    return xl,yl

def wallAngle(x_list,y_list):
        angle = float('nan')
        if len(y_list) == len(x_list) > 1:
            wall_mb = np.polyfit(x_list,y_list,1)
            #print ("wall_mb",wall_mb)
            #print ("wall_mb[0]",wall_mb[0])
            angle = np.arctan(wall_mb[0])
        return angle


def wallAngleScan(ds,tp,sector=45,verbose=False):

        # Scan in front of GoPiGo3
        dist_l,ang_l=ds_map(ds,tp,sector)
        closest_object = min(dist_l)
        tp.center()
        tp.off()

        if verbose:
            # Print scan data on terminal
            printmaps.view180(dist_l,ang_l,grid_width=80,units="cm",ignore_over=IGNORE_OVER_CM)


        x_list,y_list = polarl2cartl(dist_l,ang_l)
        angle = wallAngle(x_list,y_list)
        if np.isnan(angle):
            if verbose:
                print("Not enough points to determine wall angle")
        else:
            angle = np.degrees(angle)
            if verbose: print("angle:{:.0f}".format(angle) )
        return angle





# MAIN
def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--drive", default=False, action='store_true', help="optional scan and drive forward")
    args = vars(ap.parse_args())
    driveFlag = args['drive']

    #Make Map, GoPiGo move forward if no object within , stops makes a map and again moves forward

    PERSONAL_SPACE = 25  # cm

    # Create an instance egpg of the GoPiGo3 class.
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)    # use_mutex=True for "thread-safety"
    myconfig.setParameters(egpg)

    if carl: runLog.logger.info("Starting servoscan.py at {0:0.2f}v".format(egpg.volt()))

    # Create an instance of the Distance Sensor class.
    # I2C1 and I2C2 are the two ports through which sensors can connect to the I2C bus
    # The sensor can be connected to either port to be "on the I2C bus" so no port id is needed
    # The EasyDistanceSensor will return trusted readings out to roughly 230 cm
    #                                    and returns 300 when no obstacle seen

    #ds = egpg.init_distance_sensor(port='RPI_1')   # must use HW I2C
    #servo = egpg.init_servo("SERVO1")
    ds = myDistSensor.init(egpg)
    tp = tiltpan.TiltPan(egpg)

    try:
        egpg.stop()
        while True:
            # Scan in front of GoPiGo3
            dist_l,ang_l=ds_map(ds, tp, sector=160)
            closest_object = min(dist_l)
            tp.center()

            # Print scan data on terminal
            printmaps.view180(dist_l,ang_l,grid_width=80,units="cm",ignore_over=230)

            if driveFlag:
                # Decide if can move forward
                if (closest_object < PERSONAL_SPACE):	#If any obstacle is closer than desired, stop
                    print("\n!!! FREEZE - THERE IS SOMETHING INSIDE MY PERSONAL SPACE !!!\n")
                    break

                # We have clearance to move
                dist_to_drive = (closest_object * 0.3)
                print("\n*** WE HAVE CLEARANCE TO MOVE {:.1f}cm ***".format(dist_to_drive))
                sleep(5)
                egpg.drive_cm(dist_to_drive,blocking = True)	# drive 1/3 of the distance to closest object
            print("\n*** PAUSING TO ENJOY THE VIEW ***")
            sleep(15)
            print("\n*** Wall Angle Scan ***")
            angleToWallNormal = wallAngleScan(ds,tp,verbose=True)
            sleep(5)
        # Continue here when object within personal space
        tp.center()
        sleep(2)
        tp.off()

    except KeyboardInterrupt:
        print("\n**** Ctrl-C detected.  Finishing Up ****")
        if carl: runLog.logger.info("Exiting  servoscan.py at {0:0.2f}v".format(egpg.volt()))
        tp.center()
        sleep(2)
        tp.off()


if __name__ == "__main__":
	main()
