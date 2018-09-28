#!/usr/bin/env python

'''
# Routine for testing EasyGoPiGo3.orbit() method
# under changing conditions using WHEEL_DIAMETER values to improve accuracy and repeatability
# Test Variables:
#   radius (13.35) cm  - change with rNN.N command  (75mm + 58.5mm half track = 6" dia circle formed by outer edge of inner wheel)
#   drive_speed (120 DPS)            - change with sNNN command
#   wheel diameter (63.7-63.975 mm makes my bot very accurate, repeatably)  - change by entering wNN.N at prompt
#   check_motor_status(False)  will change to non-blocking drive and check left and right motor status - "c"
#   ranging_active(False)  will perform read_inches() during each check motor status loop  - "r" 
#   num_tries (1)  -change with xN
#
#  Operation:  Return executes once, ? gives help
#
#  Results:
#     "Uncalibrated": -4% error with 0.2% repeatability (-2.75 inch error with 1/8 inch repeatability)
#     "Calibration" via wheel diameter adjustment: 0.2% drive-to-drive accuracy  (1/8 inch error in 5 feet travel)
#                   and 0.8% session, and session-to-session accuracy (1/2 inch error in 5 feet travel)

'''

from __future__ import print_function
from __future__ import division

import time
import easygopigo3
import sys
from math import pi


egpg = easygopigo3.EasyGoPiGo3(use_mutex = True)
ds   = egpg.init_distance_sensor()


python_version = sys.version_info[0]
print("Python Version:",python_version)

def enc_to_spin_deg(enc):
	return egpg.WHEEL_DIAMETER * enc / egpg.WHEEL_BASE_WIDTH


num_turns = 1
orbit_angle = 360
wd = 63.8     # mm  default EasyGoPiGo3.WHEEL_DIAMETER=66.5
check_motor_status = False
ranging_active = False
read_motor_status_delay = 0.010
orbit_speed = 120
orbit_rad_cm = 13.35

while True:
    print ("\nOrbit({},radius_cm={:.2f}) with Wheel Dia. {:.2f} mm at {} dps?  (? for help)".format(orbit_angle,orbit_rad_cm,wd,orbit_speed))
    if python_version < 3: i = raw_input()
    else: i = input()

    if len(i) == 0:
        num_turns = 1     # continues on to execute the orbit
    elif i[0] == "o":
	orbit_rad_cm = float(i[1:]) 
	print("New orbit_rad_cm:{:.2f}".format(orbit_rad_cm))
	continue
    elif i == "c":
        check_motor_status = not check_motor_status
        print("check_motor_status is now {}".format(check_motor_status))
	continue
    elif i == "h":
	orbit_angle = 180
	print("New orbit_angle:{:.1f}".format(orbit_angle))
	continue
    elif i == "f":
	orbit_angle = 360
	print("New orbit_angle:{:.1f}".format(orbit_angle))
	continue
    elif i[0] == "a":
	orbit_angle = int(float(i[1:])) 
	print("New orbit_angle:{}".format(orbit_angle))
	continue
    elif i == "c":
        check_motor_status = not check_motor_status
        print("check_motor_status is now {}".format(check_motor_status))
        continue
    elif i[0] == "d":
        read_motor_status_delay = float(i[1:])
        print("read_motor_status_delay is now {:.3f} seconds".format(read_motor_status_delay))
        continue
    elif i == "r":
        ranging_active = not ranging_active
        print("ranging_active is now {}".format(ranging_active))
        if ranging_active: check_motor_status = True
        print("check_motor_status is now {}".format(check_motor_status))
        continue
    elif i == "?":
	print("return  executes once with stated values")
        print("oNN.NN  sets orbit_rad_cm to NN.NN")
        print("c       toggle check_motor_status ({})".format(check_motor_status))
	print("h       change orbit_angle to 180 deg")
	print("f       change orbit_angle to 360 deg")
        print("aNNN    set orbit_angle to NNN deg")
        print("d.NNN   change read_motor_status_delay to .NNN seconds")
        print("r       toggle ranging active")
	print("xN      repeat with stated values N times")
        print("sNNN    change (outer) wheel speed dps to NNN")
	print("wNN.n   set wheel dia. to NN.n")
	print("?       print this list of commands")
	print("\nCurrent orbit_rad_cm:{:.2f}".format(orbit_rad_cm))
	print("Current WHEEL_DIAMETER:{:.2f}".format(wd))
	print("Current orbit_angle:{}".format(orbit_angle))
        print("Current speed:{}".format(orbit_speed))
        print("check_motor_status: {}".format(check_motor_status))
        print("read_motor_status_delay:{:.3f}".format(read_motor_status_delay))
        print("ranging_active: {}".format(ranging_active))
	continue
    elif i[0] == "x":
	num_turns = int(float(i[1:]))
    elif i[0] == "s":
        orbit_speed = int(float(i[1:]))
        print("New orbit_speed:{}".format(orbit_speed))
        continue
    elif i[0] == "w":
        wd = float(i[1:])
	print("New WHEEL_DIAMETER:{:.2f}".format(wd))
        continue
    else:
        print("Type ? for help")
        continue

    egpg.WHEEL_DIAMETER = wd
    egpg.WHEEL_CIRCUMFERENCE = wd * pi

    print("\nResetting Encoders")
    egpg.reset_encoders()
    time.sleep(1)
    try:
      for i in range(num_turns):
        print ("\n===== Orbit({},radius_cm={:.2f}) with Wheel Dia. {:.2f} mm at {} dps =====".format(orbit_angle,orbit_rad_cm,wd,orbit_speed))
	encoderStartLeft, encoderStartRight = egpg.read_encoders()
	print ( "Encoder Values: " + str(encoderStartLeft) + ' ' + str(encoderStartRight))	# print the encoder raw
	egpg.set_speed(orbit_speed)  # DPS  (degrees per second rotation of wheels)
	startclock = time.clock()
	starttime  = time.time()
	if check_motor_status:
            egpg.orbit(degrees=orbit_angle, radius_cm=orbit_rad_cm, blocking=False)
            time.sleep(0.25)  # initial delay to let motion start
            motors_running = True
            motor_status_count = 0
            while motors_running:
                time.sleep(read_motor_status_delay)
                if ranging_active: ds_reading = ds.read_inches()
                motors_state_l = egpg.get_motor_status(egpg.MOTOR_LEFT)
                motors_state_r = egpg.get_motor_status(egpg.MOTOR_RIGHT)
                motors_running = motors_state_l[3] | motors_state_r[3]
                motor_status_count += 1
        else:
            egpg.orbit(degrees=orbit_angle, radius_cm=orbit_rad_cm, blocking=True)
	orbit_processor_time = time.clock() - startclock
	orbit_wall_time = time.time() - starttime

	print("Orbit Processor Time:{:.1f}ms Wall Time:{:.1f}s".format(orbit_processor_time*1000,orbit_wall_time))
        if check_motor_status: print("get_motor_status(L)(R) called {} times".format(motor_status_count))
        if ranging_active: print("last distance sensor reading:{:.1f} inches".format(ds_reading))

	time.sleep(1)		# to be sure totally stopped
	encoderEndLeft, encoderEndRight = egpg.read_encoders()
	deltaLeft = abs(encoderEndLeft - encoderStartLeft) 
	deltaRight = abs(encoderEndRight - encoderStartRight)
	print ("Encoder Value: " + str(encoderEndLeft) + ' ' + str(encoderEndRight))	# print the encoder raw
	print ("Delta Value: %d %d" % (deltaLeft, deltaRight))
	orbit_rate = orbit_angle/orbit_wall_time
	wheelrateL = deltaLeft/orbit_wall_time
        wheelrateR = deltaRight/orbit_wall_time
	print ("Orbit Left Wheel Rate:{:.1f} dps Right Wheel Rate:{:.1f} dps (includes start/stop effect)".format(wheelrateL, wheelrateR))
	print ("=============")
	if num_turns > 1:
		print(" ^^^^ Orbit {} ^^^^".format(i+1))
		time.sleep(2)
      num_turns = 1
    except KeyboardInterrupt:
	egpg.stop()

