#!/usr/bin/env python
#
# python_Perf.py
#
# Measure performance of some python2 calls
# Method:  Use timeit.default_timer()
#
# force Python3 compatibility for print, integer division, and input()
from __future__ import print_function
from __future__ import division
from builtins import input

# import the time library for sleep(), perf_counter() and process_time()
import time
import timeit


print("About to test integer addition")
time.sleep(1)
a=1
b=2
c=0
start_pc=timeit.default_timer()
c = a + b
end_pc=timeit.default_timer()
print("integer c = a + b: %f ms \n" % ((end_pc - start_pc)*1000) )

print("About to test float addition")
time.sleep(1)
a=2.0
b=4.0
c=0.0
start_pc=timeit.default_timer()
c = a + b
end_pc=timeit.default_timer()
print("float c = a + b: %f ms \n" % ((end_pc - start_pc)*1000) )


print("Done!")
