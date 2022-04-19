#!/usr/bin/env python3


import logging
import modulewithatexit
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')


logging.info("main started")
time.sleep(2)
# force unhandled exception
raise
