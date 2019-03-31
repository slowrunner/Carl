#!/usr/bin/env python
#
# Juicer
"""
Detect and Report Charge|Trickle|Discharge Status

This module performs the following:
1) Detect Charging by 
2) Detect Trickle by
3) Detect Discharging by
4) Maintain X minute min/max/average voltage
5) Demo main will 
 - instantiate juicer object
 - print "status" to console every 10 seconds
 - Announce and print charging status changes
 - Request juice progressively more aggressively
       if discharging and battery voltage average falls below 8.1v
 - Request removal from juice when trickle charging 
       and battery voltage average falls below 8.1v 
 - Shutdown if average battery voltage falls below 7.4v

"""

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import sys
sys.path.append('/home/pi/Carl/plib')

from time import sleep, clock
import easygopigo3 # import the GoPiGo3 class
import math
import tiltpan
import status
import battery
import numpy

# variables to be maintained
readingList = [ ]
aveVolts = 0
maxVolts = 0
minVolts = 0
shortMeanVolts = 0
longMeanVolts = 0
deltaAveVolts = 0
deviationVolts = 0
shortMeanDuration = 60.0 #seconds
longMeanMultiplier = 5
longMeanDuration = shortMeanDuration * longMeanMultiplier
shortMeanCount = 9
longMeanCount = shortMeanCount * longMeanMultiplier
readingEvery = shortMeanDuration / shortMeanCount


def compute(egpg):
    global readingList,longMeanVolts,shortMeanVolts
    readingList += [egpg.volt()]
    if (len(readingList)>longMeanCount): 
      del readingList[0]
      longMeanVolts = numpy.mean(readingList)
    shortMeanVolts = numpy.mean(readingList[-5:-1])

def printValues():
    print ("\nJuicer Values:")
    print ("lastReading %.2f volts" % readingList[-1] )
    print ("num of readings %d" % len(readingList) )
    print ("shortMeanVolts %.2f volts" % shortMeanVolts)
    print ("longMeanVolts  %.2f volts" % longMeanVolts)

def main():

    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True) # Create an instance of the EasyGoPiGo3 class
    ds = egpg.init_distance_sensor()
    ts = egpg.init_servo(tiltpan.TILT_PORT)
    ps = egpg.init_servo(tiltpan.PAN_PORT)

    tiltpan.tiltpan_center()

    print ("Juicer Main Initialization")
    print ("shortMeanDuration: %.1f" % shortMeanDuration)
    print ("longMeanDuration: %.1f" % longMeanDuration)
    print ("readingEvery %.1f seconds" % readingEvery)
    
    try:
        #  loop
        while True:
            compute(egpg)
            status.printStatus(egpg,ds)
            printValues()
            sleep(readingEvery)
#            status.batterySafetyCheck()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    egpg.stop()           # stop motors
    	    print("Ctrl-C detected - Finishing up")
    egpg.stop()

if __name__ == "__main__":
	main()
