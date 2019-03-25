#!/usr/bin/python
#
# measureLife.py     Controlled Battery Life Measurement
#      Run Battery down while printing status every 10 seconds
#
#      This test will loop reading the battery voltage
#        UNTIL voltage stays below 7.4v 4 times,
#        then will force a shutdown.
#
#      Note: actual battery voltage is 0.6v higher than reading
#            7.4v reading limit reliably gives time for orderly shutdown 
#
# 2019-03-25: changed to use volt() instead of get_voltage_battery()
#             which read 0.1 lower than egpg.volt()
#      
#
import sys
import time
import signal
import os
from datetime import datetime

import easygopigo3

LOW_BATTERY_V = 7.4   # (7.4+0.6 = 8cells x 1.0v safe value, could go to 0.9

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
  global egpg

  print "\n********* CARL Basic STATUS *****"
  print datetime.now().date(), getUptime()
  vBatt = egpg.volt()  #egpg.get_voltage_battery()
  print "Battery Voltage: %0.2f" % vBatt
  v5V = egpg.get_voltage_5v()
  print "5v Supply: %0.2f" % v5V
  print "Processor Temp: %s" % getCPUtemperature()
  print "Clock Frequency: %s" % getClockFreq()
  print "%s" % getThrottled()

# ######### CNTL-C #####
# Callback and setup to catch control-C and quit program

_funcToRun=None

def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  if (_funcToRun != None):
     _funcToRun()
  sys.exit(0)     # raise SystemExit exception

# Setup the callback to catch control-C
def set_cntl_c_handler(toRun=None):
  global _funcToRun
  _funcToRun = toRun
  signal.signal(signal.SIGINT, signal_handler)




# ##### MAIN ######

def handle_ctlc():
  global egpg
  egpg.reset_all()
  print "status.py: handle_ctlc() executed"

def main():
  global egpg

  # #### SET CNTL-C HANDLER 
  set_cntl_c_handler(handle_ctlc)

  # #### Create instance of GoPiGo3 base class 
  egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
  batteryLowCount = 0
  #print ("Starting status loop at %.2f volts" % battery.volts())  
  try:
    while True:
        printStatus()
        vBatt = egpg.volt()
        if (vBatt < LOW_BATTERY_V): 
            batteryLowCount += 1
        else: batteryLowCount = 0
        if (batteryLowCount > 3):
          print ("WARNING, WARNING, SHUTTING DOWN NOW")
          print ("BATTERY %.2f volts BATTERY LOW - SHUTTING DOWN NOW" % vBatt)
          egpg.reset_all()
          time.sleep(1)
          os.system("sudo shutdown -h now")
          sys.exit(0)
        time.sleep(10)    # check battery status every 10 seconds
                          # important to make four checks low V quickly      
    #end while
  except SystemExit:
    print "status.py: exiting"

if __name__ == "__main__":
    main()



