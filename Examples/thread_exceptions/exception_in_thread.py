#!/usr/bin/env python3

# One Thread, exception in thread

# Threads exit at completion or with uncaught exceptions

"""
If main() does not wait for thread to finish with a join(),
  then main will exit, then thread will exit with exception:


22:11:30: Main    : before creating thread
22:11:30: Main    : before running thread
22:11:30: Thread 1: starting
22:11:30: Main    : all done     <----- MAIN EXITED W/O WAITING - no join()
22:11:32: Thread 1: raising div by zero exception
Exception in thread Thread-1:
Traceback (most recent call last):
  File "/usr/lib/python3.7/threading.py", line 917, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.7/threading.py", line 865, in run
    self._target(*self._args, **self._kwargs)
  File "./exception_in_thread.py", line 49, in thread_function
    e=1/0
ZeroDivisionError: division by zero
     ----- THREAD EXITED DUE TO EXCEPTION



If main() does wait for thread to finish with a join(),
  thread will exit due to exception, then main will exit:

22:08:05: Main    : before creating thread
22:08:05: Main    : before running thread
22:08:05: Thread 1: starting
22:08:05: Main    : wait for the thread to finish with join()
22:08:07: Thread 1: raising div by zero exception
Exception in thread Thread-1:
Traceback (most recent call last):
  File "/usr/lib/python3.7/threading.py", line 917, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.7/threading.py", line 865, in run
    self._target(*self._args, **self._kwargs)
  File "./exception_in_thread.py", line 37, in thread_function
    e=1/0
ZeroDivisionError: division by zero  <--- THREAD EXITED DUE TO EXCEPTION

22:08:07: Main    : all done       <---- MAIN WAITED FOR THREAD TO EXIT 

"""

import logging
import threading
import time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: raising div by zero exception", name)
    e=1/0

    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,))
    logging.info("Main    : before running thread")
    x.start()

    wait=False
    # uncomment next line to force main() to wait for thread exit
    wait=True

    if (wait==True):  # Keep Main alive until thread finishes
      logging.info("Main    : wait for the thread to finish with join()")
      x.join()


    logging.info("Main    : all done")
