#!/usr/bin/env python3

####################################################
# This companion file tests if EasyGoPiGo3 instances share variables
#
# Run it in parallel with text_gopigo_vars.py
#
# This sets speed to 100 every second until it sees speed equal 1 or ctrl-c
# then sets speed to 2 and quits
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
from di_mutex import DI_Mutex
from easygopigo3 import EasyGoPiGo3


print("\ntest_gopigo_vars_2 running")
egpg_mutex = DI_Mutex("egpg")

egpg = EasyGoPiGo3(use_mutex = True)
b4test_speed = egpg.get_speed()
print("Speed before test:", b4test_speed)

while True:
    try:
        egpg_mutex.acquire()
        speed = egpg.get_speed()
        print("speed:",speed)
        if speed != 1:
            egpg.set_speed(102)
            print("speed set to",egpg.get_speed())
            egpg_mutex.release()
            time.sleep(1)
        else:
            egpg_mutex.release()
            break
    except KeyboardInterrupt:
        egpg_mutex.release()
        break
    except Exception as e:
        print(e)

egpg_mutex.acquire()
egpg.set_speed(2)
print("\nchanged speed to",egpg.get_speed())
egpg_mutex.release()
time.sleep(1)
print("instance 2 done")
