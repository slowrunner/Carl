#!/usr/bin/env python3

"""
# FILE:  virtualbumper.py

# PURPOSE:  Provide a software "bumper" for GoPiGo3

# USAGE:

    from virtualbumper import VirtualBumper

    egpg = EasyGoPiGo3(use_mutex=True)
    egpg.bumper = VirtualBumper(egpg)

    BUMPER_CHECK_RATE = 20 # times per second (between 20 and 100 is good)
    SPEED = 3  # get_motor_status[3] is current wheel speed

for forward() or backward():

    drive_time = 2  # seconds
    egpg.forward()

    # Drive for drive_time,  unless bump into something
    for i in range(int(drive_time * BUMPER_CHECK_RATE)):
        if egpg.bumper.bumped() == True:
            egpg.stop()
            sleep(0.1)
            break
        sleep(1.0/BUMPER_CHECK_RATE)


or for drive_cm():
    drive_dist_cm = 25
    egpg.drive_cm(drive_dist_cm, blocking=False)

    # while wheels are turning, check if bumped into something
    while True:
        if egpg.bumper.bumped() == True:
            egpg.stop()
            break
        # check if reached target distance (both wheels stop)
        if (egpg.get_motor_status(egpg.MOTOR_LEFT)[SPEED] == 0) and (egpg.get_motor_status(egpg.MOTOR_RIGHT)[SPEED] == 0):
            break

        # sleep till time to check again
        sleep(1.0/BUMPER_CHECK_RATE)

"""

from easygopigo3 import EasyGoPiGo3
from time import sleep
import logging
import datetime as dt

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

# get_motor_status(left/right_motor) returns [Overloaded, Power, Encoder, speed]
OVERLOADED = 0
POWER = 1
ENCODER = 2
SPEED = 3

RAMP_UP_DELAY = 500  # milliseconds before overloaded flag means bumped
BUMP_DEBOUNCE = 150  # must see two overloaded flags within 150ms to call it a real bump


class  VirtualBumper(object):
    last_left_motor_status = [0,0,0,0]
    last_right_motor_status = [0,0,0,0]
    virtual_bumper_state = False
    start_time = None
    last_bump_time = None

    gpg = None

    def __init__(self, egpg):
        try:
            # logging.info("left motor status:  {}".format(egpg.get_motor_status(egpg.MOTOR_LEFT)))
            # logging.info("right motor status: {}".format(egpg.get_motor_status(egpg.MOTOR_RIGHT)))
            self.gpg = egpg
            self.virtual_bumper_state = False
            self.start_time = None
            logging.info("Virtual Bumper Initialized")

        except Exception as e:
            logging.info("Could not init virtual bumper: {}".format(str(e)))

    def bumped(self):
            left_motor_status = self.gpg.get_motor_status(self.gpg.MOTOR_LEFT)
            right_motor_status = self.gpg.get_motor_status(self.gpg.MOTOR_RIGHT)

            # logging.info("left motor status:  {}".format(left_motor_status))
            # logging.info("right motor status: {}".format(right_motor_status))

            if ((abs(left_motor_status[SPEED]) > 0) or (abs(right_motor_status[SPEED]) > 0)):  # Drive starting or in progress
                dt_now = dt.datetime.now()
                if self.start_time == None:
                    self.start_time = dt_now
                elif (dt_now - self.start_time).microseconds / 1000 > RAMP_UP_DELAY:   # Past startup overloads?
                    if self.last_bump_time:  # not first bump?
                        if (dt_now - self.last_bump_time).microseconds / 1000 < BUMP_DEBOUNCE:  # Has possible bump expired?
                            if left_motor_status[OVERLOADED] == 2:
                                logging.info("LEFT BUMP  -  motor status:  {}".format(left_motor_status))
                                self.virtual_bumper_state = True
                            if right_motor_status[OVERLOADED] == 2:
                                logging.info("RIGHT BUMP -  motor status:  {}".format(right_motor_status))
                                self.virtual_bumper_state = True
                        else:    # too long since last overload
                            self.last_bump_time = None         # expire first bump, check for new first bump
                            if left_motor_status[OVERLOADED] == 2:
                                logging.info("Left possible bump  -  motor status:  {}".format(left_motor_status))
                                self.last_bump_time = dt_now
                            if right_motor_status[OVERLOADED] == 2:
                                logging.info("Right possible bump -  motor status:  {}".format(right_motor_status))
                                self.last_bump_time = dt_now

                    else:  # no first overload, so check for first bump indication
                            if left_motor_status[OVERLOADED] == 2:
                                logging.info("Left possible bump  -  motor status:  {}".format(left_motor_status))
                                self.last_bump_time = dt_now
                            if right_motor_status[OVERLOADED] == 2:
                                logging.info("Right possible bump -  motor status:  {}".format(right_motor_status))
                                self.last_bump_time = dt_now


            elif self.start_time:     # drive has ended
                self.virtual_bumper_state = False
                self.start_time = None
                self.last_bump_time = None
            else:                    # drive has not begun
                self.virtual_bumper_state = False
                self.last_bump_time = None
                sleep(0.05)

            return self.virtual_bumper_state


