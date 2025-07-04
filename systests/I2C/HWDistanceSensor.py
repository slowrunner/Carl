#!/usr/bin/env python3
#
# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python example program for the Dexter Industries Distance Sensor
#  USING THE HARDWARE I2C

from __future__ import print_function
from __future__ import division

# import the modules
from di_sensors.easy_distance_sensor import EasyDistanceSensor
import time

# instantiate the distance object
my_sensor = EasyDistanceSensor(use_mutex=True, port='RPI_1')

print("Testing HW I2C using EasyDistanceSensor(use_mutx=True)")

count = 0
# and read the sensor iteratively
try:
  while True:
    count +=1
    read_distance = my_sensor.read_mm()
    if (count%10) == 1:
        print("{} {}:distance from object: {} mm".format(time.strftime("%H:%M:%S"),count,read_distance))

    time.sleep(0.1)
except KeyboardInterrupt:
  print("\n** Control-c Exit")

