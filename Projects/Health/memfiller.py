#!/usr/bin/env python3

import os
import psutil

PROCESS = psutil.Process(os.getpid())
MEGA = 10 ** 6
MEGA_STR = ' ' * MEGA


def pmem():
    try:
        # print(psutil.virtual_memory())
        # total, available, percent, used, free, active, inactive, buffers, cached, shared, slab)
        tot, avail, percent, used, free, active, inactive, buffers = psutil.virtual_memory()
    except ValueError:
        tot, avail, percent, used, free, active, inactive, buffers, cached, shared, slab = psutil.virtual_memory()
    tot, avail, used, free = tot / MEGA, avail / MEGA, used / MEGA, free / MEGA
    proc = PROCESS.memory_info()[1] / MEGA
    print('process = %s total = %s avail = %s used = %s free = %s percent = %s'
          % (proc, tot, avail, used, free, percent))


def alloc_max_array():
    i = 0
    ar = []
    while True:
        try:
            #ar.append(MEGA_STR)  # no copy if reusing the same string!
            ar.append(MEGA_STR + str(i))
        except MemoryError:
            break
        i += 1
    max_i = i - 1
    print('maximum array allocation:', max_i)
    pmem()


def alloc_max_str():
    i = 0
    while True:
        try:
            a = ' ' * (i * 10 * MEGA)
            del a
        except MemoryError:
            break
        i += 1
    max_i = i - 1
    _ = ' ' * (max_i * 10 * MEGA)
    print('maximum string allocation', max_i)
    pmem()

pmem()
alloc_max_str()
alloc_max_array()
pmem()
