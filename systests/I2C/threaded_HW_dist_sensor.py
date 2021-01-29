#!/usr/bin/env python3

# FILE: treaded_HW_dist_sensors.py

# PURPOSE: Test with two threads reading the distance sensor, both HW I2C

import threading
import traceback
import datetime as dt
import time
import numpy.random as nprand
import easygopigo3 as easy

def print_w_date_time(alert,event_time=None):
    if event_time is None: event_time = dt.datetime.now()
    str_event_time = event_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    thread_name = threading.current_thread().name
    print("{} {}: {}".format(str_event_time,thread_name,alert))

class CheckDistSensor(threading.Thread):
    def __init__(self,port="RPI_1",egpg=None,name="not_set"):
        threading.Thread.__init__(self)
        self.exitFlag = False
        if egpg is None:
            time.sleep(nprand.uniform(1.0,3.0))
            self.egpg = easy.EasyGoPiGo3(use_mutex=True)
            time.sleep(0.1)  # allow for hardware init to complete
        else:
            self.egpg = egpg
        self.ds  = self.egpg.init_distance_sensor(port=port)
        print_w_date_time("CheckDistSensor Initialized on port {}".format(port))
        self.name = name

    def run(self):
        while (self.exitFlag is not True):
            try:
                self.reading = self.ds.read_mm()
                print_w_date_time("distance: {:.0f}".format(self.reading))
                time.sleep(nprand.uniform(0.1,0.2))
            except KeyboardInterrupt:
                print_w_date_time("caught KeyboardInterrupt")
                break
            except Exception as e:
                print_w_date_time("Exception"+str(e))
                traceback.print_exc()
                self.reading = 0
                break
        print_w_date_time("exitFlag set, stopping thread")

def main():
    print_w_date_time("Starting")
    egpg = easy.EasyGoPiGo3(use_mutex=True)

    t1 = CheckDistSensor(name="HW_i2c_1",egpg=egpg,port="RPI_1")
    t2 = CheckDistSensor(name="HW_i2c_2",egpg=egpg,port="RPI_1")
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

