#!/usr/bin/env python

'''
# Routine for testing EasyGoPiGo drive_inches() method

'''

from __future__ import print_function
from __future__ import division

import time
import easygopigo3
import sys

egpg = easygopigo3.EasyGoPiGo3(use_mutex = True)

python_version = sys.version_info[0]
print("Python Version:",python_version)

def enc_to_distance_inches(enc):
	return egpg.WHEEL_CIRCUMFIRENCE * enc/360.0 * 0.0393701 

default_dist = 20
num_tries = 1
dist = default_dist

while True:
    print ("\nDrive ({:.1f} inches)?  (0=reset, +/- change default_dist by 0.1)".format(default_dist))
    if python_version < 3: i = raw_input()
    else: i = input()

    if len(i) == 0: dist = default_dist
    elif i == "-":
	default_dist -= 0.1
	print("New default_dist:{:.1f}".format(default_dist))
	continue
    elif i == "+":
	default_dist += 0.1
	print("New default_dist:{:.1f}".format(default_dist))
	continue
    elif i[0] == "x":
	num_turns = int(float(i[1:]))
        dist=default_dist
    elif i[0] == "1":
	default_dist += 1.0
	print("New default_dist:{:.1f}".format(default_dist))
	continue
    elif int(float(i)) == 0:
        egpg.reset_encoders()
        time.sleep(1)
        continue
    else: dist=float(i)


    try:
      for i in range(num_turns):
	print ("\n===== Drive {:.1f} Inches ========".format(dist))
	encoderStartLeft, encoderStartRight = egpg.read_encoders()
	print ( "Encoder Values: " + str(encoderStartLeft) + ' ' + str(encoderStartRight))	# print the encoder raw
	egpg.set_speed(120)  # DPS  (degrees per second rotation of wheels)
	startclock = time.clock()
	starttime  = time.time()
	egpg.drive_inches(dist)
	dist_processor_time = time.clock() - startclock
	dist_wall_time = time.time() - starttime
	print("Drive {:.1f} inches: Processor Time:{:.1f}ms,  Wall Time:{:.1f}s".format(dist, dist_processor_time*1000,dist_wall_time))
	time.sleep(1)		# to be sure totally stopped
	encoderEndLeft, encoderEndRight = egpg.read_encoders()
	deltaLeft = abs(encoderEndLeft - encoderStartLeft) 
	deltaRight = abs(encoderEndRight - encoderStartRight)
	deltaAve = (deltaLeft + deltaRight)/2.0
	deltaLeftdist = enc_to_distance_inches(deltaLeft)
	deltaRightdist = enc_to_distance_inches(deltaRight)
	print ("Encoder Value: " + str(encoderEndLeft) + ' ' + str(encoderEndRight))	# print the encoder raw
	print ("Delta Value: %d %d" % (deltaLeft, deltaRight))
	print ("Delta Distance: {:.1f} {:.1f}".format(deltaLeftdist, deltaRightdist))
	print ("Accuracy: {:.1f}% {:.1f}%".format(deltaLeftdist * 100 / dist, deltaRightdist * 100 / dist))
	wheelrate = deltaAve/dist_wall_time
	print ("Wheel Rate:{:.1f} dps   (includes start/stop effect)".format(wheelrate))
	#print ("Max wheel speed differential in encoder tics: %d" % maxWheelSpeedDiff)
	print ("=============")
	if num_turns > 1:
		print(" ^^^^ Drive {} ^^^^".format(i+1))
                dist = -dist
		time.sleep(2)
      num_turns = 1
    except KeyboardInterrupt:
	egpg.stop()

