#!/usr/bin/env python3
#
# volt_test.py

"""
Documentation:

test if a sleep(1) before a call to EasyGoPiGo3.volt() affects the measurement
"""

# from __future__ import print_function # use python 3 syntax but make it compatible with python 2
# from __future__ import division       #                           ''

import sys
sys.path.append('/home/pi/Carl/plib')
import easygopigo3 # import the GoPiGo3 class
import tiltpan
import status
import battery
import numpy as np
import datetime as dt
#import speak
#import myDistSensor
import lifeLog
#import argparse
from time import sleep
# import cv2

# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-f", "--file", help="path to input file")
#ap.add_argument("-n", "--num", type=int, default=5, help="number")
#args = vars(ap.parse_args())
#print("Started with args:",args)


# constants


# varibles


def main():
    lifeLog.logger.info("Started")

    firstReadingList = [ ]
    secondReadingList = [ ]
    diffReadingList = [ ]
    timeFirstToSecondList = [ ]
    timeSecondToFirstList = [ ]
    firstMeanVolts = 0
    secondMeanVolts = 0
    times1stGreater = 0
    times2ndGreater = 0
    numLoops = 100


    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    ds = egpg.init_distance_sensor()

    tiltpan.tiltpan_center()
    sleep(0.5)
    tiltpan.off()

    try:
        #  loop
        loopSleep = 1 # second
        gapSleep =  .166
        readDist = True
        loopCount = 0
        while (loopCount < numLoops):
            loopCount += 1
            print("loop:{}".format(loopCount), end = '\r')

            dtFirstReading = dt.datetime.now()
            if (loopCount>1): 
                dtPriorSecondReading = dtSecondReading
            firstReading = egpg.volt()
            if (readDist == True): distReading = ds.read_mm()
            sleep(gapSleep)
            dtSecondReading = dt.datetime.now()
            secondReading = egpg.volt()

            if (firstReading > secondReading):  times1stGreater +=1
            if (secondReading > firstReading):  times2ndGreater +=1
            firstReadingList += [firstReading]
            secondReadingList += [secondReading]
            diffReadingList += [firstReading - secondReading]
            timeFirstToSecondList += [(dtSecondReading - dtFirstReading).total_seconds()]
            if (loopCount>1):
                timeSecondToFirstList += [(dtFirstReading - dtPriorSecondReading).total_seconds()]

            sleep(loopSleep)
        # **** DONE LOOP ****
        maxFirstReadings = np.max(firstReadingList)
        meanFirstReadings = np.mean(firstReadingList)
        minFirstReadings = np.min(firstReadingList)
        stdFirstReadings =  np.std(firstReadingList)

        maxSecondReadings = np.max(secondReadingList)
        meanSecondReadings = np.mean(secondReadingList)
        minSecondReadings = np.min(secondReadingList)
        stdSecondReadings =  np.std(secondReadingList)

        maxDifference = np.max(diffReadingList)
        meanDifference = np.mean(diffReadingList)
        minDifference = np.min(diffReadingList)
        stdDifference = np.std(diffReadingList)

        maxFirstToSecond = np.max(timeFirstToSecondList)
        meanFirstToSecond = np.mean(timeFirstToSecondList)
        minFirstToSecond = np.min(timeFirstToSecondList)
        stdFirstToSecond = np.std(timeFirstToSecondList)

        maxSecondToFirst = np.max(timeSecondToFirstList)
        meanSecondToFirst = np.mean(timeSecondToFirstList)
        minSecondToFirst = np.min(timeSecondToFirstList)
        stdSecondToFirst = np.std(timeSecondToFirstList)

        print("\n     RESULTS     ")
        if (readDist):
            print("Sleep after ds.read_mm() before 2nd reading:{} Sleep at end of loop:{}".format(gapSleep,loopSleep))
        else:
            print("No readDist:      Sleep  before 2nd reading:{} Sleep at end of loop:{}".format(gapSleep,loopSleep))
        print("First Readings  - mean:{0:.3f} max:{1:.3f} min:{2:.3f} std:{3:.3f}".format(meanFirstReadings, maxFirstReadings, minFirstReadings, stdFirstReadings) )
        print("Second Readings - mean:{0:.3f} max:{1:.3f} min:{2:.3f} std:{3:.3f}".format(meanSecondReadings, maxSecondReadings, minSecondReadings, stdSecondReadings) )
        print("Difference      - mean:{0:.3f} max:{1:.3f} min:{2:.3f} std:{3:.3f}".format(meanDifference, maxDifference, minDifference, stdDifference) )
        print("time 1st to 2nd - mean:{0:.3f} max:{1:.3f} min:{2:.3f} std:{3:.3f}".format(meanFirstToSecond, maxFirstToSecond, minFirstToSecond, stdFirstToSecond) )
        print("time 2nd to 1st - mean:{0:.3f} max:{1:.3f} min:{2:.3f} std:{3:.3f}".format(meanSecondToFirst, maxSecondToFirst, minSecondToFirst, stdSecondToFirst) )
        print("times1stGreater: {}".format(times1stGreater))
        print("times2ndGreater: {}".format(times2ndGreater))

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    lifeLog.logger.info("Finished")
    sleep(1)

if __name__ == "__main__":
	main()





if (__name__ == 'main'):  main()
