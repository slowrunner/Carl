#!/usr/bin/env python3

# FILE: treaded_dist_sensor.py

# PURPOSE: Test with two threads using distance sensor

import threading
import traceback
import datetime as dt
import time
import numpy.random as nprand
import easygopigo3 as easy
import subprocess
from pathlib import Path

from I2C_mutex import Mutex

Path('/run/lock/GoPiGo3_Dist_Sensor').touch()

# subprocess.call(['sudo', 'touch', '/run/lock/GoPiGo3_Dist_Sensor'])

mutex = Mutex(debug=False)


DexterLockI2C_handle = open('/run/lock/GoPiGo3_Dist_Sensor')





def print_w_date_time(alert,event_time=None):
    if event_time is None: event_time = dt.datetime.now()
    str_event_time = event_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    thread_name = threading.current_thread().name
    print("{} {}: {}".format(str_event_time,thread_name,alert))

class CheckDist(threading.Thread):
    def __init__(self,ds,name="not_set"):
        threading.Thread.__init__(self)
        self.name = name
        self.exitFlag = False
        time.sleep(nprand.uniform(1.0,3.0))
        self.count = 1
        self.ds = ds
        print_w_date_time("CheckDist {} Initialized".format(self.name))

    def run(self):
        while (self.exitFlag is not True):
            try:
                self.count += 1
                mutex.acquire()
                self.reading = self.ds.read_mm()
                mutex.release()
                if ((self.count % 10) == 2):
                    print_w_date_time("count: {} dist: {:.0f}".format(self.count,self.reading))
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

    egpg = easy.EasyGoPiGo3(use_mutex=True)

    try:
        easyds = egpg.init_distance_sensor(port='RPI_1')
    except Exception as e:
        print_w_date_time("Exception initializing  dist sensor: " + str(e))
        traceback.print_exc()
        exit(1)

    t1 = CheckDist(ds=easyds, name="T1")
    t2 = CheckDist(ds=easyds, name="T2")
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

