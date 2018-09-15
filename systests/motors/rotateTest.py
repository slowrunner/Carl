#!/usr/bin/env python

'''
# Routine for testing EasyGoPiGo rotate_deg() method

Note: based on rotationMotorTest.py by zolly
'''

from __future__ import print_function
from __future__ import division

import time
import easygopigo

egpg = easygopigo.EasyGoPiGo(use_Mutex = True)

#
while True:
    print ("Input is in degrees! Enter the degrees to move, or 0 to reset the encoders.")
    if p_version==2: i = int(raw_input())
    else: i = int(input())
    if i == 0:
        egpg.reset_encoders()
        time.sleep(1)
        continue 
    try:					
        print ("\n=============")
        encoderStartLeft, encodersStartRight = epgp.read_encoders()
        print ( "Encoder Values: " + str(encoderStartLeft) + ' ' + str(encoderStartRight))	# print the encoder raw 
        egpg.set_speed(120)  # DPS  (degrees per second rotation of wheels)
	startclock = time.clock()
	egpg.turn_degrees(i,blocking=True)
	turntime = time.clock() - startclock
	print("Turn Time:{:.1f)".format(turntime))
	time.sleep(0.5)		# to be sure totally stopped
        encoderEndLeft, encoderEndRight = egpg.read_encoders() 
        deltaLeft = abs(encoderEndLeft - encoderStartLeft) // 2
        deltaRight = abs(encoderEndRight - encoderStartRight) // 2
        print ("Encoder Value: " + str(encoderEndLeft) + ' ' + str(encoderEndRight))	# print the encoder raw
        print ("Delta Value: %d %d" % (deltaLeft, deltaRight))
        print ("Accuracy: %d %% %d %%" % (deltaLeft * 100 // abs(deg[0]), deltaRight * 100 // abs(deg[1])))
        #print ("Max wheel speed differential in encoder tics: %d" % maxWheelSpeedDiff)
        print ("=============")

