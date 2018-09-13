#!/usr/bin/env python
#

from __future__ import print_function
from __future__ import division


from di_sensors.distance_sensor import DistanceSensor
import timeit
import time

print("\nExample program for timing a single read of the Dexter Industries Distance Sensor.")

ds = DistanceSensor(use_mutex=True)

timeit_setup = '''
from di_sensors.distance_sensor import DistanceSensor
ds = DistanceSensor()
'''

timeit_code = '''
read_distance = ds.read_range_single()
'''
    
# read the distance as a single-shot sample
read_distance = ds.read_range_single()
print("Distance from object: {} mm".format(read_distance))
time.sleep(1)
print("Timings for ds.read_range_single()"
print timeit.repeat(setup = timeit_setup,
	      stmt = timeit_code,
	      number = 10,
	      repeat)
