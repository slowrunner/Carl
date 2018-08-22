#!/usr/bin/python
#
# status.py    Basic Status
#      Run Battery down while printing status every 30s
#
# This test will loop reading the battery voltage
#      UNTIL voltage stays below 7.5v 4 times,
#      then will issue a shutdown now
#
#
import sys
sys.path
sys.path.append('/home/pi/Carl/plib')

import time
import signal
import os
import myPyLib
from datetime import datetime

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


def printStatus():
  global b, u

  print "\n********* CARL Basic STATUS *****"
  print datetime.now().date(), getUptime()
  vBatt = 9.2  #battery.volts()
  #print "battery.volts(): %0.2f" % vBatt
  #lifeRem=battery.hoursOfLifeRemaining(vBatt)
  #lifeH=int(lifeRem)
  #lifeM=(lifeRem-lifeH)*60
  #print "battery.hoursOfLifeRemaining(): %d h %.0f m" % (lifeH, lifeM) 
  print "Processor Temp: %s" % getCPUtemperature()
  print "Clock Frequency: %s" % getClockFreq()
  print "%s" % getThrottled()
  #print "currentsensor.current_sense(): %.0f mA" % currentsensor.current_sense()
  #print  "irDistance.inInches: %0.1f" %  irDistance.inInches()



# ##### MAIN ######

def handle_ctlc():
  global b, u
  #b.cancel()
  #u.cancel()
  print "status.py: handle_ctlc() executed"

def main():
  global b, u

  # #### SET CNTL-C HANDLER 
  myPyLib.set_cntl_c_handler(handle_ctlc)

  # #### INIT SENSORS 
  # b=Bumpers()
  # u=UltrasonicDistance()
  batteryLowCount = 0
  #print ("Starting status loop at %.2f volts" % battery.volts())  
  try:
    while True:
        printStatus()
        #if (battery.batteryTooLow()): 
        #    batteryLowCount += 1
        #else: batteryLowCount = 0
        #if (batteryLowCount > 3):
          # speak.say("WARNING, WARNING, SHUTTING DOWN NOW")
        #  print ("BATTERY %.2f volts BATTERY - SHUTTING DOWN NOW" % battery.volts())
        #  os.system("sudo shutdown -h now")
        #  sys.exit(0)
        time.sleep(5)
    #end while
  except SystemExit:
    print "status.py: exiting"

if __name__ == "__main__":
    main()

