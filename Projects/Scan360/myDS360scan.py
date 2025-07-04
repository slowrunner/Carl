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
#
#

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

from time import sleep, clock
import easygopigo3 # import the GoPiGo3 class
import math
import printmaps




egpg = easygopigo3.EasyGoPiGo3(use_mutex=True) # Create an instance of the EasyGoPiGo3 class
distance_sensor = egpg.init_distance_sensor()


# Adjust GOPIGO3 CONSTANTS to my bot   default EasyGoPiGo3.WHEEL_DIAMETER = 66.5 mm
egpg.WHEEL_DIAMETER = 64.35				# empirical from systests/wheelDiaRotateTest.py
egpg.WHEEL_CIRCUMFERENCE = egpg.WHEEL_DIAMETER * math.pi

WHEEL_DIAMETER = egpg.WHEEL_DIAMETER                    # 66.5 mm default, use adjusted value
WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * math.pi          # 208.92 mm    (measures 207 )
WHEEL_BASE_WIDTH = egpg.WHEEL_BASE_WIDTH                # 117 in mm    (static 114-115, cannot measure dynamic)
WHEEL_BASE_CIRCUMFERENCE = WHEEL_BASE_WIDTH * math.pi   # 367.57 mm    (cannot measure actual)


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
#	At speed=300 takes about  18 readings (~20 deg)
#	At speed=100 takes about  36 readings (~10 deg)
#	At speed= 50 takes about  72 readings (~ 5 deg)
#	At speed= 30 takes about 120 readings (~ 3 deg)
#
def spin_and_scan(degrees=360, speed=50):
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
    motors_state_l = egpg.get_motor_status(egpg.MOTOR_LEFT)
    motors_state_r = egpg.get_motor_status(egpg.MOTOR_RIGHT)

    enc_left = motors_state_l[2]
    enc_right = motors_state_r[2]
    ave_enc_l +=[ (abs(enc_left) + abs(enc_right)) * 0.5]   # save average in case one turns a little faster
    if debug:
	print("left enc:{} right enc:{}  ave enc:{:.1f}".format(enc_left,enc_right,ave_enc_l[readings]))
    readings = 1


    # calculate an initial delay to let motion begin before next reading
    if speed < 50:
    	startup_delay = 0.35  # seconds
    else:
    	startup_delay = 0.25 - (0.03 * speed/50)  # seconds

    # Start the spin
    egpg.turn_degrees(degrees,blocking=False)

    # delay before reading again
    sleep(startup_delay)

    # check that motors are running
    motors_state_l = egpg.get_motor_status(egpg.MOTOR_LEFT)
    motors_state_r = egpg.get_motor_status(egpg.MOTOR_RIGHT)
    motors_running = motors_state_l[3] | motors_state_r[3]

    # start a timer
    if timing: start = clock()


    # probably should have a timeout safety exit on this loop
    while motors_running:

    	# Take and Store Reading
    	reading_l += [distance_sensor.read_mm()]     # in mm to keep precision

	# get encoder value and motor speed value
  	motors_state_l = egpg.get_motor_status(egpg.MOTOR_LEFT)
    	motors_state_r = egpg.get_motor_status(egpg.MOTOR_RIGHT)

	# if either motor/wheel has a non-zero speed, motors_running will be set non-zero (used as True/False)
    	motors_running = motors_state_l[3] | motors_state_r[3]

	# extract encoder values from motor state returns
    	enc_left = motors_state_l[2]
    	enc_right = motors_state_r[2]

	# save encoder average in a list (averaged in case one turns a little faster)
    	ave_enc_l +=[ (abs(enc_left) + abs(enc_right)) / 2.0]
    	if debug:
	   print("left enc:{} right enc:{}  ave enc:{:.1f}".format(enc_left,enc_right,ave_enc_l[readings]))

	if debug:
	    print("\nleft enc:{} right enc:{} ave enc:{:.1f}".format(enc_left,enc_right,ave_enc_l[readings]))
	    print("Readings:{} Reading:{:.1f} spun:{:.1f} deg".format(readings, \
								reading_l[readings], \
								encoder_ave_to_spin_deg(ave_enc_l[readings])))
	# increment readings count for this datum
        readings += 1

	# timer to measure loop
        if timing: reading_took=clock() - start

        #sleep(reading_delay)
	if timing: start = clock()

    # convert average encoder reading to degrees turned and add 90 degrees for start angle
    # angle = 90 + (Wheel Dia * Ave_Enc) / Wheel Base Cir     # simplified by *pi/pi) and *360/360 cancels
    at_angle_l =  [( (90 + encoder_ave_to_spin_deg(ave_encoders))  % 360) for ave_encoders in ave_enc_l  ]
    if timing: print("last reading took:",reading_took)
    return reading_l, at_angle_l





def main():
    dist_list_mm = []
    at_angle_list = []
    # speeds = [300, 100, 50, 30]
    speeds = [120, 120]
    for spd in speeds:
	try:
	    print("\nSPIN 360 AND SCAN at speed={}".format(spd))
	    dist_list_mm,at_angle_list = spin_and_scan(360, speed=spd)   # spin in place and take distance sensor readings
	    range_list_cm = [ dist/10 for dist in dist_list_mm ]
	    printmaps.view360(range_list_cm, at_angle_list)                # print view (all r positive, theta 0=left
	    print("Readings:{}".format(len(at_angle_list)))

	except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    egpg.stop()           # stop motors
    	    print("Ctrl-C detected - Finishing up")
    egpg.stop()

if __name__ == "__main__":
	main()
