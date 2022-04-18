#!/usr/bin/env python3

"""
# FILE:  virtualBumper.py

# PURPOSE:  Provide a software "bumper" for GoPiGo3

# USAGE:

    egpg = EasyGoPiGo3(use_mutex=True)
    egpg.bumper = VIRTUALBUMPER(egpg)

    # Drive forward for 2 seconds unless bump into something
    # Check bumper 10 times/seceond
    egpg.forward()
    for i in range(20):
        if egpg.bumper.bumped() == True:
            egpg.stop()
            sleep(0.1)
            break
        sleep(0.1)


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

class  VIRTUALBUMPER(object):
    last_left_motor_status = [0,0,0,0]
    last_right_motor_status = [0,0,0,0]
    virtual_bumper_state = False
    start_time = None
    last_bump_time = None

    gpg = None

    def __init__(self, egpg):
        try:
            logging.info("left motor status:  {}".format(egpg.get_motor_status(egpg.MOTOR_LEFT)))
            logging.info("right motor status: {}".format(egpg.get_motor_status(egpg.MOTOR_RIGHT)))
            self.gpg = egpg
            self.virtual_bumper_state = False
            self.start_time = None
            logging.info("virtual bumper initialized")

        except Exception as e:
            logging.info("Could not init virtual bumper: {}".format(str(e)))

    def bumped(self):
            left_motor_status = self.gpg.get_motor_status(self.gpg.MOTOR_LEFT)
            right_motor_status = self.gpg.get_motor_status(self.gpg.MOTOR_RIGHT)

            # logging.info("left motor status:  {}".format(left_motor_status))
            # logging.info("right motor status: {}".format(right_motor_status))

            if ((abs(left_motor_status[SPEED]) > 0) or (abs(right_motor_status[SPEED]) > 0)):
                dt_now = dt.datetime.now()
                if self.start_time == None:
                    self.start_time = dt_now
                elif (dt_now - self.start_time).microseconds / 1000 > RAMP_UP_DELAY:   # Past startup overloads?
                    if last_bump_time:  # not first bump?
                        if dt_now - last_bump_time).milliseconds / 1000 < BUMP_DEBOUNCE:  # Has possible bump expired?
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


            elif self.start_time:     # Power under 50 and was tracking a drive
                self.virtual_bumper_state = False
                self.start_time = None
                self.last_bump_time = None
            return self.virtual_bumper_state

def main():

    logging.info("=== VIRTUAL BUMPERS TEST ===")

    egpg = EasyGoPiGo3(use_mutex=True)
    egpg.bumper = VIRTUALBUMPER(egpg)

    egpg.set_speed(300)

    emergency_stop = False

    BUMPER_CHECK_RATE = 100  # times per second

    egpg.forward()
    logging.info("*** forward() ***")
    for i in range(2 * BUMPER_CHECK_RATE):
        if egpg.bumper.bumped() == True:
            egpg.stop()
            logging.info("*** EMERGENCY STOP ***")
            sleep(1.0/BUMPER_CHECK_RATE)
            emergency_stop = True
            break
        sleep(0.01)


    if not emergency_stop:
        egpg.stop()
        logging.info("*** normal stop() ***")
        sleep(0.1)

    for i in range(1 * BUMPER_CHECK_RATE):
        egpg.bumper.bumped()
        sleep(1.0/BUMPER_CHECK_RATE)


if __name__ == "__main__": main()

