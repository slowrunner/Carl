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
shortMeanVolts = 0
shortPeakVolts = 0
shortMinVolts = 0
longPeakVolts = 0
longMeanVolts = 0
longMinVolts  = 0
shortMeanDuration = 60.0 #seconds
longMeanMultiplier = 5
longMeanDuration = shortMeanDuration * longMeanMultiplier
shortMeanCount = 9
longMeanCount = shortMeanCount * longMeanMultiplier
readingEvery = shortMeanDuration / shortMeanCount


def compute(egpg):
    global readingList,shortMeanVolts,shortPeakVolts,shortMinVolts
    global longMeanVolts,longPeakVolts,longMinVolts
    readingList += [egpg.volt()]
    if (len(readingList)>longMeanCount):
      del readingList[0]
      longMeanVolts = numpy.mean(readingList)
      longPeakVolts = numpy.max(readingList)
      longMinVolts  = numpy.min(readingList)

    shortList = readingList[-5:-1]
    if (len(shortList)>0):
      shortMeanVolts = numpy.mean(shortList)
      shortPeakVolts = numpy.max(shortList)
      shortMinVolts = numpy.min(shortList)

def printValues():
    print ("\nJuicer Values:")
    print ("lastReading %.2f volts" % readingList[-1] )
    print ("num of readings %d" % len(readingList) )
    print ("shortPeakVolts %.2f volts" % shortPeakVolts)
    print ("shortMeanVolts %.2f volts" % shortMeanVolts)
    print ("shortMinVolts  %.2f volts" % shortMinVolts)
    print ("longPeakVolts  %.2f volts" % longPeakVolts)
    print ("longMeanVolts  %.2f volts" % longMeanVolts)
    print ("longMinVolts   %.2f volts" % longMinVolts)

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
