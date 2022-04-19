#!/usr/bin/env python3

import atexit
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

def module_stop():
    logging.info("module_stop() executed")

atexit.register(module_stop)



