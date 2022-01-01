#!/usr/bin/python3

#
# carl_newyear.py    Wish Happy New Year
#      Watch for impending new year,
#      Count Down from 10 seconds before new year
#      Wish "Happy New Year"
#      otherwise print status every 5 seconds
#      ( carl does not need low voltage shutdown protection )
#
# USAGE:
# ./carl_newyear.py         (start on December 31st of any year)
#
#  python3 carl_newyear.py
#
# ./carl_newyear.py -t or --test   targets 2nd future minute as start of new year
#                             (if time now 10:23:30, tgt time = 10:25:00)
#
# PRE-REQUIREMENT
#   espeak-ng  text-to-speech   sudo apt-get install espeak-ng
#                               test tts:  espeak-ng "hello"
#
from __future__ import print_function
from __future__ import division

# import the modules

import sys
import subprocess
import time
import signal
import os
from datetime import datetime, timedelta
import easygopigo3
import argparse

LOW_BATTERY_V = 8.1   # 8cells x 1.0875 (-0.6v GoPiGo3 voltage drop)

# ARGUMENT PARSER
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--test", default=False, action='store_true', help="test 2nd minute from now")
args = vars(ap.parse_args())
testFlag = args['test']

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


def printStatus(egpg):
  print("\n********* GoPiGo STATUS *****")
  print(datetime.now().date(), getUptime())
  vBatt = egpg.volt()  # use thread-safe version not get_battery_voltage
  print("Battery Voltage: %0.2f" % vBatt)
  v5V = egpg.get_voltage_5v()
  print("5v Supply: %0.2f" % v5V)
  print("Processor Temp: %s" % getCPUtemperature())
  print("Clock Frequency: %s" % getClockFreq())
  print("%s" % getThrottled())


def say_espeak(phrase,vol=100):

    phrase = phrase.replace("I'm","I m")
    phrase = phrase.replace("'","")
    phrase = phrase.replace('"',' quote ')
    phrase = phrase.replace('*',"")

    subprocess.check_output(['espeak-ng -s150 -ven-us+f5 -a'+str(vol)+' "%s"' % phrase], stderr=subprocess.STDOUT, shell=True)

def closeToMidnight(minuteBefore,tgtTime):
    d = datetime.now()
    if d > minuteBefore and d < tgtTime:
        print("\n !!! Getting Close To ",tgtTime)
        return True
    else: return False


def countDownAndYell():
    afterMidnight = False
    d = datetime.now()
    # startCountDown = d.replace(hour=23, minute = 59, second=50, microsecond=0)
    startCountDown = d.replace(second=50, microsecond=0)
    while not(afterMidnight):
        d = datetime.now()
        print (" Time Now:",d.replace(microsecond=0))
        if d > startCountDown:
            for i in range (10, 1, -1):
                nStr = "{}".format(i)
                d = datetime.now().replace(microsecond=0)
                print(nStr, d)
                say_espeak(nStr)
                # time.sleep(0.1)
            time.sleep(1.0)
            print ("\n **** HAPPY NEW YEAR ****\n")
            say_espeak("Happy New Year Everybody.  Happy New Year.")
            afterMidnight = True
        else: time.sleep(1)

# ######### CNTL-C #####
# Callback and setup to catch control-C and quit program

_funcToRun=None

def signal_handler(signal, frame):
  print('\n** Control-C Detected')
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
  print("status.py: handle_ctlc() executed")

def main():

  # #### SET CNTL-C HANDLER
  set_cntl_c_handler(handle_ctlc)

  # #### Create a mutex protected instance of EasyGoPiGo3 base class
  egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)

  batteryLowCount = 0

  dtNow = datetime.now().replace(microsecond=0)

  if testFlag:
      minuteBefore = dtNow - timedelta(seconds = dtNow.second, microseconds = dtNow.microsecond) \
                         + timedelta(minutes = 1)
      tgtTime =  minuteBefore + timedelta(minutes = 1)
  else:
      minuteBefore = dtNow.replace(hour=23, minute=59, second=0, microsecond=0)
      # minuteAfter = d.replace(year=2019, month=1, day=1, hour=0, minute=0, second=0)
      tgtTime = minuteBefore + timedelta(minutes = 1)
  print("dtNow:",dtNow)
  print("countdown watch:",minuteBefore)
  print("target datetime:",tgtTime)

  try:
    while True:
        printStatus(egpg)
        # vBatt = egpg.volt()
        # if (vBatt < LOW_BATTERY_V):
        #     batteryLowCount += 1
        # else: batteryLowCount = 0
        # if (batteryLowCount > 3):
          # speak.say("WARNING, WARNING, SHUTTING DOWN NOW")
          # print ("BATTERY %.2f volts BATTERY LOW - SHUTTING DOWN NOW" % vBatt)
          # time.sleep(1)
          # os.system("sudo shutdown -h now")
          # sys.exit(0)
        if (closeToMidnight(minuteBefore,tgtTime)):  countDownAndYell()
        time.sleep(5)
    #end while
  except SystemExit:
    print("status.py: exiting")

if __name__ == "__main__":
    main()

