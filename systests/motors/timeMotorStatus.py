#!/usr/bin/env python
#
# timeMotorStatus.py    Time GoPiGo3.get_motor_status()
#
# Result: RPi3B  1.2MHz 4core   average 110ns for two (left and right) 
#
from __future__ import print_function
from __future__ import division


import easygopigo3
import time
import numpy as np

print("\nTiming get_motor_status().")

egpg = easygopigo3.EasyGoPiGo3(use_mutex = True)


delay_l = [0.0, 0.001, 0.005, 0.010, 0.100, 0.500, 1.0, 2.0]
for delay in delay_l:
  timing_l = []
  for i in range(10):
    # Get_Motor_Status
    start=time.clock()
    left_motor_status = egpg.get_motor_status(egpg.MOTOR_LEFT)
    right_motor_status = egpg.get_motor_status(egpg.MOTOR_RIGHT)
    timing=time.clock() - start
    timing_l += [timing]
    print("Timing: {:.6f}".format(timing))
    time.sleep(delay)
  print("\nDelay between readings: {:.0f}ms".format(delay*1000))
  print("2x get_motor_status() Average Time: {:.0f} ns\n\n".format(np.mean(timing_l)*1000000))