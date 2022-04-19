#!/usr/bin/env python3

"""
# FILE:  forward_test.py

# PURPOSE:  Test VirtualBumper for GoPiGo3 forward()

"""

from easygopigo3 import EasyGoPiGo3
from virtualbumper import VirtualBumper
from time import sleep
import logging
import atexit

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

def main():

    logging.info("=== VIRTUAL BUMPERS FORWARD TEST ===")

    egpg = EasyGoPiGo3(use_mutex=True)
    atexit.register(egpg.stop)
    egpg.bumper = VirtualBumper(egpg)

    egpg.set_speed(300)

    emergency_stop = False

    BUMPER_CHECK_RATE = 15  # times per second
    drive_time = 2  # seconds

    egpg.forward()
    logging.info("*** forward({}) test checking bumper {} times per second ***".format(drive_time, BUMPER_CHECK_RATE))
    for i in range(int(drive_time * BUMPER_CHECK_RATE)):
        if egpg.bumper.bumped() == True:
            egpg.stop()
            logging.info("*** EMERGENCY STOP ***")
            emergency_stop = True
            break
        sleep(1.0/BUMPER_CHECK_RATE)

    if not emergency_stop:
        egpg.stop()
        logging.info("*** normal stop() ***")


if __name__ == "__main__": main()

