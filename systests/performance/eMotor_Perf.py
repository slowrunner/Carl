#!/usr/bin/env python
#
# eMotors_Perf.py
#
# Measure performance of some motor API calls
# Method:  Use time.perf_counter() and time.process_time() to measure asynchronous motor commands
#          perf_counter() measures total elapsed time including sleep
#          process_time() measures sys and user time not including sleep
#
# force Python3 compatibility for print, integer division, and input()
from __future__ import print_function
from __future__ import division
from builtins import input

# import the time library for sleep(), perf_counter() and process_time()
import time

# import the EasyGoPiGo3 module
import easygopigo3 as easy
import sys
import atexit

# Create an instance egpg of the EasyGoPiGo3 class.
egpg = easy.EasyGoPiGo3()
atexit.register(egpg.stop)   #setup a call to egpg.stop() when exiting program

# Make sure bot is ready and waiting
egpg.reset_all()
time.sleep(1)  # for reset to finish


print("About to command motors fwd")
time.sleep(1)
start_pc=time.perf_counter()
egpg.forward()
end_pc=time.perf_counter()
print("EasyGoPiGo3.forward() perf_counter time: %f ms \n" % (end_pc - start_pc)*1000 )

print("Stopping the motors after 1 second.")
time.sleep(1)
start_pc=time.perf_counter()
gpg.stop()
end_pc=time.perf_counter()
print("EasyGoPiGo3.stop() perf_counter time: %f ms \n" % (end_pc - start_pc)*1000 )

print("About to command motors bwd")
time.sleep(1)
start_pc=time.perf_counter()
egpg.backward()
end_pc=time.perf_counter()
print("EasyGoPiGo3.backward() perf_counter time: %f ms \n" % (end_pc - start_pc)*1000 )

print("Stopping the motors after 1 second.")
time.sleep(1)
start_pc=time.perf_counter()
gpg.stop()
end_pc=time.perf_counter()
print("EasyGoPiGo3.stop() perf_counter time: %f ms \n" % (end_pc - start_pc)*1000 )

print("EasyGoPiGo3.reset_all()")
egpg.reset_all()
time.sleep(1)  # allow time for reset to complete
print("Done!")
