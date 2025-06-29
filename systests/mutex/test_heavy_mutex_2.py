#!/usr/bin/env python3

####################################################
# This file tests the mutex class
# Run it in parallel with text_heavy_mutext_2.py
# in order to verify that mutex is functional.
# This one acquires and releases every 5 seconds
# the other one is every half second
####################################################
import time
from I2C_mutex import Mutex
import fcntl
import datetime as dt

mutex = Mutex(debug=False)

def print_w_date_time(alert,event_time=None):
    if event_time is None: event_time = dt.datetime.now()
    str_event_time = event_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    thread_name = __file__
    print("{} {}: {}".format(str_event_time,thread_name,alert))


DexterLockI2C_handle = open('/run/lock/DexterLockI2C')

while True:
    try:
        mutex.acquire()
        print_w_date_time("acquired")
        time.sleep(5)
        print_w_date_time("released\n")
        mutex.release()
    except KeyboardInterrupt:
        mutex.release()
        exit()
    except Exception as e:
        print(e)
