#!/usr/bin/env python

'''
# Routine for testing EasyGoPiGo3.turn_degrees() method
#
# Operation:
>Spin 360 Wheel Dia:66.50 Base:117.0 mm?  (? for help)

 return  execute with stated values once
 aNNN.n  set default angle to NNN.n
 c       toggle check_motor_status (False)
 h       change default_turn to 180 deg
 f       change default_turn to 360 deg
 aNNN.n  change default_turn to NNN deg
 xN      execute spin N times
 sNNN    change motor dps to NNN
 wNN.n   set WHEEL_DIAMETER to NN.n
 bNNN.n  set WHEEL_BASE_WIDTH to NNN.n
 ?       print list of commands

 WHEEL_DIA:66.50
 WHEEL_BASE_WIDTH:117.0
 default_turn:360
 spin_speed:120
#
# Result:  When the WHEEL_DIAMETER has been calibrated using wheelDiaDriveTest.py,
#          The default WHEEL_BASE_WIDTH of 117 mm  yields the best accuracy on six 360deg spins
#          09-30-2018 with batteries installed inside Carl's body, and new Pololu 1" castor ball
#          Calibration: WHEEL_DIAMETER: 64.5mm  WHEEL_BASE_WIDTH: 114.72-114.75
#

'''

from __future__ import print_function
from __future__ import division

import sys

try:
    sys.path.append('/home/pi/Carl/plib')
    import speak
    import tiltpan
    import status
    import battery
    import myDistSensor
    import runLog
    import myconfig
    Carl = True
except:
    Carl = False


import time
import easygopigo3
from math import pi

egpg = easygopigo3.EasyGoPiGo3(use_mutex = True)
ds   = egpg.init_distance_sensor()

if Carl:
    runLog.logger.info("Started")
    myconfig.setParameters(egpg)   # configure custom wheel dia and base
    tiltpan.tiltpan_center()
    time.sleep(0.5)
    tiltpan.off()

python_version = sys.version_info[0]
print("Python Version:",python_version)

def enc_to_spin_deg(enc):
	return egpg.WHEEL_DIAMETER * enc / egpg.WHEEL_BASE_WIDTH

default_turn = 360
num_turns = 1
deg = default_turn
wd = egpg.WHEEL_DIAMETER
wbw= egpg.WHEEL_BASE_WIDTH
check_motor_status = False
read_motor_status_delay = 0.1
spin_speed = 120

while True:
    print ("\nSpin {} Wheel Dia:{:.2f} Base:{:.2f} mm?  (? for help)".format(deg,wd,wbw))
    if python_version < 3: i = raw_input()
    else: i = input()

    if len(i) == 0:
        num_turns = 1
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
        print("return  execute with stated values once")
        print("aNNN.n  set default_turn to NNN.n")
        print("bNNN.n  set wheel base width to NNN.n")
        print("c       toggle check_motor_status ({})".format(check_motor_status))
	print("h       change default_turn to 180 deg")
	print("f       change default_turn to 360 deg")
	print("xN      execute spin N times")
        print("sNNN    change motor dps to NNN")
	print("wNN.n   set wheel diameter to NN.n")
        print("bNNN.n  set wheel base to NNN.n")
	print("?       print list of commands")
	print("WHEEL_DIA:{:.2f}".format(wd))
        print("WHEEL_BASE_WIDTH:{:.1f}".format(wbw))
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
    elif i[0] == "w":
	wd = float(i[1:])
	print("New WHEEL_DIAMETER:{:.2f}".format(wd))
        continue
    elif i[0] == "b":
	wbw = float(i[1:])
	print("New WHEEL_BASE_WIDTH:{:.2f}".format(wbw))
        continue
    elif i[0] == "a":
	default_turn = float(i[1:])
        deg = default_turn
	print("New default spin:{:.2f}".format(default_turn))
        continue
    else:
        print("Type ? for help")
        continue

    egpg.WHEEL_DIAMETER = wd
    egpg.WHEEL_CIRCUMFERENCE = wd * pi
    egpg.WHEEL_BASE_WIDTH = wbw
    egpg.WHEEL_BASE_CIRCUMFERENCE = wbw * pi

    print("\nResetting Encoders")
    egpg.reset_encoders()
    time.sleep(1)
    try:
      for i in range(num_turns):
	print ("\n===== Spin {:.1f} WHEEL_DIAMETER:{:.2f} WHEEL_BASE_WIDTH:{:.2f} mm at {} dps ========".format(deg,wd,wbw,spin_speed))
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


    if Carl:  runLog.logger.info("Exit")
