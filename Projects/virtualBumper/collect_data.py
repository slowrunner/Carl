#!/usr/bin/env python3

from easygopigo3 import EasyGoPiGo3
from time import sleep
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')


class  VIRTUALBUMPER(object):
    last_left_motor_status = [0,0,0,0]
    last_right_motor_status = [0,0,0,0]
    virtual_bumper_state = False

    gpg = None

    def __init__(self, egpg):
        try:
            logging.info("left motor status:  {}".format(egpg.get_motor_status(egpg.MOTOR_LEFT)))
            logging.info("right motor status: {}".format(egpg.get_motor_status(egpg.MOTOR_RIGHT)))
            self.gpg = egpg
            self.virtual_bumper_state = False
            logging.info("virtual bumper initialized")

        except Exception as e:
            logging.info("Could not init virtual bumper: {}".format(str(e)))

    def bumped(self):
            left_motor_status = self.gpg.get_motor_status(self.gpg.MOTOR_LEFT)
            right_motor_status = self.gpg.get_motor_status(self.gpg.MOTOR_RIGHT)

            logging.info("left motor status:  {}".format(left_motor_status))
            logging.info("right motor status: {}".format(right_motor_status))


            self.last_left_motor_status = left_motor_status
            self.last_right_motor_status = right_motor_status

            return self.virtual_bumper_state

def main():

    logging.info("=== VIRTUAL BUMPERS DATA COLLECTION ===")

    egpg = EasyGoPiGo3(use_mutex=True)
    egpg.bumper = VIRTUALBUMPER(egpg)

    egpg.set_speed(300)


    logging.info("*** forward() ***")
    egpg.forward()
    for i in range(100):
        if egpg.bumper.bumped() == True:
            break
        sleep(0.01)


    egpg.stop()
    logging.info("*** stop() ***")
    for i in range(100):
        egpg.bumper.bumped()
        sleep(0.01)


if __name__ == "__main__": main()

