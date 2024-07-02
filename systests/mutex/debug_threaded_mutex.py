#!/usr/bin/env python3

# FILE: treaded_mutex.py

# PURPOSE: Test with two threads using mutex

import threading
import traceback
import datetime as dt
import time
import numpy.random as nprand
from I2C_mutex import Mutex
# import fcntl

DEBUG = True
mutex = Mutex(debug=False)

DexterLockI2C_handle = open('/run/lock/DexterLockI2C')

def print_w_date_time(alert,event_time=None):
    if event_time is None: event_time = dt.datetime.now()
    str_event_time = event_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    thread_name = threading.current_thread().name
    print("{} {}: {}".format(str_event_time,thread_name,alert))

class UseMutex(threading.Thread):
    def __init__(self,name="not_set"):
        threading.Thread.__init__(self)
        self.name = name
        self.exitFlag = False
        time.sleep(nprand.uniform(1.0,3.0))
        mutex.acquire()
        self.count = 1
        mutex.release()
        print_w_date_time("UseMutex {} Initialized".format(self.name))

    def run(self):
        while (self.exitFlag is not True):
            try:
                mutex.acquire()
                if DEBUG: print_w_date_time("acquired")
                self.count += 1
                mutex.release()
                if DEBUG: print_w_date_time("released")
                if ((self.count % 10) == 2):
                    print_w_date_time("{} count: {}".format(self.name, self.count))
                time.sleep(nprand.uniform(0.1,0.5))
            except KeyboardInterrupt:
                print_w_date_time("caught KeyboardInterrupt")
                break
            except Exception as e:
                print_w_date_time("Exception"+str(e))
                traceback.print_exc()
                break
        print_w_date_time("exitFlag set, stopping thread")

def main():


    print_w_date_time("Starting")

    t1 = UseMutex(name="T1")
    t2 = UseMutex(name="T2")
    t1.start()
    t2.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("\nClosing Threads")
            t1.exitFlag = True
            t2.exitFlag = True
            t1.join()
            t2.join()
            break
    print_w_date_time("Exiting")



if __name__ == '__main__': main()

