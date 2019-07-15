#!/usr/bin/env python3
#
# readDistSensor2.py

"""
Continuously measure distance in millimeters, printing the average and individual readings
"""

from __future__ import print_function
from __future__ import division

import sys
sys.path.append('/home/pi/Carl/plib')
import numpy as np
import easygopigo3
import myDistSensor
import runLog

from di_sensors.easy_distance_sensor import EasyDistanceSensor
from time import sleep
import argparse
import time


# ARGUMENT PARSER
ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--file", required=True, help="path to input file")
ap.add_argument("-n", "--num", type=int, default=3, help="number of readings")
args = vars(ap.parse_args())
NUM_READINGS = args['num']

LOOP_DELAY = .01
NUM_AVERAGES = 3
egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
ds = myDistSensor.init(egpg)
#ds = EasyDistanceSensor(use_mutex=True)
distReadings = []
aveReadings = []
runLog.logger.info("Starting readDistSensor")
print("\nStart: "+time.strftime("%H:%M:%S"))
while True:
    distReading = ds.read_mm()
    distReadings += [distReading]
    #print("Reading: %d  %d mm" % (len(distReadings),distReading), end = '\r')
    if len(distReadings) == NUM_READINGS:
        print("Readings       : %d     " % len(distReadings))
        print("Reading Delay  : %1.3f s" % LOOP_DELAY)
        print("Average Reading: %.0f mm" % np.average(distReadings))
        print("Minimum Reading: %.0f mm" % np.min(distReadings))
        print("Maximum Reading: %.0f mm" % np.max(distReadings))
        print("Std Dev Reading: %.0f mm" % np.std(distReadings))
        print("Single Reading accuracy is +/-3*StdDev / average reading")
        print("Three SD readings vs ave reading: %.1f %%" % (3.0 * np.std(distReadings) / np.average(distReadings) *100.0))
        print("Averages usually vary +/- by 3xStdDev / sqrt(n)")
        print("Expected accuracy of average of %d readings: %.1f %%" % (NUM_READINGS, 3.0 * np.std(distReadings) / np.sqrt(NUM_READINGS) / np.average(distReadings) *100.0))
        print("Adjusted For Error Average Distance: %.0f mm" % myDistSensor.adjustReadingInMMForError(np.average(distReadings)))
        aveReadings   += [np.average(distReadings)]

        if len(aveReadings) == NUM_AVERAGES:
            print("\nAverage Average: %.0f mm" % np.average(aveReadings))
            print("Minimum Average: %.0f mm" % np.min(aveReadings))
            print("Maximum Average: %.0f mm" % np.max(aveReadings))
            print("Std Dev Average: %.0f mm" % np.std(aveReadings))
            print("Measured accuracy for averages of %d readings: +/-%.1f %%" % (NUM_READINGS,3.0 * np.std(aveReadings) / np.average(aveReadings) *100.0))
            print("****\n")
            aveReadings = []
            sleep(7)

        distReadings = [] # distReadings[0]
        print("\n"+time.strftime("%H:%M:%S"))

    sleep(LOOP_DELAY)
