#!/usr/bin/env python3

"""
  Threading example that will
  - Provide a thread exception traceback
  - Re-raise a thread exception for handling in the main
  - Handle a main thread exception
  - Handle a thread thread exception
  - Allow Main to tell thread to exit

Note: if the thread is waiting on I/O it will not be polling for exitFlag
      that case requires setting up a blocking I/O operation with a timeout
      not included in this example.
      See: https://www.geeksforgeeks.org/start-and-stop-a-thread-in-python/
"""

# Importing the modules
import threading
# import sys
import traceback
import logging
import time

# Custom Thread Class
class MyThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)    # Do the normal thread initialization
        self.exitFlag = False              # used by main to tell thread to exit


    # Function that raises the exception
    def threadFunction(self):
        logging.info("%s: Doing thread stuff", self.name)
        time.sleep(2)

        # force thread exception (comment out to try main-tells-thread-to-exit case)
        logging.info("%s Causing an exception in thread ",self.name)
        raise Exception("BadBoy")

        # if thread wants to complete, it can tell itself to stop
        logging.info("%s: Complete - telling self to exit", self.name)
        self.exitFlag = True    # (Will not happen due to divbyzero exception in this example)

    def run(self):

        # Variable that stores the exception, if raised by threadFunction
        self.exc = None
        self.name = threading.current_thread().name
        try:
            while (self.exitFlag is not True):
              self.threadFunction()
            logging.info("%s: thread told to exit",self.name)

        except Exception as e:
            logging.info("%s: Printing traceback in the thread exception handler",self.name)
            traceback.print_exc()

            # now save the exception for later re-raising to the main
            self.exc = e

    def join(self):
        threading.Thread.join(self)
        # Since join() returns in caller thread
        # we re-raise the caught exception
        # if any was caught
        if self.exc:
            name = threading.current_thread().name
            logging.info("%s: re-raising exception in thread.join()", name)
            raise self.exc


# A MAIN Function
def do_some_main_stuff():
    logging.info("Doing Some Main Stuff")
    time.sleep(5)
    logging.info("Causing an exception in do_some_main_stuff()")
    divbyzero=1/0

# MAIN function
def main():

    # set up logger
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    # Wrap main in try/except/finally
    try:
      # Create a new Thread t
      # Here Main is the caller thread
      t = MyThread()
      t.start()
      do_some_main_stuff()
    except Exception as e:
      logging.info("Main(): handling main exception: %s",e)
      traceback.print_exc()
    finally:
      # clean up thread and handle any thread exception in this main thread
      try:
          logging.info("Main(): telling thread to exit if has not already")
          t.exitFlag = True
          logging.info("Main(): waiting for thread exit")
          t.join()
      except Exception as e:
          logging.info("Main: Thread Exception Handler in Main, Details of the Thread Exception: %s", e)
    logging.info("Main: Main normal exit")

if __name__ == '__main__':
    main()
