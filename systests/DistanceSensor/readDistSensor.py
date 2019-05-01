#!/usr/bin/env python
#
# readDistSensor.py

"""
Continuously measure distance in millimeters, printing the average and individual readings
"""

from __future__ import print_function
from __future__ import division

import sys
sys.path.append('/home/pi/Carl/plib')
import numpy as np
import myDistSensor

from di_sensors.easy_distance_sensor import EasyDistanceSensor
from time import sleep

ds = EasyDistanceSensor(use_mutex=True)
distReadings = []

while True:
    distReadings += [ds.read_mm()]
    if (len(distReadings)>9 ):  del distReadings[0]
    print("\nDistance Readings:",distReadings)
    print("Average Reading: %.0f mm" % np.average(distReadings))
    print("Minimum Reading: %.0f mm" % np.min(distReadings))
    print("Maximum Reading: %.0f mm" % np.max(distReadings))
    print("Std Dev Reading: %.0f mm" % np.std(distReadings))
    print("Adjusted For Error Average Distance: %.0f mm" % myDistSensor.adjustReadingInMMForError(np.average(distReadings)))
    print("Three SD as a percent of reading: %.1f %%" % (3.0 * np.std(distReadings) / np.average(distReadings) *100.0))
    sleep(1)
