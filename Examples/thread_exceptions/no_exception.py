#!/usr/bin/env python3

# One Thread, no exception in main or thread

"""
If main() does not wait for thread to finish with a join(),
  then main will exit, then thread will exit:


21:55:19: Main    : before creating thread
21:55:19: Main    : before running thread
21:55:19: Thread 1: starting
21:55:19: Main    : wait for the thread to finish
21:55:19: Main    : all done
21:55:21: Thread 1: finishing

If main() does wait for thread to finish with a join(),
  thread will exit, then main will exit:

21:56:25: Main    : before creating thread
21:56:25: Main    : before running thread
21:56:25: Thread 1: starting
21:56:25: Main    : wait for the thread to finish
21:56:27: Thread 1: finishing
21:56:27: Main    : all done

"""

import logging
import threading
import time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,))
    logging.info("Main    : before running thread")
    x.start()

    # comment out one line
    # wait=True
    wait=False

    if (wait==True):  # Keep Main alive until thread finishes
      logging.info("Main    : wait for the thread to finish with join()")
      x.join()


    logging.info("Main    : all done")
