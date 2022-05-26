#!/usr/bin/python3
#
# distSensorError.py

"""
Continuously measure distance in millimeters, printing the average and individual readings
"""


import numpy as np

SAMPLES = 300

from di_sensors.easy_distance_sensor import EasyDistanceSensor
from time import sleep

ds = EasyDistanceSensor(use_mutex=True)
distReadings = []

while True:
    distReadings += [ds.read_mm()]
    if (len(distReadings)>(SAMPLES-1) ):  del distReadings[0]
    print("\nDistance Readings:",len(distReadings))
    ave =  np.average(distReadings)
    min =  np.min(distReadings)
    max = np.max(distReadings)
    minError = (min-ave)/ave * 100.0
    maxError = (max-ave)/ave * 100.0
    print("Average Reading: %.0f mm" % ave)
    print("Minimum Reading: {:.0f} mm  Min Error: {:.2f}%".format(min,minError))
    print("Maximum Reading: {:.0f} mm  Max Error: {:.2f}%".format(max,maxError))
    print("Std Dev Reading: %.0f mm" % np.std(distReadings))
    print("Three SD as a percent of reading: %.1f %%" % (3.0 * np.std(distReadings) / np.average(distReadings) *100.0))
    sleep(1)

