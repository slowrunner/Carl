#!/usr/bin/python
#
# happyBirthdayAllDay.py    Sing Happy Birthday To Me once an hour
#      Watch for Birthday,
#      Count Down from 10 seconds before birthday
#      Sing "Happy Birthday To Me" every hour on the day
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
import my_easygopigo3 as easygopigo3
import battery


def closeToMidnight():
    d = datetime.now()
    minuteBefore = d.replace(month=8, day=21, hour=23, minute=59, second=50, microsecond=0)
    minuteAfter =  d.replace(month=8, day=22, hour=0, minute=0, second=0)
    # TESTING
    d = datetime.now()
    minuteBefore = d.replace(month=8, day=21, hour=9, minute=59, second=50, microsecond=0)
    minuteAfter =  d.replace(month=8, day=21, hour=10, minute=0, second=0)
    if d > minuteBefore and d < minuteAfter:
        print ("close to my birthday...")
        return True
    else: return False

def myBirthdayAndOnTheHour():
    d = datetime.now()
    bDay = d.replace(month=8, day=22, minute=0, second=0)
    endBDay = d.replace(month=8, day=22, minute=59, second=59)
    # TESTING
    bDay = d.replace(month=8, day=21, minute=10, second=0)
    endBDay =    d.replace(month=8, day=21, hour=23, minute=59, second=59)
    if (d > bDay) and (d < endBDay):
        print("Time to sing...")
        return True
    else: return False

def sayHappyBirthdayToMe():
            strToSay="Happy Birthday To Me"
            print(strToSay)
            speak.say(strToSay, anytime=True)
            time.sleep(0.5)
            strToSay="Happy Birthday To Me"
            print(strToSay)
            speak.whisper(strToSay, anytime=True)
            time.sleep(0.5)

            strToSay="Happy Birthday To Me, Me Me Me."
            print(strToSay)
            speak.shout(strToSay, anytime=True)
            time.sleep(1)

            strToSay="The cutest and most lovable robot ever."
            print(strToSay)
            speak.whisper(strToSay, anytime=True)
            time.sleep(2)
            strToSay="Happy Birthday To Me"
            print(strToSay)
            speak.whisper(strToSay, anytime=True)



def countDownAndYell():
    afterMidnight = False
    d = datetime.now()
    # startCountDown = d.replace(hour=23, minute = 59, second=50, microsecond=0)
    # TESTING
    startCountDown = d.replace(hour=15, minute = 24, second=50, microsecond=0)
    while not(afterMidnight):
        d = datetime.now()
        print ("d:",d)
        if d > startCountDown:
            for i in range (10, 0, -1):
                nStr = "{}".format(i)
                d = datetime.now()
                print(nStr, d)
                speak.say(nStr,anytime=True)
                time.sleep(0.45)

            sayHappyBirthdayToMe()
            afterMidnight = True
        else: time.sleep(1)

# ##### MAIN ######

def handle_ctlc():
  print "status.py: handle_ctlc() executed"

def main():

  # #### SET CNTL-C HANDLER
  myPyLib.set_cntl_c_handler(handle_ctlc)

  # #### Create a mutex protected instance of EasyGoPiGo3 base class
  # egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)

  # ### Create (protected) instance of EasyDistanceSensor
  # ds = egpg.init_distance_sensor()  # use_mutex=True passed from egpg

  print ("Starting happyBirthdayAllDay.py")
  try:
    while True:
        if (closeToMidnight()):  countDownAndYell()
        time.sleep(5)
        if myBirthdayAndOnTheHour():
            sayHappyBirthdayToMe()
    #end while
  except SystemExit:
    print "happyBirthdayAllDay.py: exiting"

if __name__ == "__main__":
    main()

