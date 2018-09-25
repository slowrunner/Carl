#!/usr/bin/env python
#

from __future__ import print_function
from __future__ import division


from di_sensors.distance_sensor import DistanceSensor
import time
import numpy as np

print("\nExample program for timing a single read of the Dexter Industries Distance Sensor.")

ds = DistanceSensor()

timing_l = []

for i in range(10):
  # read the distance as a single-shot sample
  start=time.clock()
  read_distance = ds.read_range_single()
  timing=time.clock() - start
  timing_l += [timing]
  print("Distance from object: {} mm".format(read_distance))
  print("Timing: {:.3f}".format(timing))
  time.sleep(1)
print("\nAverage Time: {:.0f} ms".format(np.mean(timing_l)*1000))
