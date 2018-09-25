#!/usr/bin/env python

'''
# Routine for testing EasyGoPiGo WHEEL_DIAMETER using the rotate_deg() method

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

default_turn = 360
num_turns = 1
deg = default_turn
wd = egpg.WHEEL_DIAMETER
default_wd = wd
check_motor_status = False
read_motor_status_delay = 0.1
spin_speed = 120

while True:
    print ("\nSpin {} with Wheel Dia.({:.2f} mm)?  (? for help)".format(deg,default_wd))
    if python_version < 3: i = raw_input()
    else: i = input()

    if len(i) == 0: wd = default_wd
    elif i == "-":
	default_wd -= 0.1
	print("New default_wd:{:.2f}".format(default_wd))
	continue
    elif i == "+":
	default_wd += 0.1
	print("New default_wd:{:.2f}".format(default_wd))
	continue
    elif i == "h":
	deg = default_turn = 180
	print("New default_turn:{:.1f}".format(default_turn))
	continue
    elif i == "f":
	deg = default_turn = 360
	print("New default_turn:{:.1f}".format(default_turn))
	continue
    elif i == "c":
        check_motor_status = not check_motor_status
        print("check_motor_status is now {}".format(check_motor_status))
        continue
    elif i == "?":
	print("-    decrease default_wd by 0.1")
	print("+    increase default_wd by 0.1")
        print("c    toggle check_motor_status ({})".format(check_motor_status))
	print("h    change default_turn to 180 deg")
	print("f    change default_turn to 360 deg")
	print("xN   repeat default_turn with default_wd N times")
        print("sNNN change motor dps to NNN")
	print("NN.n set default_wd to NN.n and spin default_turn once")
	print("?    print list of commands")
	print("default_wd:{:.2f}".format(default_wd))
	print("default_turn:{}".format(default_turn))
        print("spin_speed:{}".format(spin_speed))
	continue
    elif i[0] == "x":
	num_turns = int(float(i[1:]))
        deg=default_turn
    elif i[0] == "s":
        spin_speed = int(float(i[1:]))
        print("New spin_speed:{}".format(spin_speed))
        continue
    elif int(float(i)) == 0:
	default_wd = egpg.WHEEL_DIAMETER
	wd = default_wd
	print("New default_wd:{:.2f}".format(default_wd))
        continue
    else:
	wd=float(i)
	default_wd=wd

    egpg.WHEEL_DIAMETER = wd
    egpg.WHEEL_CIRCUMFERENCE = wd * pi

    print("\nResetting Encoders")
    egpg.reset_encoders()
    time.sleep(1)
    try:
      for i in range(num_turns):
	print ("\n===== Spin {:.1f} Degrees with WHEEL_DIA: {:.2f} mm at {} dps ========".format(deg,wd,spin_speed))
	encoderStartLeft, encoderStartRight = egpg.read_encoders()
	print ( "Encoder Values: " + str(encoderStartLeft) + ' ' + str(encoderStartRight))	# print the encoder raw
	egpg.set_speed(spin_speed)  # DPS  (degrees per second rotation of wheels)
	startclock = time.clock()
	starttime  = time.time()
	if check_motor_status:
            egpg.turn_degrees(deg,blocking=False)
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
            egpg.turn_degrees(deg)
	turn_processor_time = time.clock() - startclock
	turn_wall_time = time.time() - starttime

	print("Turn Processor Time:{:.1f}ms Wall Time:{:.1f}s".format(turn_processor_time*1000,turn_wall_time))
        if check_motor_status: print("get_motor_status() called {} times".format(motor_status_count))

	time.sleep(1)		# to be sure totally stopped
	encoderEndLeft, encoderEndRight = egpg.read_encoders()
	deltaLeft = abs(encoderEndLeft - encoderStartLeft) 
	deltaRight = abs(encoderEndRight - encoderStartRight)
	deltaAve = (deltaLeft + deltaRight)/2.0
	deltaLeftDeg = enc_to_spin_deg(deltaLeft)
	deltaRightDeg = enc_to_spin_deg(deltaRight)
	print ("Encoder Value: " + str(encoderEndLeft) + ' ' + str(encoderEndRight))	# print the encoder raw
	print ("Delta Value: %d %d" % (deltaLeft, deltaRight))
	print ("Delta Degrees: {:.1f} {:.1f}".format(deltaLeftDeg, deltaRightDeg))
	print ("Accuracy: {:.1f}% {:.1f}%".format(deltaLeftDeg * 100 / deg, deltaRightDeg * 100 / deg))
	spinrate = deg/turn_wall_time
	wheelrate = deltaAve/turn_wall_time
	print ("Spin Rate:{:.1f} dps Wheel Rate:{:.1f} dps (includes start/stop effect)".format(spinrate, wheelrate))
	print ("=============")
	if num_turns > 1:
		print(" ^^^^ Turn {} ^^^^".format(i+1))
		time.sleep(2)
      num_turns = 1
    except KeyboardInterrupt:
	egpg.stop()

