#!/usr/bin/env python3

####################################################
# This file proves EasyGoPiGo3 instances do not share variables
#
# Run it in parallel with text_gopigo_vars_2.py
#
# This reads speed every second, until cntrl-c
# then sets speed to 1 and 
# waits for speed change or second cntrl-c
# then restores speed before test and quits
#
# Usage:
#     In 1st console:  ./test_gopigo_vars.py  
#     In 2nd console:  ./test_gopigo_vars_2.py
#     See that 1st console never changes
#     In 1st console:  cntl-c
#     See that 2nd console does not see 1st object's change
#     In 2nd console:  cntl-c
#     See that 1st console does not see 2nd object's change
#     In 1st console:  cntl-c
####################################################
import time
# from I2C_mutex import Mutex
from di_mutex import DI_Mutex
import fcntl
from easygopigo3 import EasyGoPiGo3

egpg_mutex = DI_Mutex("egpg")

egpg = EasyGoPiGo3(use_mutex = True)
b4test_speed = egpg.get_speed()
print("Speed before test:", b4test_speed)

while True:
    try:
        egpg_mutex.acquire()
        print("current speed:", egpg.get_speed())
        egpg_mutex.release()
        time.sleep(1)
    except KeyboardInterrupt:
        egpg_mutex.release()
        egpg_mutex.acquire()
        egpg.set_speed(1)
        egpg_mutex.release()
        break
    except Exception as e:
        print(e)

while egpg.get_speed() == 1:
    try:
        print("waiting for speed change")
        time.sleep(1)
    except KeyboardInterrupt:
        break

print("Restoring speed to:",b4test_speed)
egpg.set_speed(b4test_speed)
time.sleep(1)
print("instance 1 done")
