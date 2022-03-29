#!/usr/bin/env python3

from easygopigo3 import EasyGoPiGo3
from time import sleep
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')


class  VIRTUALBUMPER(object):
    last_left_motor_status = [0,0,0,0]
    last_right_motor_status = [0,0,0,0]
    max_left_diff = 0
    max_right_diff = 0
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

            left_diff = left_motor_status[3] - self.last_left_motor_status[3]
            right_diff = right_motor_status[3] - self.last_left_motor_status[3]

            if left_diff < self.max_left_diff:
                self.max_left_diff = left_diff
            if right_diff < self.max_right_diff:
                self.max_right_diff = right_diff

            logging.info("left motor status:  {} diff {:>5d}   max: {:>5d}".format(left_motor_status,left_diff,self.max_left_diff))
            logging.info("right motor status: {} diff {:>5d}   max: {:>5d}".format(right_motor_status,right_diff,self.max_right_diff))


            self.last_left_motor_status = left_motor_status
            self.last_right_motor_status = right_motor_status

            if (left_motor_status[3] == 0) and (right_motor_status[3] == 0):
                self.max_left_diff = 0
                self.max_right_diff = 0
                self.virtual_bumper_state = False
                logging.info("reset virtual bumper max left and right diff to 0")

            if (left_motor_status[0] and 0x2) or (right_motor_status[0] and 0x2):
                if (self.max_left_diff < -30) or (self.max_right_diff < -30):
                    logging.info("**** VIRTUAL BUMPER TRUE ****")
                    self.virtual_bumper_state = True

            return self.virtual_bumper_state

def main():

    logging.info("=== VIRTUAL BUMPERS TEST ===")

    egpg = EasyGoPiGo3(use_mutex=True)
    egpg.bumper = VIRTUALBUMPER(egpg)

    egpg.forward()
    logging.info("*** forward() ***")
    for i in range(100):
        if egpg.bumper.bumped() == True:
            break
        sleep(0.01)

    logging.info("max left diff: {}".format(egpg.bumper.max_left_diff))
    logging.info("max right diff: {}".format(egpg.bumper.max_right_diff))


    egpg.stop()
    logging.info("*** stop() ***")
    for i in range(100):
        egpg.bumper.bumped()
        sleep(0.01)

    logging.info("max left diff: {}".format(egpg.bumper.max_left_diff))
    logging.info("max right diff: {}".format(egpg.bumper.max_right_diff))

if __name__ == "__main__": main()

