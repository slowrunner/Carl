#!/usr/bin/env python3

# Handle a thread exception in the main

# Importing the modules
import threading
# import sys
import traceback
import logging


# Custom Thread Class
class MyThread(threading.Thread):

  # Function that raises the exception
    def someFunction(self):
        name = threading.current_thread().name
        logging.info("%s Causing an exception in thread ",name)
        divbyzero=1/0

    def run(self):

        # Variable that stores the exception, if raised by someFunction
        self.exc = None
        try:
            self.someFunction()
        except Exception as e:
            name = threading.current_thread().name
            logging.info("%s: Printing traceback in the thread exception handler",name)
            traceback.print_stack()

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

# MAIN function
def main():

    # set up logger
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")


    # Create a new Thread t
    # Here Main is the caller thread
    t = MyThread()
    t.start()

    # Exception handled in main thread
    try:
        t.join()
    except Exception as e:
        logging.info("Exception Handled in Main, Details of the Exception: %s", e)

if __name__ == '__main__':
    main()
