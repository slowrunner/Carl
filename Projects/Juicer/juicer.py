#!/usr/bin/env python
#
# Juicer
"""
Detect and Report Charge|Trickle|Discharge Status

This module performs the following:
1) Detect Charging by linear approximation (y=mx+b) of readings having m>0
2) Detect Discharging by m<0
3) Detect Trickling by m>0 and peak voltage 0.5v or more higher than mean voltage
4) Maintain 1 minute and 5 minute peak and average voltage
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
import os
from time import sleep, clock
import easygopigo3 # import the GoPiGo3 class
import math
import tiltpan
import status
import battery
import numpy as np
import datetime as dt
import speak

# constants
UNKNOWN = 0
NOTCHARGING = 1   # disconnected 
CHARGING    = 2   # charging 
TRICKLING   = 3   # Trickle charging (less than load)
printableCS = ["Unknown", "Not Charging", "Charging", "Trickle Charging"]

# variables to be maintained
readingList = [ ]
shortMeanVolts = 0
shortPeakVolts = 0
shortMinVolts = 0
longPeakVolts = 0
longMeanVolts = 0
longMinVolts  = 0
longSDev = 0
shortMeanDuration = 60.0 #seconds
longMeanMultiplier = 5
longMeanDuration = shortMeanDuration * longMeanMultiplier
shortMeanCount = 9
longMeanCount = shortMeanCount * longMeanMultiplier
readingEvery = shortMeanDuration / shortMeanCount
lowBatteryCount = 0
chargingState = 0  # unknown
dtLastChargingStateChange = dt.datetime.now()

def compute(egpg):
    global readingList, chargingState, dtLastChargingStateChange
    global shortMeanVolts,shortPeakVolts,shortMinVolts
    global longMeanVolts,longPeakVolts,longMinVolts,longSDev

    readingList += [egpg.volt()]
    if (len(readingList)>longMeanCount):
      del readingList[0]
      longMeanVolts = np.mean(readingList)
      longPeakVolts = np.max(readingList)
      longMinVolts  = np.min(readingList)
      longSDev      = np.std(readingList)

    shortList = readingList[-5:-1]
    if (len(shortList)>0):
      shortMeanVolts = np.mean(shortList)
      shortPeakVolts = np.max(shortList)
      shortMinVolts  = np.min(shortList)

    lastChargingState = chargingState
    chargingState = chargingStatus()
    if (lastChargingState != chargingState):
        dtLastChargingStateChange = dt.datetime.now()
        print("*** chargingState changed: ",printableCS[chargingState]," ****")
        speak.say("New Charging State"+printableCS[chargingState])

def chargingStatus():
    # https://stackoverflow.com/questions/10048571/python-finding-a-trend-in-a-set-of-numbers?noredirect=1&lq=1

    global UNKNOWN, NOTCHARGING, CHARGING, TRICKLING
    global readingList
    global shortMeanVolts,shortPeakVolts,shortMinVolts
    global longMeanVolts,longPeakVolts,longMinVolts,longSDev
    global chargingState,dtLastChargingStateChange

    shortList = readingList[-9:-1]
    if (len(shortList)>1):
      x = []
      y = shortList

      x.append(range(len(y)))                  # Time Variable
      x.append([1 for ele in xrange(len(y))])  # add intercept, use range in Python3
      y = np.matrix(y).T
      x = np.matrix(x).T
      betas = ((x.T*x).I*x.T*y)
      slope = betas[0,0]
      intercept = betas[1,0]
      print("\nslope: %.4f" % slope)
      chargingValue = chargingState

      if (longMeanVolts > 0):
          if (chargingState == CHARGING):
               if (longMeanVolts > shortMeanVolts):
                   chargingValue = TRICKLING
               else:
                   chargingValue = CHARGING
          elif (chargingState == NOTCHARGING):
               if (slope > 0.01):
                   chargingValue = CHARGING
          elif (chargingState == TRICKLING):
               if (longSDev < 0.2):
                   chargingValue = NOTCHARGING
               else:   # need to set to avoid unknown
                   chargingValue = TRICKLING
          elif (chargingState == UNKNOWN):
               if (slope > 0):
                   chargingValue = CHARGING
          else:
               chargingValue = UNKNOWN
      else:   # just starting up - less than 5 minutes of data
          #if ((shortPeakVolts-shortMeanVolts)>0.5):
          if (chargingState == CHARGING):
               if (slope > -0.1):
                   chargingValue = CHARGING
               elif ((shortPeakVolts - shortMinVolts)>0.3):
                   chargingValue = TRICKLING
               else:
                   chargingValue = NOTCHARGING
          elif (chargingState == UNKNOWN):
               if ( (shortPeakVolts-shortMinVolts)>0.3 ):
                   chargingValue = CHARGING  # or trickling
               else:
                   chargingValue = UNKNOWN
          elif (chargingState == TRICKLING):
               if ((shortPeakVolts - shortMeanVolts) < 0.5):
                   chargingValue = NOTCHARGING
          elif (chargingState == NOTCHARGING):
               if (slope < 0.05):
                   chargingValue = NOTCHARGING
               else:
                   chargingValue = CHARGING
    else:
        chargingValue = UNKNOWN

    return chargingValue

def printValues():
    print ("\nJuicer Values:")
    print ("lastReading %.2f volts" % readingList[-1] )
    print ("num of readings %d" % len(readingList) )
    print ("shortPeakVolts %.3f volts" % shortPeakVolts)
    print ("shortMeanVolts %.3f volts" % shortMeanVolts)
    print ("shortMinVolts  %.3f volts" % shortMinVolts)
    print ("longPeakVolts  %.3f volts" % longPeakVolts)
    print ("longMeanVolts  %.3f volts" % longMeanVolts)
    print ("longMinVolts   %.3f volts" % longMinVolts)
    print ("Charging Status: ", printableCS[chargingStatus()])
    lastChangeInSeconds = (dt.datetime.now() - dtLastChargingStateChange).total_seconds()
    lastChangeDays = divmod(lastChangeInSeconds, 86400)
    lastChangeHours = divmod(lastChangeDays[1], 3600)
    lastChangeMinutes = divmod(lastChangeHours[1], 60)
    lastChangeSeconds = divmod(lastChangeMinutes[1], 1)
    print ("Last Changed: %d days %dh %dm %ds" % (lastChangeDays[0],lastChangeHours[0],lastChangeMinutes[0],lastChangeSeconds[0]) )

def safetyCheck(egpg):
        global batteryLowCount

        LOW_BATTERY_V = 7.1    # 7.1+0.6=7.7 or 0.9625/cell if they are balanced...
        vBatt = egpg.volt()
        if (vBatt < LOW_BATTERY_V):
            batteryLowCount += 1
            print("\nHello? My Battery is getting a little low here.")
        else: batteryLowCount = 0
        if (batteryLowCount > 3):
          speak.say("WARNING, WARNING, SHUTTING DOWN NOW")
          print ("BATTERY %.2f volts BATTERY LOW - SHUTTING DOWN NOW" % vBatt)
          time.sleep(1)
          os.system("sudo shutdown -h now")
          sys.exit(0)

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
            safetyCheck(egpg)
            sleep(readingEvery)

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    egpg.stop()           # stop motors
    	    print("Ctrl-C detected - Finishing up")
    egpg.stop()

if __name__ == "__main__":
	main()
