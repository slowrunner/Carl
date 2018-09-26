#!/usr/bin/env python
#
# timeEasyDS.py    Time EasyDistanceSensor.read_mm()
#
# Result: RPi3B  1.2MHz 4core   average 66ms 
#
from __future__ import print_function
from __future__ import division


from di_sensors.easy_distance_sensor import EasyDistanceSensor
import time
import numpy as np

print("\nExample program for timing a single read of the Dexter Industries Easy Distance Sensor.")

eds = EasyDistanceSensor()
delay_l = [0.0, 0.001, 0.005, 0.010, 0.100, 1.0]
for delay in delay_l:
  timing_l = []
  dist_l = []
  for i in range(10):
    # read the distance as a single-shot sample
    start=time.clock()
    read_distance = eds.read_mm()
    timing=time.clock() - start
    timing_l += [timing]
    dist_l += [read_distance]
    print("Distance from object: {} mm".format(read_distance))
    print("Timing: {:.3f}".format(timing))
    time.sleep(delay)
  mean_dist = np.mean(dist_l)
  var_dist = np.var(dist_l)
  print("\nDelay between readings: {:.0f}ms".format(delay*1000))
  print("Distance Mean: {:.1f}mm Variance: {:.1f}mm  {:.1f}%".format(mean_dist,var_dist,var_dist/mean_dist*100))
  print("EasyDistanceSensor.read_mm Average Time: {:.0f} ms\n\n".format(np.mean(timing_l)*1000))
