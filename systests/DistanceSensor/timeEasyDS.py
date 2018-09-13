#!/usr/bin/env python
#

from __future__ import print_function
from __future__ import division


from di_sensors.easy_distance_sensor import EasyDistanceSensor
import time

print("\nExample program for timing a single read of the Dexter Industries Easy Distance Sensor.")

eds = EasyDistanceSensor()

for i in range(10):
  # read the distance as a single-shot sample
  start=time.clock()
  read_distance = eds.read_mm()
  timing=time.clock() - start
  print("Distance from object: {} mm".format(read_distance))
  print("Timing: {:.3f}".format(timing))
  time.sleep(1)
