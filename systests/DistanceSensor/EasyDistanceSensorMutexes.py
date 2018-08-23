#!/usr/bin/env python
#
# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python example program for the Dexter Industries Temperature Humidity Pressure Sensor

from __future__ import print_function
from __future__ import division

# do the import stuff
from di_sensors.easy_distance_sensor import EasyDistanceSensor
from time import time, sleep
from threading import Thread, Event, get_ident

# instantiate the distance object
my_sensor = EasyDistanceSensor(use_mutex = True)
start_time = time()
runtime = 2.0
# create an event object for triggering the "shutdown" of each thread
stop_event = Event()

# target function for each thread
def readingSensor():
    while not stop_event.is_set():
      thread_id = get_ident()
      distance = my_sensor.read()
      print("Thread ID = {} with distance value = {}".format(thread_id, distance))
      sleep(0.001)

# create an object for each thread
thread1 = Thread(target = readingSensor)
thread2 = Thread(target = readingSensor)

# and then start them
thread1.start()
thread2.start()

# let it run for [runtime] seconds
while time() - start_time <= runtime:
    sleep(0.1)

# and then set the stop event variable
stop_event.set()

# and wait both threads to end
thread1.join()
thread2.join()
