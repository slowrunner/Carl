#!/usr/bin/env python3

# Compare single proc vs multiple procs execution for io bound operation

"""
Typical Result:
  Starting 4000 cycles of io-bound processing
  Sequential - run time: 39.74 seconds
  4 procs Parallel - run time: 17.68 seconds
  2 procs Parallel twice - run time: 20.68 seconds
"""
import time
import multiprocessing as mp

# one thousand
cycles = 1 * 1000

def t():
        with open('/dev/urandom', 'rb') as f:
                for x in range(cycles):
                        f.read(4 * 65535)

if __name__ == '__main__':
    print("  Starting {} cycles of io-bound processing".format(cycles*4))
    start_time = time.time()
    t()
    t()
    t()
    t()
    print("  Sequential - run time: %.2f seconds" % (time.time() - start_time))

    # four procs
    start_time = time.time()
    p1 = mp.Process(target=t)
    p2 = mp.Process(target=t)
    p3 = mp.Process(target=t)
    p4 = mp.Process(target=t)
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    print("  4 procs Parallel - run time: %.2f seconds" % (time.time() - start_time))

    # two procs
    start_time = time.time()
    p1 = mp.Process(target=t)
    p2 = mp.Process(target=t)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    p3 = mp.Process(target=t)
    p4 = mp.Process(target=t)
    p3.start()
    p4.start()
    p3.join()
    p4.join()
    print("  2 procs Parallel twice - run time: %.2f seconds" % (time.time() - start_time))



