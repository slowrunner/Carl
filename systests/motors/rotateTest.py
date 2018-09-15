#!/usr/bin/env python

'''
# Routine for testing EasyGoPiGo rotate_deg() method

'''

from __future__ import print_function
from __future__ import division

import time
import easygopigo3
import sys

egpg = easygopigo3.EasyGoPiGo3(use_mutex = True)

python_version = sys.version_info[0]
print("Python Version:",python_version)

def enc_to_spin_deg(enc):
	return egpg.WHEEL_DIAMETER * enc / egpg.WHEEL_BASE_WIDTH

default_turn = 360
num_turns = 1
deg = default_turn

while True:
    print ("\nSpin ({:.1f} deg)?  (0=reset, +/- change default_turn by 0.1)".format(default_turn))
    if python_version < 3: i = raw_input()
    else: i = input()

    if len(i) == 0: deg = default_turn
    elif i == "-":
	default_turn -= 0.1
	print("New default_turn:{:.1f}".format(default_turn))
	continue
    elif i == "+":
	default_turn += 0.1
	print("New default_turn:{:.1f}".format(default_turn))
	continue
    elif i[0] == "x":
	num_turns = int(float(i[1:]))
        deg=default_turn
    elif i[0] == "1":
	default_turn += 1.0
	print("New default_turn:{:.1f}".format(default_turn))
	continue
    elif int(float(i)) == 0:
        egpg.reset_encoders()
        time.sleep(1)
        continue
    else: deg=float(i)


    try:
      for i in range(num_turns):
	print ("\n===== Spin {:.1f} Degrees ========".format(deg))
	encoderStartLeft, encoderStartRight = egpg.read_encoders()
	print ( "Encoder Values: " + str(encoderStartLeft) + ' ' + str(encoderStartRight))	# print the encoder raw
	egpg.set_speed(120)  # DPS  (degrees per second rotation of wheels)
	startclock = time.clock()
	starttime  = time.time()
	egpg.turn_degrees(deg)
	turn_processor_time = time.clock() - startclock
	turn_wall_time = time.time() - starttime
	print("Turn Processor Time:{:.1f}ms Wall Time:{:.1f}s".format(turn_processor_time*1000,turn_wall_time))
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
	#print ("Max wheel speed differential in encoder tics: %d" % maxWheelSpeedDiff)
	print ("=============")
	if num_turns > 1:
		print(" ^^^^ Turn {} ^^^^".format(i+1))
		time.sleep(2)
      num_turns = 1
    except KeyboardInterrupt:
	egpg.stop()

