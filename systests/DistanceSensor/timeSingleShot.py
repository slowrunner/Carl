#!/usr/bin/env python
#

from __future__ import print_function
from __future__ import division


from di_sensors.distance_sensor import DistanceSensor
import time

print("\nExample program for timing a single read of the Dexter Industries Distance Sensor.")

ds = DistanceSensor()

for i in range(10):
  # read the distance as a single-shot sample
  start=time.clock()
  read_distance = ds.read_range_single()
  timing=time.clock() - start
  print("Distance from object: {} mm".format(read_distance))
  print("Timing: {:.3f}".format(timing))
  time.sleep(1)