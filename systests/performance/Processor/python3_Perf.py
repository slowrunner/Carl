#!/usr/bin/env python3
#
# python3_Perf.py
#
# Measure performance of some python3 calls
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

print("About to test integer addition")
time.sleep(1)
a=1
b=2
c=0
start_pc=time.perf_counter()
for a in range(1,4000):
    c = a + b
end_pc=time.perf_counter()
# print("integer c = a + b: %f ms \n" % ((end_pc - start_pc)*1000) )
print("4000 x integer c = a + b: %f ms \n" % ((end_pc - start_pc)*1000) )
print("integer c = a + b: %f ms \n" % ((end_pc - start_pc)*1000/4000.0) )

print("About to test float addition")
time.sleep(1)
a=2.0
b=4.0
c=0.0
start_pc=time.perf_counter()
for i in range(1,4000):
    # c = a + b
    c = float(i) + b
end_pc=time.perf_counter()
# print("float c = a + b: %f ms \n" % ((end_pc - start_pc)*1000) )
print("4000 x float c = a + b: %f ms \n" % ((end_pc - start_pc)*1000) )
print("float c = a + b: %f ms \n" % ((end_pc - start_pc)*1000/4000.0) )

print("Done!")
