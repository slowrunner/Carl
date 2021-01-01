#!/usr/bin/python3
#
# Carls_NewYear.py    Wish Happy New Year
#      Watch for impending new year,
#      Count Down from 10 seconds before new year
#      Wish "Happy New Year"
#      otherwise print status every 30s
#
#


#

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
import status

# Set low because Juicer should be managing battery
LOW_BATTERY_V = 7.6   # 8cells x 1.1375 - 0.6 GoPiGo3 voltage drop


def closeToMidnight():
    d = datetime.now()
    minuteBefore = d.replace(hour=23, minute=59, second=0, microsecond=0)
    minuteAfter = d.replace(year=2019, month=1, day=1, hour=0, minute=0, second=0)
    if d > minuteBefore and d < minuteAfter:
        print("close to midnight")
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
  print("status.py: handle_ctlc() executed")

def main():

  # #### SET CNTL-C HANDLER
  myPyLib.set_cntl_c_handler(handle_ctlc)

  # #### Create a mutex protected instance of EasyGoPiGo3 base class
  egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)

  # ### Create (protected) instance of EasyDistanceSensor
  ds = egpg.init_distance_sensor()  # use_mutex=True passed from egpg

  batteryLowCount = 0
  alert = "Starting My New Year Watch at {:.2f} volts".format( egpg.volt())
  print(datetime.now().strftime("%Y-%m-%d %H:%M:%S "), alert)
  speak.say(alert)

  try:
    while True:
        status.printStatus(egpg,ds)
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
        if (closeToMidnight()):
            countDownAndYell()
            break
        time.sleep(5)
    #end while
  except SystemExit:
      pass
  print("status.py: exiting")

 

if __name__ == "__main__":
    main()

