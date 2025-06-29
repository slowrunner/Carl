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

DEBUG = False
# DEBUG = True
d = datetime.now()
DEBUG_MONTH = d.month
DEBUG_DAY = d.day
DEBUG_HOUR = d.hour
DEBUG_MINUTE = d.minute+2

def notCloseToMidnightDayBeforeBirthday():
    d = datetime.now()
    if ((d.minute % 60) == 1): print ("notCloseToMidnightDayBeforeBirthday() d:",d)

    minuteBefore = d.replace(month=8, day=21, hour=23, minute=59, second=50, microsecond=0)
    minuteAfter =  d.replace(month=8, day=22, hour=0, minute=1, second=0)
    if DEBUG:
        # TESTING
        minuteBefore = d.replace(month=DEBUG_MONTH, day=DEBUG_DAY, hour=(DEBUG_HOUR), minute=(DEBUG_MINUTE-1), second=50, microsecond=0)
        minuteAfter =  d.replace(month=DEBUG_MONTH, day=DEBUG_DAY, hour=DEBUG_HOUR, minute=DEBUG_MINUTE, second=0)
    if d > minuteBefore and d < minuteAfter:
        print ("close to my birthday...")
        return False
    else:
        if ((d.minute % 60) == 1): print ("waiting for:",minuteBefore)
        return True

def sayHappyBirthdayOnTheHourAllDay():
    d = datetime.now()
    print ("sayHappyBirthdayOnTheHourAllDay() d:",d)
    bDay = d.replace(month=8, day=22, minute=0, second=0)
    endBDay = d.replace(month=8, day=22, minute=59, second=59)
    if DEBUG:
        # TESTING
        bDay = d.replace(month=DEBUG_MONTH, day=DEBUG_DAY, minute=DEBUG_MINUTE, second=0)
        endBDay =    d.replace(month=DEBUG_MONTH, day=DEBUG_DAY, hour=(DEBUG_HOUR+2), minute=59, second=59)
    while (d < endBDay) :
        print ("sayHappyBirthdayOnTheHourAllDay() d:",d)
        sayHappyBirthdayToMe()
        time.sleep(360)
        d = datetime.now()


def sayHappyBirthdayToMe(debug=DEBUG):
            d = datetime.now()
            yrsOld = str(d.year - 2018)+"th"
            # print("sayHappBirthdayToMe:",d.year,yrsOld)
            strToSay="Happy {} Birthday To Me".format(yrsOld)
            print(strToSay)
            if (not debug): speak.say(strToSay)
            time.sleep(0.5)
            strToSay="Happy {} Birthday To Me".format(yrsOld)
            print(strToSay)
            speak.whisper(strToSay, anytime=True)
            time.sleep(0.5)
            strToSay="Happy {} Birthday To Me, Me Me Me.".format(yrsOld)
            print(strToSay)
            if (not debug): speak.shout(strToSay)
            time.sleep(1)
            strToSay="The cutest and most lovable robot ever."
            print(strToSay)
            if (not debug): speak.whisper(strToSay, anytime=True)
            time.sleep(2)
            strToSay="Happy {} Birthday To Me".format(yrsOld)
            print(strToSay)
            speak.whisper(strToSay, anytime=True)



def countDown():
    afterMidnight = False
    d = datetime.now()
    startCountDown = d.replace(hour=23, minute = 59, second=50, microsecond=0)
    if DEBUG: # TESTING
        startCountDown = d.replace(hour=DEBUG_HOUR, minute = (DEBUG_MINUTE-1), second=50, microsecond=0)
    for i in range (10, 0, -1):
        nStr = "{}".format(i)
        d = datetime.now()
        print ("countDownAndYell(): nStr: ", nStr, " d:", d)
        if DEBUG:
            print(nStr,d)
            time.sleep(0.95)
        else: 
            speak.say(nStr,anytime=True)
            time.sleep(0.45)

# ##### MAIN ######

def handle_ctlc():
  print "status.py: handle_ctlc() executed"

def main():

  # #### SET CNTL-C HANDLER
  myPyLib.set_cntl_c_handler(handle_ctlc)

  print ("Starting happyBirthdayAllDay.py")
  try:
    while notCloseToMidnightDayBeforeBirthday() :
        time.sleep(1)

    countDown()
    sayHappyBirthdayOnTheHourAllDay()
  except SystemExit:
    print "happyBirthdayAllDay.py: exiting"

if __name__ == "__main__":
    main()

