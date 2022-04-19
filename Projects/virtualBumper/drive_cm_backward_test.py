#!/usr/bin/env python3

"""
# FILE:  drive_cm_backward_test.py

# PURPOSE:  Test VirtualBumper class for drive_cm() with negative distance

"""

from easygopigo3 import EasyGoPiGo3
from time import sleep
import logging
from virtualbumper import VirtualBumper
import atexit

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

# get_motor_status(left/right_motor) returns [Overloaded, Power, Encoder, speed]
OVERLOADED = 0
POWER = 1
ENCODER = 2
SPEED = 3


def main():

    logging.info("=== VIRTUAL BUMPERS DRIVE_CM BACKWARD TEST ===")

    egpg = EasyGoPiGo3(use_mutex=True)
    atexit.register(egpg.stop)           # force a stop to prevent runaway bot from unhandled exceptions

    egpg.bumper = VirtualBumper(egpg)

    egpg.set_speed(300)

    emergency_stop = False

    BUMPER_CHECK_RATE = 15  # times per second

    # test: drive 25 cm with virtual bumper
    drive_dist_cm = -25
    egpg.drive_cm(drive_dist_cm, blocking=False)
    logging.info("*** drive_cm({}) checking virtual bumper {} times per second ***".format(drive_dist_cm, BUMPER_CHECK_RATE))

    # while wheels are turning, check if bumped into something
    while True:
        if egpg.bumper.bumped() == True:
            egpg.stop()
            logging.info("*** EMERGENCY STOP ***")
            emergency_stop = True
            break
        # check if reached target distance (both wheels stop)
        if (egpg.get_motor_status(egpg.MOTOR_LEFT)[SPEED] == 0) and (egpg.get_motor_status(egpg.MOTOR_RIGHT)[SPEED] == 0):
            break

        # sleep till time to check again
        sleep(1.0/BUMPER_CHECK_RATE)



    if not emergency_stop:
        logging.info("*** normal stop() ***")



if __name__ == "__main__": main()

