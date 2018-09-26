#!/usr/bin/env python

'''
# Routine for testing EasyGoPiGo  drive_inches() method
# under changing conditions using WHEEL_DIAMETER values to improve accuracy and repeatability

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

def enc_to_dist(enc):
	return egpg.WHEEL_DIAMETER * enc / 360

def minus_if_odd(a):
    if a & 1:  rv = -1
    else: rv = 1
    return rv

default_dist = 20.0  # inches
num_tries = 1
dist = default_dist
wd = egpg.WHEEL_DIAMETER
check_motor_status = False
read_motor_status_delay = 0.1
drive_speed = 120

while True:
    print ("\nDrive {} inches with Wheel Dia.({:.2f} mm)?  (? for help)".format(dist,wd))
    if python_version < 3: i = raw_input()
    else: i = input()

    if len(i) == 0: wd = 66.5
    elif i == "-":
	dist -= 0.1
	print("New drive distance:{:.2f}".format(dist))
	continue
    elif i == "+":
	dist += 0.1
	print("New drive distance:{:.2f}".format(dist))
	continue
    elif i == "c":
        check_motor_status = not check_motor_status
        print("check_motor_status is now {}".format(check_motor_status))
        continue
    elif i == "?":
	print("-    decrease distance by 0.1 inch")
	print("+    increase distance by 0.1 inch")
        print("c    toggle check_motor_status ({})".format(check_motor_status))
	print("xN   repeat drive N times (fwd, bwd, fwd...)")
        print("sNNN change motor dps to NNN")
	print("NN.n set WHEEL_DIAMETER to NN.n and drive  once")
	print("?    print list of commands")
	print("Current WHEEL_DIAMETER:{:.2f}".format(wd))
	print("Current Distance:{}".format(dist))
        print("Current Speed:{} dps".format(drive_speed))
	continue
    elif i[0] == "x":
	num_tries = int(float(i[1:]))
    elif i[0] == "s":
        drive_speed = int(float(i[1:]))
        print("New drive_speed:{}".format(drive_speed))
        continue
    else:         # NN.N  new WHEEL_DIAMETER
	wd=float(i)


    egpg.WHEEL_DIAMETER = wd
    egpg.WHEEL_CIRCUMFERENCE = wd * pi

    print("\nResetting Encoders")
    egpg.reset_encoders()
    time.sleep(1)
    try:
      for i in range(num_tries):
	print ("\n===== Drive {:.1f} inches with WHEEL_DIA: {:.2f} mm at {} dps ========".format(dist,wd,drive_speed))
	encoderStartLeft, encoderStartRight = egpg.read_encoders()
	print ( "Encoder Values: " + str(encoderStartLeft) + ' ' + str(encoderStartRight))
	egpg.set_speed(drive_speed)  # DPS  (degrees per second rotation of wheels)
	startclock = time.clock()
	starttime  = time.time()
	if check_motor_status:
            egpg.drive_inches(minus_if_odd(i)*dist,blocking=False)
            time.sleep(0.25)  # initial delay to let motion start
            motors_running = True
            motor_status_count = 0
            while motors_running:
                time.sleep(read_motor_status_delay)
                motors_state_l = egpg.get_motor_status(egpg.MOTOR_LEFT)
                motors_state_r = egpg.get_motor_status(egpg.MOTOR_RIGHT)
                motors_running = motors_state_l[3] | motors_state_r[3]
                motor_status_count += 2
        else:
            egpg.drive_inches(minus_if_odd(i)*dist)
	drive_processor_time = time.clock() - startclock
	drive_wall_time = time.time() - starttime

	print("Drive Time:{:.1f}ms Wall Time:{:.1f}s".format(drive_processor_time*1000,drive_wall_time))
        if check_motor_status: print("get_motor_status() called {} times".format(motor_status_count))

	time.sleep(1)		# to be sure totally stopped
	encoderEndLeft, encoderEndRight = egpg.read_encoders()
	deltaLeft = abs(encoderEndLeft - encoderStartLeft)
	deltaRight = abs(encoderEndRight - encoderStartRight)
	deltaAve = (deltaLeft + deltaRight)/2.0
	deltaLeftdist = enc_to_dist(deltaLeft)
	deltaRightdist = enc_to_dist(deltaRight)
	print ("Encoder Value: " + str(encoderEndLeft) + ' ' + str(encoderEndRight))	# print the encoder raw
	print ("Delta Value: %d %d" % (deltaLeft, deltaRight))
	print ("Distance: L {:.2f} R {:.2f} Ave {:.2f}".format(deltaLeftdist, deltaRightdist))
	print ("Accuracy: L {:.1f}% R {:.1f}% Ave {:.1f}%".format(
                                       deltaLeftdist * 100 / dist,
                                       deltaRightdist * 100 / dist,
                                       deltaAve * 100 / dist ))
	drive_rate = dist/drive_wall_time
	wheelrate = deltaAve/turn_wall_time
	print ("Drive Rate:{:.1f} in/s Wheel Rate:{:.1f} dps (includes start/stop effect)".format(drive_rate, wheelrate))
	print ("=============")
	if num_tries > 1:
		print(" ^^^^ Drive {} ^^^^".format(i+1))
		time.sleep(2)
      num_tries = 1
    except KeyboardInterrupt:
	egpg.stop()

