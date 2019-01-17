#!/usr/bin/python
#
# status.py    Basic Status (thread-safe)
#      Run Battery down while printing status every 30s
#
# This test will loop reading the battery voltage
#      UNTIL voltage stays below 8.1v 4 times,
#      then will issue a shutdown now
#

# After advice from some folks over at raspberrypi.org robotics forum,
# and thinking about the 168 NiMH cells in my 10 year old Prius,
# my target discharge depth is 15-20% remaining capacity.
# 2019-January: ran logBattV.py - 8hrs to yellow light, a little more to "red and dead"
# The GoPiGo3 volt() function registered 8.1v at the 15-20% capacity point 
# which would be 8.7v at the battery pack or 1.09v/cell.
# (GoPiGo3 reverse polarity protection diode drop of 0.6v)
# This will yield a little more than 6.5 hours of mindless contemplation by my bot in its corner.
# Sacrificing 45-90 minutes of immediate gratification for longevity.

#
# from __future__ import print_function
from __future__ import division

# import the modules

import sys
sys.path
sys.path.append('/home/pi/Carl/plib')

import time
import signal
import os
import myPyLib
import speak
from datetime import datetime
import easygopigo3
import battery

LOW_BATTERY_V = 8.1   # (8cells x 1.09) - 0.6 GoPiGo3 voltage drop from reverse voltage protection diode

# Return CPU temperature as a character string
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("\n",""))

# Return Clock Freq as a character string
def getClockFreq():
    res = os.popen('vcgencmd measure_clock arm').readline()
    res = int(res.split("=")[1])
    if (res < 1000000000):
        res = str(res/1000000)+" MHz"
    else: res = '{:.2f}'.format(res/1000000000.0)+" GHz"
    return res

# Return throttled flags as a character string
def getThrottled():
    res = os.popen('vcgencmd get_throttled').readline()
    return res.replace("\n","")

def getUptime():
    res = os.popen('uptime').readline()
    return res.replace("\n","")


def printStatus(egpg,ds):


  print "\n********* CARL Basic STATUS *****"
  print datetime.now().date(), getUptime()
  vBatt = egpg.volt()  # use thread-safe version not get_battery_voltage
  print "Battery Voltage: %0.2f" % vBatt
  v5V = egpg.get_voltage_5v()
  print "5v Supply: %0.2f" % v5V
  lifeRem=battery.hoursOfLifeRemaining(vBatt)
  lifeH=int(lifeRem)
  lifeM=(lifeRem-lifeH)*60
  print "Estimated Life Remaining: %d h %.0f m" % (lifeH, lifeM)
  print "Processor Temp: %s" % getCPUtemperature()
  print "Clock Frequency: %s" % getClockFreq()
  print "%s" % getThrottled()
  #print "currentsensor.current_sense(): %.0f mA" % currentsensor.current_sense()
  distReading = ds.read_inches()
  if distReading < 90:
      print  "Distance Sensor: %0.1f inches" %  ds.read_inches()
  else:
      print  "Distance Sensor: nothing within 90 inches"


# ##### MAIN ######

def handle_ctlc():
  print "status.py: handle_ctlc() executed"

def main():

  # #### SET CNTL-C HANDLER
  myPyLib.set_cntl_c_handler(handle_ctlc)

  # #### Create a mutex protected instance of EasyGoPiGo3 base class
  egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)

  # ### Create (protected) instance of EasyDistanceSensor
  ds = egpg.init_distance_sensor()  # use_mutex=True passed from egpg

  batteryLowCount = 0
  #print ("Starting status loop at %.2f volts" % battery.volts())
  try:
    while True:
        printStatus(egpg,ds)
        vBatt = egpg.volt()
        if (vBatt < LOW_BATTERY_V):
            batteryLowCount += 1
            speak.say("Hello? My battery is getting a little low here.")
            print("\nHello? My Battery is getting a little low here.")
        else: batteryLowCount = 0
        if (batteryLowCount > 3):
          speak.say("WARNING, WARNING, SHUTTING DOWN NOW")
          print ("BATTERY %.2f volts BATTERY LOW - SHUTTING DOWN NOW" % vBatt)
          time.sleep(1)
          os.system("sudo shutdown -h now")
          sys.exit(0)
        time.sleep(5)
    #end while
  except SystemExit:
    print "status.py: exiting"

if __name__ == "__main__":
    main()

