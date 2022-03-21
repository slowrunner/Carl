#!/usr/bin/env python3

import time
import logging
import wallfollowing

"""

    FILE:  safe_turn_test.py

    Test wallfollowing.safe_turn()

    safe_turn() ensures there is sufficient room from a wall in front of the bot
    to clear the rear of the bot when turning 180, and then performs the turn.

    The distance allows for a 2.5 cm baseboard not in the distance reading,

    Due to coasting to a stop, the bot will end up backing an extra 3 cm.

"""

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')


def main():

    wallfollowing.TALK = False

    egpg = wallfollowing.init_robot(ds_port="RPI_1", ps_port="SERVO1")

    msg="Set me facing close to a wall please"
    logging.info(msg)

    for msg in reversed(range(3)):
        logging.info(msg)
        time.sleep(1)



    msg="Executing safe 180 degree turn"
    logging.info(msg)

    wallfollowing.safe_turn(egpg,wallfollowing.CW_180)

    logging.info("==== THAT'S ALL FOR THIS TEST ====")

if __name__ == '__main__':
    main()

