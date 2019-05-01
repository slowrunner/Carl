#!/usr/bin/env python
#
# juiceRules
"""
Rules and Data that maintain Charging Status [UNKNOWN, CHARGING, TRICKLING, NOTCHARGING]

This module contains the rules for detecting charging status and charging status changes

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
import myDistSensor

# constants
UNKNOWN = 0
NOTCHARGING = 1   # disconnected 
CHARGING    = 2   # charging 
TRICKLING   = 3   # Trickle charging (less than load)
printableCS = ["Unknown", "Not Charging", "Charging", "Trickle Charging"]

NOTDOCKED = 1
DOCKED = 2
DOCKREQUESTED = 3
CABLED = 4
printableDS = ["Unknown", "Not Docked", "Docked", "Cable Requested", "Cabled"]

# variables to be maintained
readingList = [ ]
shortMeanVolts = 0
shortPeakVolts = 0
shortMinVolts = 0
longPeakVolts = 0
longMeanVolts = 0
longMinVolts  = 0
shortMeanDuration = 60.0 #seconds
longMeanMultiplier = 5     # six minutes
longMeanDuration = shortMeanDuration * longMeanMultiplier
shortMeanCount = 30
longMeanCount = shortMeanCount * longMeanMultiplier
readingEvery = shortMeanDuration / shortMeanCount
lowBatteryCount = 0
chargingState = 0  # unknown
dtLastChargingStateChange = dt.datetime.now()
lastChangeRule = "0" # startup

dockingState = UNKNOWN
dockingDistanceInMM = 87  # 89 = 3.5 * 25.4
dockingApproachDistanceInMM = 264 # 260 = 10.25 * 25.4
dismountFudgeInMM = 3  # 4 gave 266 ave dist and 30 good dockings
dockingCount = 0

def get_uptime(sim = False,simUptimeInSec = 300):
    if (sim == True):
        uptime_seconds = simUptimeInSec
        print ("get_uptime(sim) returning:",uptime_seconds)
    else:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])

    return uptime_seconds

# maintain the datalist
def compute(egpg=None,sim=False,simBattVoltage=10.5):
    global readingList
    global shortMeanVolts,shortPeakVolts,shortMinVolts
    global longMeanVolts,longPeakVolts,longMinVolts

    if (sim == True):
        readingList += [simBattVoltage]
    else:
        sleep(1)
        readingList += [egpg.volt()]
    # print("debug: lastReading: %.3f" % readingList[-1])
    if (len(readingList)>longMeanCount):
      del readingList[0]
#      print("readingList:",readingList)
#      print("readingList[:-shortMeanCount]:",readingList[:-shortMeanCount])
      longMeanVolts = np.mean(readingList)
      longPeakVolts = np.max(readingList[:-shortMeanCount])  #max and min not include shortlist
      longMinVolts  = np.min(readingList[:-shortMeanCount])

    if (len(readingList)>shortMeanCount):
        shortList = readingList[-shortMeanCount:]
    else:
        shortList = readingList

    # print("debug: readingList:",readingList)
    # print("debug: shortList:",shortList)

    if (len(shortList)>0):
      shortMeanVolts = np.mean(shortList)
      shortPeakVolts = np.max(shortList)
      shortMinVolts  = np.min(shortList)

def chargingStatus(dtNow=None):
    # https://stackoverflow.com/questions/10048571/python-finding-a-trend-in-a-set-of-numbers?noredirect=1&lq=1

    global UNKNOWN, NOTCHARGING, CHARGING, TRICKLING
    global readingList
    global shortMeanVolts,shortPeakVolts,shortMinVolts
    global longMeanVolts,longPeakVolts,longMinVolts
    global chargingState,dtLastChargingStateChange,lastChangeRule

#    shortList = readingList[-shortMeanCount:]
    # print("debug: shortlist =",shortList)

#    if (len(shortList)>1):
    if (len(readingList)>1):
      x = []
#      y = shortList
      y= readingList

      x.append(range(len(y)))                  # Time Variable
      x.append([1 for ele in xrange(len(y))])  # add intercept, use range in Python3
      y = np.matrix(y).T
      x = np.matrix(x).T
      betas = ((x.T*x).I*x.T*y)
      slope = betas[0,0]
      intercept = betas[1,0]
      # print("\nslope: %.4f" % slope)
      chargingValue = chargingState
      if (dtNow == None):
          dtNow = dt.datetime.now()
      lastChangeInSeconds = (dtNow - dtLastChargingStateChange).total_seconds()


      if (longMeanVolts > 0):
          if (chargingState == CHARGING):
               if ((longPeakVolts > 12) and \
                   ((longMeanVolts - shortMeanVolts) > 0.5) and \
                   (longMinVolts >= shortMinVolts) and \
                   (lastChangeInSeconds > 300) and \
                   (slope < 0) ):
                       chargingValue = TRICKLING
                       lastChangeRule = "230"
               elif ((longPeakVolts > 11.5) and \
                   ((longMeanVolts - shortMeanVolts) > 0.5) and \
                   (longMinVolts >= shortMinVolts) and \
                   (lastChangeInSeconds > 300) and \
                   (slope < 0) ):
                       chargingValue = TRICKLING
                       lastChangeRule = "230a"
               elif (((shortPeakVolts - shortMinVolts) < 0.07) and \
                   (longPeakVolts < 11.5) and \
                   ((longPeakVolts - longMinVolts) < 0.25) and \
                   (longMeanVolts > shortMeanVolts) and \
                   (lastChangeInSeconds > 120) and \
                   (slope < 0) ):
                       chargingValue = NOTCHARGING
                       lastChangeRule = "210"
               else:  # no change
                   pass
          elif (chargingState == NOTCHARGING):
               if ((slope > 0) and \
                   (lastChangeInSeconds > 150) and \
                   (shortMeanVolts > longMeanVolts) and \
                   (shortPeakVolts >= longPeakVolts) and \
                   ((shortPeakVolts - shortMinVolts)>0.5) ):
                   chargingValue = CHARGING
                   lastChangeRule = "120"
               else:
                   pass
          elif (chargingState == TRICKLING):
               if (((shortPeakVolts - shortMeanVolts) < 0.035) and \
                   (longPeakVolts < 10.5) and \
                   ((longPeakVolts - longMeanVolts) < 0.075) and \
#                   ((longPeakVolts - longMinVolts) < 0.5) and \
                   (longMeanVolts > shortMeanVolts) and \
                   (lastChangeInSeconds > 120) and \
                   (slope < 0) ):
                       chargingValue = NOTCHARGING
                       lastChangeRule = "310"
               elif (((shortPeakVolts - shortMeanVolts) < 0.1) and \
                   ((longPeakVolts - longMeanVolts) < 0.2) and \
                   (longMeanVolts > shortMeanVolts) and \
                   (lastChangeInSeconds > 120) and \
                   (slope < 0) ):
                       chargingValue = NOTCHARGING
                       lastChangeRule = "310a"
               else:   # no change
                   pass
          elif (chargingState == UNKNOWN):
               if ( (shortPeakVolts >= longPeakVolts) and \
                    (shortMeanVolts > longMeanVolts) and \
                    (slope > 0.02) and \
                    (lastChangeInSeconds > 60) ):
                   chargingValue = CHARGING
                   lastChangeRule = "420"
               elif ( ((longPeakVolts - longMinVolts) < 0.15) and \
                      (longMeanVolts > shortMeanVolts) and \
                      ((shortPeakVolts - shortMinVolts) < 0.07) and \
                      (slope < 0) and \
                      (lastChangeInSeconds > 120) ):
                          chargingValue = NOTCHARGING
                          lastChangeRule = "410"
          else:
              pass
      else:   # just starting up - less than 5 minutes of data
          if (chargingState == UNKNOWN):
               if (get_uptime() < 240):  # don't try if recently booted
                   lastChangeRule = "44a"
               elif ( (shortMeanVolts < 11) and \
                      ((shortPeakVolts-shortMeanVolts)>0.5) and \
                      ((shortMeanVolts-shortMinVolts)<0.15) and \
                      (lastChangeInSeconds > 60) and \
                      (slope < 0) ):
                        chargingValue = TRICKLING
                        lastChangeRule = "43"
               elif ( ((shortMeanVolts-shortMinVolts)>0.5) and \
                      (slope > 0)  and \
                      (lastChangeInSeconds>45)):
                        chargingValue = CHARGING
                        lastChangeRule = "42b"
               elif ( (shortMeanVolts > 11) and \
                      (lastChangeInSeconds>60) and \
                      (slope > 0) ):
                   chargingValue = CHARGING
                   lastChangeRule = "42a"
               else:
                   pass
    else:  # only one reading so far
        chargingValue = UNKNOWN
        lastChangeRule = "44b"

    # check if changed from last time checked
    lastChargingState = chargingState
    if (lastChargingState != chargingValue):
        chargingState = chargingValue
        dtLastChargingStateChange = dtNow
        print("*** chargingState changed from: ",printableCS[lastChargingState]," to: ", printableCS[chargingState]," ****")
        print("*** by Rule: ",lastChangeRule)
        speak.say("New Charging State"+printableCS[chargingState])

    return chargingValue

def printValues():
    print ("\nJuicer Values:")
    print ("lastReading %.3f volts" % readingList[-1] )
    print ("num of readings %d" % len(readingList) )
    print ("shortPeakVolts %.3f volts" % shortPeakVolts)
    print ("shortMeanVolts %.3f volts" % shortMeanVolts)
    print ("shortMinVolts  %.3f volts" % shortMinVolts)
    print ("longPeakVolts  %.3f volts" % longPeakVolts)
    print ("longMeanVolts  %.3f volts" % longMeanVolts)
    print ("longMinVolts   %.3f volts" % longMinVolts)
    print ("Charging Status: ", printableCS[chargingState])
    lastChangeInSeconds = (dt.datetime.now() - dtLastChargingStateChange).total_seconds()
    lastChangeDays = divmod(lastChangeInSeconds, 86400)
    lastChangeHours = divmod(lastChangeDays[1], 3600)
    lastChangeMinutes = divmod(lastChangeHours[1], 60)
    lastChangeSeconds = divmod(lastChangeMinutes[1], 1)
    print ("Last Changed: %d days %dh %dm %ds" % (lastChangeDays[0],lastChangeHours[0],lastChangeMinutes[0],lastChangeSeconds[0]) )
    print ("Last Change Rule: ",lastChangeRule)
    print ("Docking Status: ", printableDS[dockingState])
    print ("Docking Count: ", dockingCount)

def safetyCheck(egpg,low_battery_v = 7.6):
        global batteryLowCount, shortMinVolts, shortMeanVolts

        #7.1  
        vBatt = shortMeanVolts
        if (vBatt < low_battery_v):
            batteryLowCount += 1
            print("\n******** WARNING: Safety Shutdown Is Imminent ******")
            speak.say("Safety Shutdown Is Imminent.")
        else: batteryLowCount = 0
        if (batteryLowCount > 3):
          print("SHORT MIN BATTERY VOLTAGE: %.2f" % shortMinVolts)
          print("SHORT MEAN BATTERY VOLTAGE: %.2f" % shortMeanVolts)
          sleep(1)
          vBatt = egpg.volt()
          speak.say("WARNING, WARNING, SHUTTING DOWN NOW")
          print ("BATTERY %.2f volts BATTERY LOW - SHUTTING DOWN NOW" % vBatt)
          sleep(1)
          os.system("sudo shutdown -h now")
          sys.exit(0)

def undock(egpg,ds):
    global dockingDistanceInCM,dockingState,chargingState,dtLastChargingStateChange
    global lastChangeRule

    tiltpan.tiltpan_center()
    distanceForwardInMM = myDistSensor.adjustForAveErrorInMM(ds.read_mm())
    if ( (distanceForwardInMM > (dockingDistanceInMM * 2.0)) and \
         (dockingState == DOCKED) ):
         print("\n**** INITIATING DISMOUNT ****")
         speak.say("Initiating dismount.")
         sleep(5)
         distanceForwardInMM = myDistSensor.adjustForAveErrorInMM(ds.read())
         if (distanceForwardInMM > (dockingDistanceInMM * 2.0)):
             print("**** Dismounting")
             speak.say("Dismounting")
             egpg.set_speed(150)
             dismountDistanceInCM = (dockingDistanceInMM + dismountFudgeInMM)/10.0
             egpg.drive_cm(dismountDistanceInCM,True)
             dockingState = NOTDOCKED
             lastChargingState = chargingState
             chargingState = NOTCHARGING
             lastChangeRule = "310c"
             dtLastChargingStateChange = dt.datetime.now()
             print("*** chargingState changed from: ",printableCS[lastChargingState]," to: ", printableCS[chargingState]," ****")
             print("*** by Rule: ",lastChangeRule)
             speak.say("New Charging State"+printableCS[chargingState])


             print("**** DISMOUNT COMPLETE ")
             speak.say("Dismount complete")
         else:
             print("**** DISMOUNT BLOCKED by object at: %.0f inches" % (distanceForwardInMM / 25.4) )
             speak.say("Dismount blocked")

    elif ( dockingState == CABLED ):
             print("**** Please DISCONNECT CABLE ****")
             speak.say("Please disconnect cable.")
    else:
        print("**** UNABLE TO UNDOCK ****")
        speak.say("Unable to undock.")


def dock(egpg,ds):
    global dockingApproachDistanceInCM,dockingState,dockingDistanceInCM,dockingCount

    print("\n**** DOCKING REQUESTED ****")

    if (dockingState != NOTDOCKED):
        print("**** ERROR: Docking request when not undocked")
        return

    tiltpan.tiltpan_center()
    distanceReadings = []
    for x in range(6):
        sleep(0.2)
        distanceReadings += [myDistSensor.adjustForAveErrorInMM(ds.read_mm())]
    print("**** Distance Readings:",distanceReadings)
    distanceForwardInMM = np.average(distanceReadings)
    print("**** Current  Distance is %.1f mm %.2f in" % (distanceForwardInMM, distanceForwardInMM / 25.4))
    print("**** Approach Distance is %.2f mm" % dockingApproachDistanceInMM )

    appErrorInMM = distanceForwardInMM - dockingApproachDistanceInMM
    if ( -20 <  appErrorInMM > 20 ):
        print("**** DOCK APPROACH ERROR - REQUEST MANUAL PLACEMENT ON DOCK ****")
        speak.say("Dock approach error. Please put me on the dock")
        dockingState = DOCKREQUESTED
        if (  appErrorInMM > 0):
            print("**** Approach Distance too large by %.2f MM" % appErrorInMM)
        else:
            print("**** Approace Distance too small by %.2f MM" % appErrorInMM)
        sleep(5)
    elif ( (dockingState == NOTDOCKED) ):
        print("\n**** INITIATING DOCK MOUNTING SEQUENCE ****")
        speak.say("Initiating dock mounting sequence.")
        sleep(5)
        print("**** TURNING 180")
        speak.say("Turning one eighty.")
        egpg.set_speed(150)
        egpg.orbit(180)
        print("**** Preparing to Back")
        print("Preparing to back onto dock.")
        sleep(5)
        backingDistanceInCM =  -1.0 * (dockingDistanceInMM + appErrorInMM / 1.5) / 10.0
        print("**** BACKING ONTO DOCK %.0f mm" % (backingDistanceInCM * 10.0))
        speak.say("Backing onto dock")
        egpg.drive_cm( backingDistanceInCM,True)
        print("**** DOCKING COMPLETED ****")
        speak.say("Docking completed.")
        dockingState = DOCKED
        dockingCount += 1
        sleep(5)
    else:
        print("\n**** UNKNOWN DOCKING ERROR ****")
        speak.say("Unknown docking error.")
        sleep(5)

def dockingTest(egpg,ds):
    global dockingState,chargingState

    # DOCKING TEST LOOP
    for x in xrange(30):
        print("\n****************************")
        print("     DOCKING TEST CYCLE: ",x)
        dockingState = DOCKED
        chargingState = TRICKLING
        print("Docking State:", printableDS[dockingState])
        speak.say("Docking state is "+printableDS[dockingState])
        print("Charging State:", printableCS[chargingState])
        speak.say("Charging State is "+printableCS[chargingState])
        undock(egpg,ds)
        print("Docking State:", printableDS[dockingState])
        speak.say("Docking state is "+printableDS[dockingState])
        print("Charging State:", printableCS[chargingState])
        speak.say("Charging State is "+printableCS[chargingState])

        sleep(5)
        action = "Turning around to be at approach point"
        print(action)
        speak.say(action)
        egpg.orbit(182)
        sleep(5)
        chargingState = NOTCHARGING
        print("Docking State:", printableDS[dockingState])
        speak.say("Docking state is "+printableDS[dockingState])
        print("Charging State:", printableCS[chargingState])
        speak.say("Charging State is "+printableCS[chargingState])


        dock(egpg,ds)
        print("Docking State:", printableDS[dockingState])
        speak.say("Docking state is "+printableDS[dockingState])
        chargingState = UNKNOWN
        print("Charging State:", printableCS[chargingState])
        speak.say("Charging State is "+printableCS[chargingState])
        sleep(5)
        print("I'm thirsty.  I'll be here a while.")
        speak.say("I'm thirsty.  I'll be here a while.")
        sleep(5)


def main():
    global dockingState,chargingState

    sim = False
    if (sim != True):
       egpg = easygopigo3.EasyGoPiGo3(use_mutex=True) # Create an instance of the EasyGoPiGo3 class
       ds = egpg.init_distance_sensor()
       ts = egpg.init_servo(tiltpan.TILT_PORT)
       ps = egpg.init_servo(tiltpan.PAN_PORT)
       tiltpan.tiltpan_center()
    else:
       egpg = None

    # uncomment to perform 10 undock/docks 
    dockingTest(egpg,ds)

    print ("Juicer Main Initialization")
    print ("shortMeanDuration: %.1f" % shortMeanDuration)
    print ("longMeanDuration: %.1f" % longMeanDuration)
    print ("readingEvery %.1f seconds" % readingEvery)
    print ("simulation: ",sim)



    try:
        #  loop
        loopCount = 0
        while True:
            loopCount += 1
            compute(egpg)
            chargingStatus()
            if ((loopCount % 5) == 1 ):
                status.printStatus(egpg,ds)
                printValues()
            safetyCheck(egpg)
            if ((dockingState == UNKNOWN) and \
                ((chargingState == TRICKLING) or \
                 (chargingState == CHARGING)) ):
                dockingState = DOCKED
            if ((dockingState == UNKNOWN) and \
                 (chargingState == NOTCHARGING) ):
                dockingState = NOTDOCKED
            if ((chargingState == TRICKLING) and \
               (dockingState == DOCKED)):
                print("Time to get off the pot")
                undock(egpg,ds)
            if ((chargingState == NOTCHARGING) and \
                (dockingState == NOTDOCKED) and \
                (shortMeanVolts < 8.1) ):
                print("Time to get on the pot")
                action = "Turning around to be at approach point"
                print(action)
                speak.say(action)
                egpg.orbit(182)
                sleep(5)
                dock(egpg,ds)

            sleep(readingEvery)

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    egpg.stop()           # stop motors
    	    print("Ctrl-C detected - Finishing up")
    egpg.stop()

if __name__ == "__main__":
	main()
