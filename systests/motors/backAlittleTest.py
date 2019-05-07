#!/usr/bin/env python

'''
# backAlittleTest.py  find a time needed to back a desired distance
#
# (docking requires backing until hit back stop, need to know how long to back)

'''

from __future__ import print_function
from __future__ import division

import time
import easygopigo3
import sys
sys.path.append('/home/pi/Carl/plib')
import lifeLog

egpg = easygopigo3.EasyGoPiGo3(use_mutex = True)

strToLog = "Starting backAlittleTest.py"
print(strToLog)
lifeLog.logger.info(strToLog)

python_version = sys.version_info[0]
print("Python Version:",python_version)

def enc_to_distance_mm(enc):
	return egpg.WHEEL_CIRCUMFERENCE * enc/360.0 # * 0.0393701 

default_dist = 6 #mm
num_tries = 1
dist = default_dist

while True:
    print ("\nBack({:.1f} mm)?  (0=reset, +/- change default_dist by 1mm)".format(default_dist))
    if python_version < 3: i = raw_input()
    else: i = input()

    if len(i) == 0: dist = default_dist
    elif i == "-":
	default_dist -= 1
	print("New default_dist:{:d}".format(default_dist))
	continue
    elif i == "+":
	default_dist += 1
	print("New default_dist:{:d}".format(default_dist))
	continue
    elif i == "d":
        print("Backing for 90 ms")
        egpg.set_speed(120)
        egpg.backward()
        time.sleep(0.090)
        egpg.stop()
        continue
    elif i[0] == "x":
	num_tries = int(float(i[1:]))
        dist=default_dist
    elif int(float(i)) == 0:
        egpg.reset_encoders()
        time.sleep(1)
        continue
    else: dist=int(i)


    try:
      for i in range(num_tries):
	print ("\n===== back {:d} mm ========".format(dist))
	encoderStartLeft, encoderStartRight = egpg.read_encoders()
	print ( "Encoder Values: " + str(encoderStartLeft) + ' ' + str(encoderStartRight))	# print the encoder raw
	egpg.set_speed(120)  # DPS  (degrees per second rotation of wheels)
	startclock = time.clock()
	starttime  = time.time()
	egpg.drive_cm(-dist/10.0)
	dist_processor_time = time.clock() - startclock
	dist_wall_time = time.time() - starttime
	print("Back {:d} mm: Processor Time:{:.1f}ms,  Wall Time:{:.1f}s".format(dist, dist_processor_time*1000,dist_wall_time))
	time.sleep(1)		# to be sure totally stopped
	encoderEndLeft, encoderEndRight = egpg.read_encoders()
	deltaLeft = abs(encoderEndLeft - encoderStartLeft) 
	deltaRight = abs(encoderEndRight - encoderStartRight)
	deltaAve = (deltaLeft + deltaRight)/2.0
	deltaLeftdist = enc_to_distance_mm(deltaLeft)
	deltaRightdist = enc_to_distance_mm(deltaRight)
	print ("Encoder Value: " + str(encoderEndLeft) + ' ' + str(encoderEndRight))	# print the encoder raw
	print ("Delta Value: %d %d" % (deltaLeft, deltaRight))
	print ("Delta Distance: {:0.1f} {:0.1f}".format(deltaLeftdist, deltaRightdist))
	print ("Accuracy: {:.1f}% {:.1f}%".format(deltaLeftdist * 100 / dist, deltaRightdist * 100 / dist))
	wheelrate = deltaAve/dist_wall_time
	print ("Wheel Rate:{:.1f} dps   (includes start/stop effect)".format(wheelrate))
	#print ("Max wheel speed differential in encoder tics: %d" % maxWheelSpeedDiff)
	print ("=============")
	if num_tries > 1:
		print(" ^^^^ Multi Backing Test {} ^^^^".format(i+1))
                dist = -dist
		time.sleep(2)
      num_tries = 1
    except KeyboardInterrupt:
	egpg.stop()
        strToLog = "Exiting backAlittleTest.py"
        print(strToLog)
        lifeLog.logger.info(strToLog)
        time.sleep(3)

