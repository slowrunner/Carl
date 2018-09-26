#!/usr/bin/env python
#
# timeContinuous.py    Time EasyDistanceSensor.read_mm()
#
# Result: RPi3B  1.2MHz 4core   average 10ms
#
from __future__ import print_function
from __future__ import division


from di_sensors.distance_sensor import DistanceSensor
import time
import numpy as np

print("\nTiming continuous reading of the Dexter Industries Distance Sensor.")

cds = DistanceSensor()
cds.start_continuous()

delay_l = [0.0, 0.001, 0.005, 0.010, 0.020, 0.025, 0.030, 0.050, 0.100]
for delay in delay_l:
  timing_l = []
  dist_l = []
  for i in range(10):
    # read the distance
    start=time.clock()
    read_distance = cds.read_range_continuous()
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
  print("DistanceSensor.read_range_continuous Average Time: {:.0f} ms\n\n".format(np.mean(timing_l)*1000))
