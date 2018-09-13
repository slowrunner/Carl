#!/usr/bin/env python
#

from __future__ import print_function
from __future__ import division


from di_sensors.distance_sensor import DistanceSensor
import time

print("\nExample program for timing continuous mode reads of the Dexter Industries Distance Sensor.")

ds = DistanceSensor()
ds.start_continuous()

for i in range(10):
  # read the distance as a single-shot sample
  start=time.clock()
  read_distance = ds.read_range_continuous()
  timing=time.clock() - start
  print("Distance from object: {} mm".format(read_distance))
  print("Timing: {:.3f}".format(timing))
  # delay for 1/2 single read timing to ensure a new reading each time
  # (repeat test, increasing delay from 0.001 until no repeats seen in timings)
  time.sleep(0.005)
