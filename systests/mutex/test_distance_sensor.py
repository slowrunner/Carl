#!/usr/bin/env python3

####################################################
# This file contains a short test to determine
#     if it is possible to access the distance sensor
#     from two separate processes using mutex.
# Run in parallel with test_distance_sensor_2.py
####################################################

import time
import traceback
import datetime as dt
import easygopigo3 as easy

egpg = easy.EasyGoPiGo3(use_mutex=True)

my_Distance_portI2C = egpg.init_distance_sensor()
time.sleep(0.1)

def print_w_date_time(alert,event_time=None):
    if event_time is None: event_time = dt.datetime.now()
    str_event_time = event_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print("{} test_distance_sensor.py: {}".format(str_event_time,alert))


# start()
print_w_date_time("Starting - printing distance every 10 readings")
loop_cnt = 0
while True:
        loop_cnt += 1
        try:
            dist =  my_Distance_portI2C.read_mm()
            if ((loop_cnt % 10) == 1):
                print_w_date_time("{:.0f} mm".format(dist))
        except KeyboardInterrupt:
            print("\nExiting")
            exit(0)
        except Exception as e:
            print_w_date_time("Exception: " + str(e))
            traceback.print_exc()
        if dist == 0:
            exit(1)
        time.sleep(0.01)

