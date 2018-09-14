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

from time import sleep, clock
import easygopigo3 # import the GoPiGo3 class
import math
import printmaps




egpg = easygopigo3.EasyGoPiGo3(use_mutex=True) # Create an instance of the EasyGoPiGo3 class
distance_sensor = egpg.init_distance_sensor()
distance_sensor.start_continuous(100)

# GOPIGO3 CONSTANTS


WHEEL_DIAMETER = egpg.WHEEL_DIAMETER                    # 66.5 in mm   (measures 65.89 from circumfirence/pi)
WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * math.pi          # 208.92 mm    (measures 207 )
WHEEL_BASE_WIDTH = egpg.WHEEL_BASE_WIDTH                # 117 in mm    (static 114-115, cannot measure dynamic)
WHEEL_BASE_CIRCUMFERENCE = WHEEL_BASE_WIDTH * math.pi   # 367.57 mm    (cannot measure actual)

#
#   MOTORS RUNNING         Returns True/False
def motors_running():
    motors_state = egpg.get_motor_status(egpg.MOTOR_LEFT)[3] | egpg.get_motor_status(egpg.MOTOR_RIGHT)[3]
    return (motors_state != 0)

#
#   ENCODER AVERAGE TO SPIN DEGREES
def encoder_ave_to_spin_deg(encoder_ave):

    # deg = (WHEEL_DIAMETER*pi * encoder_ave/360)   / (WHEEL_BASE_WIDTH*pi /360) )
    # simplify by *pi/*pi  360/360
    d = WHEEL_DIAMETER * encoder_ave / WHEEL_BASE_WIDTH
    return d

#
#   SPIN AND SCAN 
#	Spin in place taking distance sensor readings as often as possible
#	At the default speed (100) takes about 36 readings on a RPi 3B (four-core 1.2GHz)
#	At speed=300 takes about 15 readings
#
def spin_and_scan(degrees=360, speed=100):
    debug = False
    timing= False

    reading_l = []
    at_angle_l = []
    ave_enc_l = []
    readings = 0

    # reset encoders to 0
    egpg.reset_encoders()

    # Limit the speed
    egpg.set_speed(speed)

    # Take and Store Reading
    reading_l += [distance_sensor.read_mm()]     # in mm to keep precision
    left_enc,right_enc = egpg.read_encoders() # degrees each wheel turned (should be 0)
    ave_enc_l +=[ (abs(left_enc) + abs(right_enc)) / 2.0]   # save ave encoder for first reading
    if debug:
	print("left enc:{} right enc:{}  ave enc:{:.1f}".format(left_enc,right_enc,ave_enc_l[readings]))
    readings = 1


    # calculate an initial delay to let motion begin before next reading
    startup_delay = 0.3 * 100/speed  # seconds
    reading_delay = 0.005

    # Start the spin
    egpg.turn_degrees(degrees,blocking=False)

    # delay before reading again
    sleep(startup_delay)

    # start a timer
    if timing: start = clock()

    # probably should have a timeout safety exit on this loop
    while motors_running():

        # Find out how much we've spun so far
        left_enc,right_enc = egpg.read_encoders()      		# degrees each wheel turned
        ave_enc_l +=[ (abs(left_enc) + abs(right_enc)) / 2.0]   # save average in case one turns a little faster

        # take a new reading
        reading_l += [distance_sensor.read_range_continuous()]    #in mm for no loss of precision

	if debug:
	    print("\nleft enc:{} right enc:{} ave enc:{:.1f}".format(left_enc,right_enc,ave_enc_l[readings]))
	    print("Readings:{} Reading:{:.1f} spun:{:.1f} deg".format(readings, \
								reading_l[readings], \
								encoder_ave_to_spin_deg(ave_enc_l[readings])))
	# increment readings count for this datum
        readings += 1

	# timer to measure loop
        #if timing: reading_took=clock() - start

        sleep(reading_delay)
	#if timing: start = clock()

    # convert average encoder reading to degrees turned and add 90 degrees for start angle
    # angle = 90 + (Wheel Dia * Ave_Enc) / Wheel Base Cir     # simplified by *pi/pi) and *360/360 cancels
    at_angle_l =  [( (90 + encoder_ave_to_spin_deg(ave_encoders))  % 360) for ave_encoders in ave_enc_l  ]
    if timing: print("last reading took:",reading_took)
    return reading_l, at_angle_l





def main():
    dist_list_mm = []
    at_angle_list = []

    try:
	print("\nSPIN 360 AND SCAN at speed=100")
        dist_list_mm,at_angle_list = spin_and_scan(360, speed=100)   # spin in place and take distance sensor readings
        range_list_cm = [ dist/10 for dist in dist_list_mm ]
        printmaps.view360(range_list_cm, at_angle_list)                # print view (all r positive, theta 0=left)
	print("Readings:{}\n",len(at_angle_list))

	print("\nSPIN 360 AND SCAN at speed=300")
        dist_list_mm,at_angle_list = spin_and_scan(360, speed=300)   # spin in place and take distance sensor readings
        range_list_cm = [ dist/10 for dist in dist_list_mm ]
        printmaps.view360(range_list_cm, at_angle_list)                # print view (all r positive, theta 0=left)
	print("Readings:{}\n",len(at_angle_list))

	print("\nSPIN 360 AND SCAN at speed=50")
        dist_list_mm,at_angle_list = spin_and_scan(360, speed=50)   # spin in place and take distance sensor readings
        range_list_cm = [ dist/10 for dist in dist_list_mm ]
        printmaps.view360(range_list_cm, at_angle_list)                # print view (all r positive, theta 0=left)
	print("Readings:{}\n",len(at_angle_list))
        egpg.stop()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    	egpg.stop()           # stop motors 
    	print("Ctrl-C detected - Finishing up")


if __name__ == "__main__":
	main()
