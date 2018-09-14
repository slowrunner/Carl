#!/usr/bin/env python

# TEST cost of one list concat, vs computing average

from __future__ import print_function

import timeit

setitup = '''
y_list = []
x_list = []
ave_list = []
'''


concat_list = '''
for x in range(720):
  y = -(x + 3)
  y_list += [x]
  x_list += [y]
'''

ave_values = '''
for x in range(720):
  y = -(x + 3)
  ave_list += [(abs(x) + abs(y)) * 0.5]
'''

print("concat_list:", timeit.timeit(setup=setitup, stmt=concat_list, number=10000)/10000)
print("ave_values: ", timeit.timeit(setup=setitup, stmt=ave_values,  number=10000)/10000)



   
