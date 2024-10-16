#!/usr/bin/env python3
#
# juicer.py
#
# USAGE::
#      ./juicer.py        will undock when trickle charging, will dock at PLAYTIME_LIMITv
#      ./juicer.py test   will perform 5 undock-dockings (start on dock)
"""

Rules and Data that maintain Charging Status [UNKNOWN, CHARGING, TRICKLING, NOTCHARGING]
                             Docking Status  [UNKNOWN, DOCKED, NOTDOCKED, DOCKREQUESTED]

This module contains the rules for detecting charging status and charging status changes

Physical Aspects:
	-------		Wall

	 120mm

	  ___		Docking Back stop
	   o		Skid Ball


	 280mm		Dismount Drive and docking backup distance


	   o		Skid after dismount

	 ~50mm

	  _-_		Distance Sensor at approach point (444 - 450mm or so)

	  75mm

	|     |		Wheels at approach point (and after dismount)

"""

# from __future__ import print_function # use python 3 syntax but make it compatible with python 2
# from __future__ import division       #                           ''

import sys
# sys.path.append('/home/pi/Carl/plib')
sys.path.insert(1,'/home/pi/Carl/plib')   # will use plib version of easygopigo3 and gopigo3
import os
from time import sleep, clock
import easygopigo3 # import the EasyGoPiGo3 class from plib to get timeout in drive_cm
# import my_easygopigo3 as easygopigo3 # import the GoPiGo3 class
import math
import tiltpan
import status
import battery
import numpy as np
import datetime as dt
import speak
import myDistSensor
import lifeLog
import myconfig
import carlDataJson as cd
import runLog


# constants
PLAYTIME_LIMIT = 8.1
CONDITIONING_LIMIT = 7.7
SHUTDOWN_LIMIT = 7.4
DOCKING_TEST_LIMIT = 8.75

UNKNOWN = 0
NOTCHARGING = 1   # disconnected
CHARGING    = 2   # charging
TRICKLING   = 3   # Trickle charging (less than load)
printableCS = ["Unknown", "Not Charging", "Charging", "Trickle Charging"]

NOTDOCKED = 1
DOCKED = 2
DOCKREQUESTED = 3
UNDOCKREQUESTED = 4
CABLED = 5
printableDS = ["Unknown", "Not Docked", "Docked", "Manual Dock Requested", "Manual UnDock Requested", "Cabled"]

# variables to be maintained
readingList = [ ]
shortMeanVolts = 0
shortPeakVolts = 0
shortMinVolts = 0
longPeakVolts = 0
longMeanVolts = 0
longMinVolts  = 0
shortMeanDuration = 60.0 #seconds
longMeanMultiplier = 5     # five minutes
longMeanDuration = shortMeanDuration * longMeanMultiplier
shortMeanCount = 30
longMeanCount = shortMeanCount * longMeanMultiplier
readingEvery = shortMeanDuration / shortMeanCount
lowBatteryCount = 0
chargingState = 0  # unknown
dtStart = dt.datetime.now()
dtLastChargingStateChange = dtStart
lastChangeRule = "0" # startup

dockingState = UNKNOWN
dtLastDockingStateChange = dtStart
# Distance from rear castor docked position to rear castor undocked position
dockingDistanceInMM = 280 # 90  # (measures about 85 to undock position after 90+3mm dismount)
dockingApproachDistanceInMM = 444 # 375 # 263  # 263 to sign, 266 to wall
allowedApproachErrorInMM = 50  # 2/2021 was 20  +/- band around target approach distance
# Next value is subrtracted from backing distance to allaw drive_cm to always be short a little
maxApproachDistanceMeasurementErrorInMM = 7  #  was 6, +/-5 typical max and min
dismountFudgeInMM = 3  # results in 248 to CARL sign or 266 to wall after undock 90+3mm
dismountBlockedInMM = dockingApproachDistanceInMM # 375  # 270 mm minimum 
possibleEarlyTrickleVolts = 0    # voltage first detect possible early trickling
maxChargeTime = (4 * 60 * 60)    # was 3.5h on Tenergy 1025 - trying 4.0h for Tenergy 1005 0.9A setting


# load chargeConditioning and chargeCycles/dockingCount
# Not loading chargingState and dockingState 
def loadVars():
    global chargeCycles, dockingCount, chargeConditioning, chargingState, dockingState

    try:
        chargeCycles = int(cd.getCarlData('chargeCycles'))
        dockingCount = chargeCycles
        print("loaded chargeCycles and dockingCount from carlData.json")
    except:
        dockingCount = 0
        chargeCycles = 0
        print("init dockingCount and chargeCycles to 0/Unknown")

    try:
        chargeConditioning = int(cd.getCarlData('chargeConditioning'))
        print("loaded chargeConditioning from carlData.json")
    except:
        chargeConditioning = 0
        print("init chargeConditioning to 0")

    """
    try:
        chargingState = int(cd.getCarlData('chargingState'))
        print("loaded chargingState from carlData.json")
    except:
        chargingState = 0
        cd.saveCarlData('chargingState',chargingState)
        print("init carlData chargingState to 0 UNKNOWN")

    try:
        dockingState = int(cd.getCarlData('dockingState'))
        print("loaded dockingState from carlData.json")
    except:
        dockingState = 0
        cd.saveCarlData('dockingState', dockingState)
        print("init carlData dockingState to 0 UNKNOWN")
    """

dockingFinalBackInSeconds = 0.125

def resetChargingStateToUnknown():
    global readingList,shortMeanVolts,shortPeakVolts,shortMinVolts,longPeakVolts,longMeanVolts,longMinVolts
    global chargingState,dtLastChargingStateChange,lastChangeRule,possibleEarlyTrickleVolts

    readingList = [ ]
    shortMeanVolts = 0
    shortPeakVolts = 0
    shortMinVolts = 0
    longPeakVolts = 0
    longMeanVolts = 0
    longMinVolts  = 0
    lastChargingState = chargingState
    chargingState = 0  # unknown
    dtNow = dt.datetime.now()
    dtLastChargingStateChange = dtNow
    lastChangeRule = "0r" # restart
    currentPrintableChargingState = printableCS[chargingState]
    print("*** ",dtNow.strftime("%H:%M:%S")," chargingState changed from: ",printableCS[lastChargingState]," to: ", currentPrintableChargingState, " ****")
    print("*** by Rule: ",lastChangeRule)
    speak.whisper("New Charging State"+currentPrintableChargingState)
    cd.saveCarlData('chargingState',chargingState)
    possibleEarlyTrickleVolts = 0

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

    # global UNKNOWN, NOTCHARGING, CHARGING, TRICKLING
    global readingList
    global shortMeanVolts,shortPeakVolts,shortMinVolts
    global longMeanVolts,longPeakVolts,longMinVolts
    global chargingState,dtLastChargingStateChange,lastChangeRule
    global chargeCycles, possibleEarlyTrickleVolts
    global dockingState
    # global DOCKED, DOCKREQUESTED, UNDOCKREQUESTED, NOTDOCKED, CABLED

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
                       if ( (possibleEarlyTrickleVolts - shortMeanVolts) > 0.3 ):
                           lifeLog.logger.info("--- Probable EARLY TRICKLE DETECTED at {:.1f}v".format(shortMeanVolts))
                           chargingValue = TRICKLING
                           lastChangeRule = "230b"
                           possibleEarlyTrickleVolts = 0
                       elif (possibleEarlyTrickleVolts == 0):
                           logMsg = "--- Possible EARLY TRICKLE DETECTED at {:.1f}v".format(shortMeanVolts)
                           lifeLog.logger.info(logMsg)
                           print(logMsg)
                           possibleEarlyTrickleVolts = shortMeanVolts
               elif  (lastChangeInSeconds >  maxChargeTime):        # max charge time is around 3.5-4.0h
                       chargingValue = TRICKLING
                       lastChangeRule = "230c"
                       logMsg = "--- Probable TRICKLE not detected {:.1f}v".format(shortMeanVolts)
                       lifeLog.logger.info(logMsg)
                       print(logMsg)
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
               # print("slope:{} lastChangeInSeconds:{} shortMeanV:{} longMeanV:{} dockingState:{}".format(
               #        slope, lastChangeInSeconds, shortMeanVolts, longMeanVolts, dockingState))

               if ((slope > 0) and \
                   (lastChangeInSeconds > 150) and \
                   (shortMeanVolts > longMeanVolts) and \
                   (shortPeakVolts >= longPeakVolts) and \
                   ((shortPeakVolts - shortMinVolts)>0.5) and \
                   (dockingState == DOCKED)):
                       chargingValue = CHARGING
                       lastChangeRule = "120"
               elif ((slope > 0) and \
                   (lastChangeInSeconds > 150) and \
                   ((shortMeanVolts - longMeanVolts)>0.1) and \
                   # (shortPeakVolts >= longPeakVolts) and \
                   # ((shortPeakVolts - shortMinVolts)>0.5) and \
                   (dockingState == DOCKREQUESTED)):
                       chargingValue = CHARGING
                       lastChangeRule = "121"
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
               elif ( (longMeanVolts > shortMeanVolts) and \
                      (longPeakVolts < 10.5) and \
                      (slope < 0) and \
                      (lastChangeInSeconds > 300) ):
                          chargingValue = NOTCHARGING
                          lastChangeRule = "410a"
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
        # chargingValue = UNKNOWN
        chargingValue = chargingState
        # cd.saveCarlData('chargingState',chargingState)
        # lastChangeRule = "44b"
        print("chargeStatus(): Only one reading so far. chargingState: {}".format(chargingState))

    # check if changed from last time checked
    lastChargingState = chargingState
    if (lastChargingState != chargingValue):
        chargingState = chargingValue
        dtLastChargingStateChange = dtNow
        currentPrintableChargingState = printableCS[chargingState]
        print("*** chargingState changed from: ",printableCS[lastChargingState]," to: ", currentPrintableChargingState, " ****")
        print("*** by Rule: ",lastChangeRule)
        speak.whisper("New Charging State"+currentPrintableChargingState)
        cd.saveCarlData('chargingState',chargingState)
        if chargingState == CHARGING:
            chargeCycles = int(cd.getCarlData('chargeCycles'))
            chargeCycles += 1
            cd.saveCarlData('chargeCycles',chargeCycles)
    return chargingValue

def printValues():
    print ("\nJuicer Values:")
    dtNow = dt.datetime.now()
    runTimeInSeconds = (dtNow - dtStart).total_seconds()
    runTimeDays = divmod(runTimeInSeconds, 86400)
    runTimeHours = divmod(runTimeDays[1], 3600)
    runTimeMinutes = divmod(runTimeHours[1], 60)
    print ("Juicer Run Time %d days %dh %dm" % (runTimeDays[0],runTimeHours[0],runTimeMinutes[0]))
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
    if (chargeConditioning>0): 
        print ("Conditioning Cycle:",chargeConditioning)
        print ("Conditioning Play Time Limit {}v".format(CONDITIONING_LIMIT))
    else:
        print ("Play Time Limit {}v".format(PLAYTIME_LIMIT))
    if (possibleEarlyTrickleVolts>0): print ("possibleEarlyTrickleVolts: {:.2f}".format(possibleEarlyTrickleVolts) )


def safetyCheck(egpg,low_battery_v = SHUTDOWN_LIMIT):
        global lowBatteryCount, shortMinVolts, shortMeanVolts


        vBatt = shortMeanVolts
        if (vBatt < low_battery_v):
            lowBatteryCount += 1
            print("\n******** WARNING: {}v Safety Shutdown Is Imminent ******".format(low_battery_v))
            speak.say("Safety Shutdown Is Imminent.")
        else: lowBatteryCount = 0
        if (lowBatteryCount > 3):
          print("SHORT MIN BATTERY VOLTAGE: %.2f" % shortMinVolts)
          print("SHORT MEAN BATTERY VOLTAGE: %.2f" % shortMeanVolts)
          sleep(1)
          vBatt = egpg.volt()
          speak.shout("WARNING, WARNING, SHUTTING DOWN NOW")
          print ("BATTERY %.2f volts BATTERY LOW - SHUTTING DOWN NOW" % vBatt)
          print ("Shutdown at ", dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
          strToLog = "Safety Shutdown at  {:.2f} volts".format(vBatt)
          lifeLog.logger.info(strToLog)
          sleep(1)
          os.system("sudo shutdown -h now")
          sys.exit(0)

# default undocking is trickling->notcharging rule 310c
def undock(egpg,ds,tp, rule="310c"):
    global dockingDistanceInCM,dockingState,chargingState,dtLastChargingStateChange
    global lastChangeRule,dtLastDockingStateChange,chargeConditioning,possibleEarlyTrickleVolts

    printValues()
    tp.tiltpan_center()
    distanceForwardInMM = myDistSensor.adjustReadingInMMForError(ds.read_mm())
    # if ( (distanceForwardInMM > (dockingDistanceInMM * 2.0)) and \
    if ( (distanceForwardInMM > dismountBlockedInMM) and \
         (dockingState == DOCKED) ):
         print("\n**** INITIATING DISMOUNT ****")
         speak.whisper("Initiating dismount.")
         sleep(5)
         distanceForwardInMM = myDistSensor.adjustReadingInMMForError(ds.read_mm())
         if (distanceForwardInMM > dismountBlockedInMM):
             print("**** Dismounting")
             speak.whisper("Dismounting")
             egpg.set_speed(150)
             dismountDistanceInCM = (dockingDistanceInMM + dismountFudgeInMM)/10.0
             egpg.drive_cm(dismountDistanceInCM,True)
             dockingState = NOTDOCKED
             cd.saveCarlData('dockingState', dockingState)
             dtNow = dt.datetime.now()
             lastChargingState = chargingState
             chargingState = NOTCHARGING
             cd.saveCarlData('chargingState',chargingState)
             lastChangeRule = rule   # "310c" default or 110 docking failure 
             dtLastChargingStateChange = dtNow
             print("*** chargingState changed from: ",printableCS[lastChargingState]," to: ", printableCS[chargingState]," ****")
             print("*** by Rule: ",lastChangeRule)
             speak.whisper("New Charging State"+printableCS[chargingState])
             print("**** DISMOUNT COMPLETE AT ", dtNow.strftime("%Y-%m-%d %H:%M:%S") )
             speak.whisper("Dismount complete")

             # 
             lastDockingChangeInSeconds = (dtNow - dtLastDockingStateChange).total_seconds()
             lastDockingChangeDays = divmod(lastDockingChangeInSeconds, 86400)
             lastDockingChangeHours = round( (lastDockingChangeDays[1] / 3600.0),1)
             #print("lastDockingChangeDays:",lastDockingChangeDays)
             #print("lastDockingChangeHours:",lastDockingChangeHours)
             # prepare a two reading average of battery voltage to log for dismount
             vBatt = egpg.volt()
             sleep(0.25)
             vBatt = (vBatt + egpg.volt())/2.0
             strToLog = "---- Dismount {0} at {1:.1f} v after {2:.1f} h recharge".format( dockingCount,vBatt, lastDockingChangeHours)
             lifeLog.logger.info(strToLog)
             cd.saveCarlData('lastDismount',strToLog)
             cd.saveCarlData('lastDismountTime', dtNow.strftime("%Y-%m-%d %H:%M:%S"))
             cd.saveCarlData('lastRechargeDuration', "{:.1f}".format(lastDockingChangeHours))
             print(strToLog)
             dtLastDockingStateChange = dtNow
             possibleEarlyTrickleVolts = 0      # undocked so possible trickle voltage no longer relevant
             # check ~/Carl/carlData.json value (if set >0 will begin rundown to lower voltage cycles)
             try:
                 chargeConditioning = int(cd.getCarlData('chargeConditioning'))
             except:
                 chargeConditioning = 0



         else:
             print(dt.datetime.now().strftime("%H:%M:%S"),"**** DISMOUNT BLOCKED by object at: %.0f inches" % (distanceForwardInMM / 25.4) )
             speak.say("Dismount blocked")

    elif ( dockingState == CABLED ):
             print("**** Please DISCONNECT CABLE ****")
             speak.say("Please disconnect cable.")
    elif ( dockingState == UNDOCKREQUESTED ):
             print("**** PLEASE MANUALLY UNDOCK ME ****")
             speak.say("Please take me off the dock.")
             speak.say("Requesting manual undock.")
             strToLog = "Manual UnDock Requested at {}v".format(shortMeanVolts)
             lifeLog.logger.info(strToLog)
             print(strToLog)


    else:
        print(dt.datetime.now().strftime("%H:%M:%S"),"**** UNABLE TO UNDOCK ****")
        speak.say("Unable to undock.")

    tp.off()
    # exit undock

def dock(egpg,ds,tp):
    global dockingApproachDistanceInCM,dockingState,dockingDistanceInCM,dockingCount,dtLastDockingStateChange
    global possibleEarlyTrickleVolts

    print("\n**** DOCKING REQUESTED ****")
    dtNow = dt.datetime.now()


    if ( dockingState == DOCKREQUESTED ):
             print("**** PLEASE MANUALLY DOCK ME ****")
             speak.say("Please put me on the dock.")
             sleep(5)
             speak.say("Requesting manual docking.")
             strToLog = "Manual Dock Requested at {}v".format(shortMeanVolts)
             lifeLog.logger.info(strToLog)
             # Do not set dtLastDockingStateChange till actually docked
             print(strToLog)
             return

    elif (dockingState != NOTDOCKED):
        print("**** ERROR: Docking request when not undocked")
        return

    tp.tiltpan_center()
    distanceReadings = []
    for x in range(6):
        sleep(0.2)
        distanceReadings += [ds.read_mm()]
    # print("**** Distance Readings:",distanceReadings)
    distanceForwardInMM = myDistSensor.adjustReadingInMMForError(np.average(distanceReadings))
    print("**** Current  Distance is %.1f mm %.2f in" % (distanceForwardInMM, distanceForwardInMM / 25.4))
    print("**** Approach Distance is %.2f mm" % dockingApproachDistanceInMM )
    appErrorInMM = distanceForwardInMM - dockingApproachDistanceInMM
    if ( -allowedApproachErrorInMM <  appErrorInMM > allowedApproachErrorInMM ):
        print(dt.datetime.now().strftime("%H:%M:%S"),"**** DOCK APPROACH ERROR - REQUEST MANUAL PLACEMENT ON DOCK ****")
        speak.say("Dock approach error. Please put me on the dock")
        lastDockingChangeInSeconds = (dtNow - dtLastDockingStateChange).total_seconds()
        lastDockingChangeDays = divmod(lastDockingChangeInSeconds, 86400)
        lastDockingChangeHours = round( (lastDockingChangeDays[1] / 3600.0),1)
        strToLog = "---- Manual Docking {0} requested  at {1:.1f} v after {2:.1f} h playtime".format( dockingCount,shortMeanVolts,lastDockingChangeHours)
        lifeLog.logger.info("**** Dock Approach Error")
        lifeLog.logger.info(strToLog)
        dockingState = DOCKREQUESTED
        cd.saveCarlData('dockingState', dockingState)
        # Don't set dtLastDockingStateChane until actually Docked (RPIMonitor wants Docking.+playtime but don't want to reset playtime till actually on dock)
        # dtLastDockingStateChange = dt.datetime.now()
        if (  appErrorInMM > 0):
            print("**** Approach Distance too large by %.2f MM" % (appErrorInMM-allowedApproachError))
        else:
            print("**** Approace Distance too small by %.2f MM" % (appErrorInMM+allowedApproachError))
        sleep(5)
    elif ( (dockingState == NOTDOCKED) ):
        print("\n**** INITIATING DOCK MOUNTING SEQUENCE ****")
        speak.whisper("Initiating dock mounting sequence.")
        sleep(5)
        print("**** TURNING 180")
        speak.whisper("Turning one eighty.")
        egpg.set_speed(150)
        egpg.orbit(180)
        print("**** Preparing to Back onto dock")
        speak.whisper("Preparing to back onto dock.")
        sleep(5)
        # leave maxApproachDistanceMeasurementInMM to back manually
        backingDistanceInCM =  -1.0 * (dockingDistanceInMM + appErrorInMM -maxApproachDistanceMeasurementErrorInMM ) / 10.0
        print("**** BACKING ONTO DOCK %.0f mm" % (backingDistanceInCM * 10.0))
        speak.whisper("Backing onto dock")
        # sometimes the "wait for encoders" blocking will never happen.  Backing takes about 3 seconds, so timeout after 5 seconds.
        egpg.drive_cm( backingDistanceInCM,blocking=True,timeout=5)
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


        print("**** DOCKING COMPLETE AT ", dtNow.strftime("%Y-%m-%d %H:%M:%S") )
        speak.whisper("Docking completed.")
        dockingState = DOCKED
        cd.saveCarlData('dockingState', dockingState)
        cd.saveCarlData('lastDockingTime', dtNow.strftime("%Y-%m-%d %H:%M:%S") )
        dockingCount += 1
        lastDockingChangeInSeconds = (dtNow - dtLastDockingStateChange).total_seconds()
        lastDockingChangeDays = divmod(lastDockingChangeInSeconds, 86400)
        lastDockingChangeHours = round( (lastDockingChangeDays[1] / 3600.0),1)
        strToLog = "---- Docking {0} completed  at {1:.1f} v after {2:.1f} h playtime".format( dockingCount,shortMeanVolts,lastDockingChangeHours)
        lifeLog.logger.info(strToLog)
        cd.saveCarlData('lastDocking',strToLog)
        cd.saveCarlData('lastPlaytimeDuration',"{:.1f}".format(lastDockingChangeHours))
        dtLastDockingStateChange = dtNow
        possibleEarlyTrickleVolts = 0       # reset any prior detections
        sleep(5)
    else:
        print("\n**** UNKNOWN DOCKING ERROR ****")
        speak.say("Unknown docking error.")
        sleep(5)

    tp.off()
    # exit dock()


def manualDockingCompleted():
    global dockingState, chargingState, dockingCount, lastDockingChangeInSeconds, lastDockingChangeDays, lastDockingChangeHours, dtLastDockingStateChange
    global possibleEarlyTrickleVolts

    dtNow = dt.datetime.now()
    print("**** MANUAL DOCKING COMPLETE AT ", dtNow.strftime("%Y-%m-%d %H:%M:%S") )
    speak.whisper("Manual Docking completed.")
    dockingState = DOCKED
    cd.saveCarlData('dockingState',dockingState)
    dockingCount += 1
    lastDockingChangeInSeconds = (dtNow - dtLastDockingStateChange).total_seconds()
    lastDockingChangeDays = divmod(lastDockingChangeInSeconds, 86400)
    lastDockingChangeHours = round( (lastDockingChangeDays[1] / 3600.0),1)
    strToLog = "---- Docking {0} (manual) at {1:.1f} v and {2:.1f} h playtime".format( dockingCount,shortMeanVolts,lastDockingChangeHours)
    lifeLog.logger.info(strToLog)
    cd.saveCarlData('lastDocking',strToLog)
    dtLastDockingStateChange = dtNow
    possibleEarlyTrickleVolts = 0       # reset any prior detections

# Docking Test
#
# Place Carl on Dock, then 
# initiate with:  ./juicer.py test  (uncomment dockingTest in main)
# 
def dockingTest(egpg,ds,tp,numTests = 30):
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
        speak.whisper("Docking state is "+printableDS[dockingState])
        print("Charging State:", printableCS[chargingState])
        speak.whisper("Charging State is "+printableCS[chargingState])
        if (shortMeanVolts > DOCKING_TEST_LIMIT):
            undock(egpg,ds,tp)
            print("Status after undock()")
            print("Docking State:", printableDS[dockingState])
            speak.whisper("Docking state is "+printableDS[dockingState])
            print("Charging State:", printableCS[chargingState])
            speak.whisper("Charging State is "+printableCS[chargingState])
            sleep(5)

            if (dockingState == NOTDOCKED):
                print("\n**** DOCKING APPROACH INITIATED")
                action = "Turning around to be at approach point"
                print(action)
                speak.whisper(action)
                egpg.orbit(180)
                sleep(5)


                dock(egpg,ds,tp)
                print("Status after dock()")
                print("Docking State:", printableDS[dockingState])
                speak.whisper("Docking state is "+printableDS[dockingState])
                resetChargingStateToUnknown()
                print("checking battery level")
                while (longMeanVolts == 0):
                    compute(egpg)
                    chargingStatus()
                print("Charging State:", printableCS[chargingState])
                speak.whisper("Charging State is "+printableCS[chargingState])
                print("I'm thirsty.  I'll be here a while.")
                speak.whisper("I'm thirsty.  I'll be here a while.")
                sleep(5)
        else:
            print("\n**** shortMeanVolts %.2f insufficient" % shortMeanVolts)
            print("SLEEPING FOR 10 MINUTES\n")
            sleep(600)

def manualDockingTest(egpg,ds,tp,numTests = 1):
    global dockingState,chargingState

    print("\n**** MANUAL DOCKING TEST INITIATED ****")
    print("waiting for longMeanVolts not 0")
    while (longMeanVolts == 0):
        compute(egpg)
        chargingStatus()
    print("shortMeanVolts: %.2f" % shortMeanVolts)
    print("longMeanVolts: %.2f" % longMeanVolts) 
    dockingState = NOTDOCKED
    cd.saveCarlData('dockingState',dockingState)
    chargingState = NOTCHARGING
    cd.saveCarlData('chargingState',chargingState)
    dock(egpg,ds,tp)
    lastChangeRule = "Testing"

@runLog.logRun
def main():
    global dockingState,chargingState,dtLastDockingStateChange,chargeConditioning


    sim = False
    if (sim != True):
       egpg = easygopigo3.EasyGoPiGo3(use_mutex=True) # Create an instance of the EasyGoPiGo3 class
       lifeLog.logger.info("---- juicer.py started at {:.2f}v".format(egpg.volt()))
       myconfig.setParameters(egpg)
       ds = myDistSensor.init(egpg)
       tp = tiltpan.TiltPan(egpg)
       tp.tiltpan_center()
       sleep(0.5)
       tp.off()
    else:
       egpg = None

    loadVars()  # get vars from carlData.json

    print ("Juicer Main Initialization")
    print ("shortMeanDuration: %.1f" % shortMeanDuration)
    print ("longMeanDuration: %.1f" % longMeanDuration)
    print ("readingEvery %.1f seconds" % readingEvery)
    print ("simulation: ",sim)
    print ("dockingState: ", dockingState)
    print ("chargingState: ", chargingState)

    # ./juicer.py test   to perform undock/docking tests
    if (len(sys.argv)>1):
        if (sys.argv[1] == "test"):
            dockingTest(egpg,ds,tp,numTests = 5)
            # manualDockingTest(egpg,ds,tp)

    try:
        #  loop
        loopCount = 0
        while True:
            loopCount += 1
            compute(egpg)
            chargingStatus()
            if ((loopCount % 15) == 1 ):  # loop is 2s, so once every 30s print values
                status.printStatus(egpg,ds)
                printValues()
            safetyCheck(egpg)
            # Detect when docked
            if (((dockingState == UNKNOWN) or \
                 (dockingState == NOTDOCKED)) and \
                ((chargingState == TRICKLING) or \
                 (chargingState == CHARGING)) ):
                dockingState = DOCKED
                cd.saveCarlData('dockingState', dockingState)
                dtLastDockingStateChange = dt.datetime.now()
            # Detect when docked after manual docking requested
            if ((dockingState == DOCKREQUESTED) and \
                ((chargingState == TRICKLING) or \
                 (chargingState == CHARGING)) ):
                manualDockingCompleted()
            # Remind after manual docking request
            if ((dockingState == DOCKREQUESTED) and \
                (chargingState == NOTCHARGING)  and \
                (loopCount % 60 == 1) ):                  # every 2 minutes
                dtNow = dt.datetime.now()
                print("**** Awaiting Manual Docking: ", dtNow.strftime("%Y-%m-%d %H:%M:%S") )
                speak.whisper("Awaiting Manual Docking")
            # Starting up away from dock
            if ((dockingState == UNKNOWN) and \
                 (chargingState == NOTCHARGING) ):
                dockingState = NOTDOCKED
                cd.saveCarlData('dockingState', dockingState)
                dtLastDockingStateChange = dt.datetime.now()
            # Time to go out to play
            if ((chargingState == TRICKLING) and \
               (dockingState == DOCKED)):
                print("\n**** Time to get off the pot")
                undock(egpg,ds,tp)
            # Check for End of play time
            chargeConditioning = int(cd.getCarlData('chargeConditioning'))
            if ((chargingState == NOTCHARGING) and \
                (dockingState == NOTDOCKED) and \
                ( ((chargeConditioning ==0) and (shortMeanVolts < PLAYTIME_LIMIT)) or \
                  ((chargeConditioning > 0) and (shortMeanVolts < CONDITIONING_LIMIT)) ) \
               ) :
                print("\n**** Time to get on the pot")
                action = "**** Turning around to be at approach point"
                print(action)
                speak.whisper(action)
                egpg.orbit(180)
                sleep(5)
                dock(egpg,ds,tp)
                if (chargeConditioning > 0):
                    lifeLog.logger.info("-- Charge Conditioning {} completed".format(chargeConditioning))
                    chargeConditioning -= 1
                    cd.saveCarlData('chargeConditioning',chargeConditioning)

            # Detect docking that didn't align contacts well - need to undock/dock
            if ((dockingState == DOCKED) and \
                ((chargingState == UNKNOWN) or \
                 (chargingState == NOTCHARGING)) and \
                ( (dt.datetime.now() - dtLastDockingStateChange).total_seconds() > 300) ):
                printValues()
                print("\n**** Docking Failure Possible, undocking")
                speak.say("Docking Failure Possible, undocking.")
                lifeLog.logger.info("---- Docking Failure Possible")
                # resetChargingStateToUnknown()  # clear the voltage history to not confuse rules
                undock(egpg,ds,tp,rule="110")
            # False detection of Trickling as Charging - need to undock/dock
            if ((dockingState == DOCKED) and \
                (chargingState == CHARGING) and \
                ( ((chargeConditioning > 0) and (shortMeanVolts < CONDITIONING_LIMIT)) or \
                  ((chargeConditioning == 0) and (shortMeanVolts < PLAYTIME_LIMIT)) ) and \
                ( (dt.datetime.now() - dtLastDockingStateChange).total_seconds() > 300) ):
                printValues()
                print("\n**** Charger Trickling, Need Charging Possible, undocking")
                speak.say("Charger Trickling, I Need A Real Charge. Undocking.")
                lifeLog.logger.info("---- Docking Failure Possible. Trickling, Need Charging")
                # resetChargingStateToUnknown() # clear the voltage history to not confuse rules
                undock(egpg,ds,tp)


            sleep(readingEvery)

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    egpg.stop()           # stop motors
            print("Ctrl-C detected - Finishing up")
            printValues()
            print("**** juicer exit ****")
            sleep(1)
    egpg.stop()

if __name__ == "__main__":
	main()
