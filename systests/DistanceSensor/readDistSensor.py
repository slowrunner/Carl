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
    distReadings += [myDistSensor.adjustForAveErrorInMM(ds.read_mm())]
    if (len(distReadings)>9 ):  del distReadings[0]
    print("\nDistance Readings:",distReadings)
    print("Average Distance: %.0f mm" % np.average(distReadings))
    sleep(1)
