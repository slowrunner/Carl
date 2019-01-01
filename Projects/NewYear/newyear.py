#!/usr/bin/python
#
# newyear.py    Wish Happy New Year
#      Watch for impending new year,
#      Count Down from 10 seconds before new year
#      Wish "Happy New Year"
#      otherwise print status every 30s
#
#


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

LOW_BATTERY_V = 8.5   # 8cells x 1.1375 - 0.6 GoPiGo3 voltage drop

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


def closeToMidnight():
    d = datetime.now()
    minuteBefore = d.replace(hour=23, minute=59, second=0, microsecond=0)
    minuteAfter = d.replace(year=2019, month=1, day=1, hour=0, minute=0, second=0)
    if d > minuteBefore and d < minuteAfter:
        print ("close to midnight")
        return True
    else: return False


def countDownAndYell():
    afterMidnight = False
    d = datetime.now()
    startCountDown = d.replace(hour=23, minute = 59, second=50, microsecond=0)
    while not(afterMidnight):
        d = datetime.now()
        print ("d:",d)
        if d > startCountDown:
            for i in range (10, 0, -1):
                nStr = "{}".format(i)
                d = datetime.now()
                print(nStr, d)
                speak.say(nStr)
                time.sleep(0.45)
            print ("Happy New Year")
            speak.say("Happy New Year Everybody.  Happy New Year.")
            afterMidnight = True
        else: time.sleep(1)

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
        else: batteryLowCount = 0
        if (batteryLowCount > 3):
          speak.say("WARNING, WARNING, SHUTTING DOWN NOW")
          print ("BATTERY %.2f volts BATTERY LOW - SHUTTING DOWN NOW" % vBatt)
          time.sleep(1)
          os.system("sudo shutdown -h now")
          sys.exit(0)
        if (closeToMidnight()):  countDownAndYell()
        time.sleep(5)
    #end while
  except SystemExit:
    print "status.py: exiting"

if __name__ == "__main__":
    main()

