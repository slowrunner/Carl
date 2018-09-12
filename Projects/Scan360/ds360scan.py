#!/usr/bin/env python
#
# https://www.dexterindustries.com/GoPiGo/
# https://github.com/DexterInd/GoPiGo3
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md
#
# This code is an example for making the GoPiGo3 turn accurately using EasyGoPiGo3 class
#
# Results:  When you run this program, the GoPiGo3 should 
#                     turn 90 degrees to the right, 180 to the left, and then 90 to the right, ending where it started.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

from time import sleep
import easygopigo3 # import the GoPiGo3 class
import math
import printmaps




egpg = easygopigo3.EasyGoPiGo3(use_mutex=True) # Create an instance of the EasyGoPiGo3 class
distance_sensor = egpg.init_distance_sensor()


# GOPIGO3 CONSTANTS

TICS_PER_WHEEL_DEGREE = 2.0
WHEEL_DIAMETER = egpg.WHEEL_DIAMETER                    # 66.5 in mm   (measures 65.89 from circumfirence/pi)
WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * math.pi          # 208.92 mm    (measures 207 )
WHEEL_BASE_WIDTH = egpg.WHEEL_BASE_WIDTH                # 117 in mm    (static 114-115, cannot measure dynamic)
WHEEL_BASE_CIRCUMFERENCE = WHEEL_BASE_WIDTH * math.pi   # 367.57 mm    (cannot measure actual)

#
#   MOTORS RUNNING         Returns True/False
def motors_running():
    motors_state = egpg.get_motor_status(egpg.MOTOR_LEFT)[3] | egpg.get_motor_status(egpg.MOTOR_RIGHT)[3]
    return (motors_state != 0)

def spin_and_scan(degrees=360, speed=100):
    debug = True
    reading_l = []
    at_angle_l = []

    # reset encoders to 0
    egpg.reset_encoders()

    # Limit the speed
    egpg.set_speed(speed)

    # Take and Store Reading
    reading_l += [distance_sensor.read()]    # in cm
    at_angle_l += [90.0]                     # First reading straight ahead
    readings = 1


    # calculate an initial delay to limit readings loop
    time_360_at_100 = 4.0 # seconds
    default_readings=16
    reading_delay = time_360_at_100/default_readings * 0.9

    # Start the spin
    egpg.turn_degrees(degrees,blocking=False)

    # delay before reading again
    sleep(reading_delay)

    # probably should have a timeout safety exit on this loop
    while motors_running():
        # take a new reading
        reading_l += [distance_sensor.read_mm()]    #in mm for no loss of precision

        # Find out how much we've spun so far
        left_enc,right_enc = egpg.read_encoders()      		# degrees each wheel turned
        ave_encoders = (abs(left_enc) + abs(right_enc)) / 2.0   # in case one turns a little faster
	if debug:
	    print("left enc:{} right enc:{}  ave enc:{:.1f}".format(left_enc,right_enc,ave_encoders))

        # starting at GoPiGo3 angle 90  (0 = left  90 = straight ahead)
        # angle = 90 + (Wheel Dia * Ave_Enc) / Wheel Base Cir     # simplified by *pi/pi) and *360/360 cancels
        at_angle_l +=  [( (WHEEL_DIAMETER * ave_encoders) / WHEEL_BASE_CIRCUMFERENCE) % 360 ]
        readings += 1

	if debug:
	   print("Readings:{} Reading:{:.1f} Angle:{:.1f}".format(readings, \
								reading_l[readings-1], at_angle_l[readings-1]))

	# adjust delay to get requested number of readings during the spin
        sleep(reading_delay)

    return reading_l, at_angle_l





def main():
    dist_list_mm = []
    at_angle_list = []

    try:
        dist_list_mm,at_angle_list = spin_and_scan(360, speed=100)   # spin in place and take distance sensor readings
        range_list_cm = [ dist/10 for dist in dist_list_mm ]
        printmaps.view360(range_list_cm, at_angle_list)                # print view (all r positive, theta 0=left)
        egpg.stop()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    	egpg.stop()           # stop motors 
    	print("Ctrl-C detected - Finishing up")


if __name__ == "__main__":
	main()
