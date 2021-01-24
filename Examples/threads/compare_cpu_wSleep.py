#!/usr/bin/env python3

# Compare single threaded vs multi-threaded execution for cpu bound operation
# with a sleep to allow other threads to run

"""
Typical Result:
  Starting 4000000 cycles of cpu-only threading with a yield
  Sequential run time: 20.88 seconds
  4 threads Parallel run time: 69.21 seconds
  2 threads Parallel twice - run time: 32.62 seconds
"""
import time
import threading

# one million
cycles = 1000 * 1000

def t():
    for x in range(cycles):
        fdivision = cycles / 2.0
        fcomparison = (x > fdivision)
        faddition = fdivision + 1.0
        fsubtract = fdivision - 2.0
        fmultiply = fdivision * 2.0
        time.sleep(0)

if __name__ == '__main__':
    print("  Starting {} cycles of cpu-only threading with a yield".format(cycles*4))
    start_time = time.time()
    t()
    t()
    t()
    t()
    print("  Sequential run time: %.2f seconds" % (time.time() - start_time))

    # four threads
    start_time = time.time()
    t1 = threading.Thread(target=t)
    t2 = threading.Thread(target=t)
    t3 = threading.Thread(target=t)
    t4 = threading.Thread(target=t)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    print("  4 threads Parallel run time: %.2f seconds" % (time.time() - start_time))


    # two threads
    start_time = time.time()
    t1 = threading.Thread(target=t)
    t2 = threading.Thread(target=t)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    t3 = threading.Thread(target=t)
    t4 = threading.Thread(target=t)
    t3.start()
    t4.start()
    t3.join()
    t4.join()
    print("  2 threads Parallel twice - run time: %.2f seconds" % (time.time() - start_time))

