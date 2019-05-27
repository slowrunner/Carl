#!/usr/bin/env python3
#
# juicerRules.py
#
# USAGE::
#      ./juicerRules.py sim filename    will process <filename> readings simulating juicer.py execution
"""

Rules and Data that maintain Charging Status [UNKNOWN, CHARGING, TRICKLING, NOTCHARGING]
                             Docking Status  [UNKNOWN, DOCKED, NOTDOCKED, DOCKREQUESTED]

This module contains the rules for detecting charging status and charging status changes

"""

# from __future__ import print_function # use python 3 syntax but make it compatible with python 2
# from __future__ import division       #                           ''

import sys
sys.path.append('/home/pi/Carl/plib')
import os
from time import sleep, clock
#import easygopigo3 # import the GoPiGo3 class
import math
#import tiltpan
#import status
#import battery
import numpy as np
import datetime as dt
#import speak
#import myDistSensor
#import lifeLog
#import myconfig
import csv

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
printableDS = ["Unknown", "Not Docked", "Docked", "Manual Dock Requested", "Cabled"]

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
dtNow = dt.datetime.now()
dtStart = dtNow           # change if simulating
dtLastChargingStateChange = dtStart
lastChangeRule = "0" # startup

dockingState = UNKNOWN
dtLastDockingStateChange = dtStart
dockingDistanceInMM = 90  # (measures about 85 to undock position after 90+3mm dismount)
dockingApproachDistanceInMM = 266  # 248 to sign, 266 to wall 
maxApproachDistanceMeasurementErrorInMM = 6  #  +/-5 typical max and min 
dismountFudgeInMM = 3  # results in 248 to CARL sign or 266 to wall after undock 90+3mm
dockingCount = 0
dockingFinalBackInSeconds = 0.125
sim = False


def resetChargingStateToUnknown(dtNow=dt.datetime.now()):
    global readingList,shortMeanVolts,shortPeakVolts,shortMinVolts,longPeakVolts,longMeanVolts,longMinVolts
    global chargingState,dtLastChargingStateChange,lastChangeRule,dtStart

    readingList = [ ]
    shortMeanVolts = 0
    shortPeakVolts = 0
    shortMinVolts = 0
    longPeakVolts = 0
    longMeanVolts = 0
    longMinVolts  = 0
    lastChargingState = chargingState
    chargingState = 0  # unknown
    dtStart = dtNow
    dtLastChargingStateChange = dtStart
    lastChangeRule = "0r" # restart
    print("*** chargingState changed from: ",printableCS[lastChargingState]," to: ", printableCS[chargingState]," ****")
    print("*** by Rule: ",lastChangeRule)
    # speak.whisper("New Charging State"+printableCS[chargingState])

def get_uptime(sim = False, dtNow = None):
    if (sim == True):
        uptime_seconds = (dtNow - dtStart).seconds
        # print ("get_uptime(sim) returning:",uptime_seconds)
    else:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])

    return uptime_seconds

# maintain the datalist
def compute(egpg=None,sim=False,simBattVoltage=None):
    global readingList
    global shortMeanVolts,shortPeakVolts,shortMinVolts
    global longMeanVolts,longPeakVolts,longMinVolts

    if (sim == True):
        readingList += [simBattVoltage]
    else:
        sleep(0.1)
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
      x.append([1 for ele in range(len(y))])  # add intercept, use range in Python3
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
               elif ((shortMeanVolts < 11) and \
                   ((shortPeakVolts - shortMeanVolts) > 0.5) and \
                   ((shortMeanVolts - shortMinVolts) < 0.15) and \
                   (lastChangeInSeconds > 600) and \
                   (slope < 0) ):
                       chargingValue = TRICKLING
                       lastChangeRule = "230b"
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
               if (get_uptime(sim,dtNow) < 240):  # don't try if recently booted
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
        printValues(dtNow)
        chargingState = chargingValue
        dtLastChargingStateChange = dtNow
        print("*** chargingState changed from: ",printableCS[lastChargingState]," to: ", printableCS[chargingState]," ****")
        print("*** by Rule: ",lastChangeRule)
        #speak.whisper("New Charging State"+printableCS[chargingState])

    return chargingValue

def printValues(dtNow=None):
    print ("\nJuicer Values:")
    if (dtNow == None):
        dtNow = dt.datetime.now()
    runTimeInSeconds = (dtNow - dtStart).total_seconds()
    runTimeDays = divmod(runTimeInSeconds, 86400)
    runTimeHours = divmod(runTimeDays[1], 3600)
    runTimeMinutes = divmod(runTimeHours[1], 60)
    print ("JuicerRules Sim Time %d days %dh %dm" % (runTimeDays[0],runTimeHours[0],runTimeMinutes[0]))
    print ("lastReading %.3f volts" % readingList[-1] )
    if (len(readingList) < longMeanCount): print ("num of readings %d" % len(readingList) )
    print ("shortPeakVolts %.3f volts" % shortPeakVolts)
    print ("shortMeanVolts %.3f volts" % shortMeanVolts)
    print ("shortMinVolts  %.3f volts" % shortMinVolts)
    print ("longPeakVolts  %.3f volts" % longPeakVolts)
    print ("longMeanVolts  %.3f volts" % longMeanVolts)
    print ("longMinVolts   %.3f volts" % longMinVolts)
    print ("Charging Status: ", printableCS[chargingState])
    lastChangeInSeconds = (dtNow - dtLastChargingStateChange).total_seconds()
    lastChangeDays = divmod(lastChangeInSeconds, 86400)
    lastChangeHours = divmod(lastChangeDays[1], 3600)
    lastChangeMinutes = divmod(lastChangeHours[1], 60)
    lastChangeSeconds = divmod(lastChangeMinutes[1], 1)
    print ("Last Changed: %d days %dh %dm %ds" % (lastChangeDays[0],lastChangeHours[0],lastChangeMinutes[0],lastChangeSeconds[0]) )
    print ("Last Change Rule: ",lastChangeRule)
    print ("Docking Status: ", printableDS[dockingState])
    print ("Docking Count: ", dockingCount)
    lastDockingChangeInSeconds = (dtNow - dtLastDockingStateChange).total_seconds()
    lastDockingChangeDays = divmod(lastDockingChangeInSeconds, 86400)
    lastDockingChangeHours = divmod(lastDockingChangeDays[1], 3600)
    lastDockingChangeMinutes = divmod(lastDockingChangeHours[1], 60)
    lastDockingChangeSeconds = divmod(lastDockingChangeMinutes[1], 1)
    print ("Last Docking Change: %dh %dm %ds" % (lastDockingChangeHours[0],lastDockingChangeMinutes[0],lastDockingChangeSeconds[0]) )

def safetyCheck(egpg,low_battery_v = 7.6):
        global lowBatteryCount, shortMinVolts, shortMeanVolts


        vBatt = shortMeanVolts
        if (vBatt < low_battery_v):
            lowBatteryCount += 1
            print("\n******** WARNING: Safety Shutdown Is Imminent ******")
            # speak.say("Safety Shutdown Is Imminent.")
        else: lowBatteryCount = 0
        if (lowBatteryCount > 3):
          print("SHORT MIN BATTERY VOLTAGE: %.2f" % shortMinVolts)
          print("SHORT MEAN BATTERY VOLTAGE: %.2f" % shortMeanVolts)
          sleep(1)
          vBatt = egpg.volt()
          # speak.shout("WARNING, WARNING, SHUTTING DOWN NOW")
          print ("BATTERY %.2f volts BATTERY LOW - SHUTTING DOWN NOW" % vBatt)
          print ("Shutdown at ", dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
          sleep(1)
          os.system("sudo shutdown -h now")
          sys.exit(0)

def undock(egpg,ds):
    global dockingDistanceInCM,dockingState,chargingState,dtLastChargingStateChange
    global lastChangeRule,dtLastDockingStateChange

    tiltpan.tiltpan_center()
    distanceForwardInMM = myDistSensor.adjustReadingInMMForError(ds.read_mm())
    if ( (distanceForwardInMM > (dockingDistanceInMM * 2.0)) and \
         (dockingState == DOCKED) ):
         print("\n**** INITIATING DISMOUNT ****")
         # speak.whisper("Initiating dismount.")
         sleep(5)
         distanceForwardInMM = myDistSensor.adjustReadingInMMForError(ds.read_mm())
         if (distanceForwardInMM > (dockingDistanceInMM * 4.0)):
             print("**** Dismounting")
             # speak.whisper("Dismounting")
             egpg.set_speed(150)
             dismountDistanceInCM = (dockingDistanceInMM + dismountFudgeInMM)/10.0
             egpg.drive_cm(dismountDistanceInCM,True)
             dockingState = NOTDOCKED
             dtNow = dt.datetime.now()
             lastChargingState = chargingState
             chargingState = NOTCHARGING
             lastChangeRule = "310c"
             dtLastChargingStateChange = dtNow
             print("*** chargingState changed from: ",printableCS[lastChargingState]," to: ", printableCS[chargingState]," ****")
             print("*** by Rule: ",lastChangeRule)
             # speak.whisper("New Charging State"+printableCS[chargingState])
             print("**** DISMOUNT COMPLETE AT ", dtNow.strftime("%Y-%m-%d %H:%M:%S") )
             # speak.whisper("Dismount complete")

             # assumption juicer.py always starts docked.
             lastDockingChangeInSeconds = (dtNow - dtLastDockingStateChange).total_seconds()
             lastDockingChangeDays = divmod(lastDockingChangeInSeconds, 86400)
             lastDockingChangeHours = round( (lastDockingChangeDays[1] / 3600.0),1)
             #print("lastDockingChangeDays:",lastDockingChangeDays)
             #print("lastDockingChangeHours:",lastDockingChangeHours)
             strToLog = "---- Dismount {0} at {1:.1f} v after {2:.1f} h".format( (dockingCount+1),shortMeanVolts, lastDockingChangeHours)
             #lifeLog.logger.info(strToLog)

             dtLastDockingStateChange = dtNow


         else:
             print("**** DISMOUNT BLOCKED by object at: %.0f inches" % (distanceForwardInMM / 25.4) )
             # speak.say("Dismount blocked")

    elif ( dockingState == CABLED ):
             print("**** Please DISCONNECT CABLE ****")
             # speak.say("Please disconnect cable.")
    else:
        print("**** UNABLE TO UNDOCK ****")
        # speak.say("Unable to undock.")

    tiltpan.off()
    # exit undock

def dock(egpg,ds):
    global dockingApproachDistanceInCM,dockingState,dockingDistanceInCM,dockingCount,dtLastDockingStateChange

    print("\n**** DOCKING REQUESTED ****")

    if (dockingState != NOTDOCKED):
        print("**** ERROR: Docking request when not undocked")
        return

    tiltpan.tiltpan_center()
    distanceReadings = []
    for x in range(6):
        sleep(0.2)
        distanceReadings += [ds.read_mm()]
    # print("**** Distance Readings:",distanceReadings)
    distanceForwardInMM = myDistSensor.adjustReadingInMMForError(np.average(distanceReadings))
    print("**** Current  Distance is %.1f mm %.2f in" % (distanceForwardInMM, distanceForwardInMM / 25.4))
    print("**** Approach Distance is %.2f mm" % dockingApproachDistanceInMM )
    appErrorInMM = distanceForwardInMM - dockingApproachDistanceInMM
    if ( -20 <  appErrorInMM > 20 ):
        print("**** DOCK APPROACH ERROR - REQUEST MANUAL PLACEMENT ON DOCK ****")
        # speak.say("Dock approach error. Please put me on the dock")
        # lifeLog.logger.info("**** Dock Approach Error - MANUAL DOCKING REQUESTED")
        dockingState = DOCKREQUESTED
        dtLastDockingStateChange = dt.datetime.now()
        if (  appErrorInMM > 0):
            print("**** Approach Distance too large by %.2f MM" % appErrorInMM)
        else:
            print("**** Approace Distance too small by %.2f MM" % appErrorInMM)
        sleep(5)
    elif ( (dockingState == NOTDOCKED) ):
        print("\n**** INITIATING DOCK MOUNTING SEQUENCE ****")
        # speak.whisper("Initiating dock mounting sequence.")
        sleep(5)
        print("**** TURNING 180")
        # speak.whisper("Turning one eighty.")
        egpg.set_speed(150)
        egpg.orbit(180)
        print("**** Preparing to Back onto dock")
        # speak.whisper("Preparing to back onto dock.")
        sleep(5)
        # leave maxApproachDistanceMeasurementInMM to back manually
        backingDistanceInCM =  -1.0 * (dockingDistanceInMM + appErrorInMM -maxApproachDistanceMeasurementErrorInMM ) / 10.0
        print("**** BACKING ONTO DOCK %.0f mm" % (backingDistanceInCM * 10.0))
        # speak.whisper("Backing onto dock")
        egpg.drive_cm( backingDistanceInCM,True)
        sleep(1)
        print("**** Backing for a bit to account for measurement errors")
        egpg.backward()
        sleep(dockingFinalBackInSeconds)
        egpg.stop()
        sleep(1)
        print("**** Backing again just to be sure we're good")
        egpg.backward()
        sleep(dockingFinalBackInSeconds)
        egpg.stop()

        dtNow = dt.datetime.now()
        print("**** DOCKING COMPLETE AT ", dtNow.strftime("%Y-%m-%d %H:%M:%S") )
        # speak.whisper("Docking completed.")
        dockingState = DOCKED
        dockingCount += 1
        lastDockingChangeInSeconds = (dtNow - dtLastDockingStateChange).total_seconds()
        lastDockingChangeDays = divmod(lastDockingChangeInSeconds, 86400)
        lastDockingChangeHours = round( (lastDockingChangeDays[1] / 3600.0),1)
        strToLog = "---- Docking {0} completed  at {1:.1f} v after {2:.1f} h".format( dockingCount,shortMeanVolts,lastDockingChangeHours)
        # lifeLog.logger.info(strToLog)
        dtLastDockingStateChange = dtNow
        sleep(5)
    else:
        print("\n**** UNKNOWN DOCKING ERROR ****")
        # speak.say("Unknown docking error.")
        sleep(5)

    tiltpan.off()
    # exit dock()

def dockingTest(egpg,ds,numTests = 30):
    global dockingState,chargingState

    print("\n**** DOCKING TEST INITIATED ****")
    print("checking battery level")
    while (longMeanVolts == 0):
        compute(egpg)
        chargingStatus()
    print("shortMeanVolts: %.2f" % shortMeanVolts)

    # DOCKING TEST LOOP
    for x in range(numTests):
        print("\n****************************")
        print("     DOCKING TEST CYCLE: ",x)
        dockingState = DOCKED
        chargingState = TRICKLING
        lastChangeRule = "Testing"
        dtLastChargingStateChange = dt.datetime.now()
        print("Docking State:", printableDS[dockingState])
        # speak.whisper("Docking state is "+printableDS[dockingState])
        print("Charging State:", printableCS[chargingState])
        # speak.whisper("Charging State is "+printableCS[chargingState])
        if (shortMeanVolts > 8.75):
            undock(egpg,ds)
            print("Status after undock()")
            print("Docking State:", printableDS[dockingState])
            # speak.whisper("Docking state is "+printableDS[dockingState])
            print("Charging State:", printableCS[chargingState])
            # speak.whisper("Charging State is "+printableCS[chargingState])
            sleep(5)

            if (dockingState == NOTDOCKED):
                print("\n**** DOCKING APPROACH INITIATED")
                action = "Turning around to be at approach point"
                print(action)
                # speak.whisper(action)
                egpg.orbit(180)
                sleep(5)


                dock(egpg,ds)
                print("Status after dock()")
                print("Docking State:", printableDS[dockingState])
                # speak.whisper("Docking state is "+printableDS[dockingState])
                resetChargingStateToUnknown()
                print("checking battery level")
                while (longMeanVolts == 0):
                    compute(egpg)
                    chargingStatus()
                print("Charging State:", printableCS[chargingState])
                # speak.whisper("Charging State is "+printableCS[chargingState])
                print("I'm thirsty.  I'll be here a while.")
                # speak.whisper("I'm thirsty.  I'll be here a while.")
                sleep(5)
        else:
            print("\n**** shortMeanVolts %.2f insufficient" % shortMeanVolts)
            print("SLEEPING FOR 10 MINUTES\n")
            sleep(600)


def main():
    global dockingState,chargingState,dtLastDockingStateChange,sim

    # lifeLog.logger.info("Started")

    # ./juicerRules.py sim filename  SIMULATION
    sim = False
    if (len(sys.argv)>1):
        if (sys.argv[1] == "sim"):
            if (len(sys.argv)>2):
                simFilename = sys.argv[2]
                sim = True
            else:
                print("USAGE: ./juiceRules.py sim <filename>")
                exit(0)


    if (sim != True):
        print("USAGE: ./juiceRules.py sim <filename>")
        exit(0)
    else:
       egpg = None
       


    print ("JuicerRules SIMULATION  Main Initialization")
    print ("shortMeanDuration: %.1f" % shortMeanDuration)
    print ("longMeanDuration: %.1f" % longMeanDuration)
    print ("readingEvery %.1f seconds" % readingEvery)
    print ("simulation: ",sim)

    try:
        if sim:
            fdata = open(simFilename)
            freader = csv.reader(fdata)
            header_row = next(freader)
            # print("Sim Data Header",header_row)
            loopSleep = 0.005
            printEvery = 10000
        else:  
            loopSleep = readingEvery
            printEvery = 5 


        #  loop
        readingCount = 0
        
        for row in freader:
            readingCount += 1
            dtNow = dt.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            vBattNow = float(row[1])
            if (readingCount == 1):  
                resetChargingStateToUnknown(dtNow)
                dtLastDockingStateChange = dtNow
            compute(egpg,sim,vBattNow)
            chargingStatus(dtNow)
            if ((readingCount % printEvery) == 1 ):
                # status.printStatus(egpg,ds)
                printValues(dtNow)

            """
            safetyCheck(egpg)
            # Detect when docked
            if (((dockingState == UNKNOWN) or \
                 (dockingState == DOCKREQUESTED) or \
                 (dockingState == NOTDOCKED)) and \
                ((chargingState == TRICKLING) or \
                 (chargingState == CHARGING)) ):
                dockingState = DOCKED
                dtLastDockingStateChange = dt.datetime.now()
            # Starting up away from dock
            if ((dockingState == UNKNOWN) and \
                 (chargingState == NOTCHARGING) ):
                dockingState = NOTDOCKED
                dtLastDockingStateChange = dt.datetime.now()
            # Time to go out to play
            if ((chargingState == TRICKLING) and \
               (dockingState == DOCKED)):
                print("\n**** Time to get off the pot")
                undock(egpg,ds)
            # End of play time
            if ((chargingState == NOTCHARGING) and \
                (dockingState == NOTDOCKED) and \
                (shortMeanVolts < 8.5) ):
                print("\n**** Time to get on the pot")
                action = "**** Turning around to be at approach point"
                print(action)
                # speak.whisper(action)
                egpg.orbit(180)
                sleep(5)
                dock(egpg,ds)
            # Detect docking that didn't align contacts well - need to undock/dock
            if ((dockingState == DOCKED) and \
                ((chargingState == UNKNOWN) or \
                 (chargingState == NOTCHARGING)) and \
                ( (dt.datetime.now() - dtLastDockingStateChange).total_seconds() > 180) ):
                print("\n**** Docking Failure Possible, undocking")
                # speak.say("Docking Failure Possible, undocking.")
                lifeLog.logger.info("---- Docking Failure Possible")
                undock(egpg,ds)
            # False detection of Trickling as Charging - need to undock/dock
            if ((dockingState == DOCKED) and \
                (chargingState == CHARGING) and \
                (shortMeanVolts < 8.75) and \
                ( (dt.datetime.now() - dtLastDockingStateChange).total_seconds() > 120) ):
                print("\n**** Charger Trickling, Need Charging Possible, undocking")
                # speak.say("Charger Trickling, I Need A Real Charge. Undocking.")
                lifeLog.logger.info("---- Docking Failure Possible. Trickling, Need Charging")
                undock(egpg,ds)

            """
            sleep(loopSleep)

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    # egpg.stop()           # stop motors
            print("Ctrl-C detected - Finishing up")
            sleep(1)
    #egpg.stop()

if __name__ == "__main__":
	main()
