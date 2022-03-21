#!/usr/bin/env python3

import time
import logging
import wallfollowing

"""

    FILE:  measurewall.py

    This program uses wallfollowing to measure the length of a wall

    Process:
    - Start with robot roughly parallel to a wall on right 15-20 cm away
    - Bot will travel to end of wall (corner or wall opening) and then turn 180
    - Bot will wall follow to other end of wall (corner or wall opening)
    - Bot will announce wall length estimate and turn 180 to face original direction

"""

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')


def main():

    wallfollowing.TALK = True

    logging.info("==== MEASURE WALL USING WALL FOLLOWING ====")
    wallfollowing.say("Measure wall using wall follwoing")
    time.sleep(4)

    egpg = wallfollowing.init_robot(ds_port="RPI_1", ps_port="SERVO1")

    msg="Point me along a wall on my right side, about 15 cm away please"
    logging.info(msg)
    wallfollowing.say(msg)
    time.sleep(5)

    for msg in reversed(range(10)):
        logging.info(msg)
        wallfollowing.say(msg)
        time.sleep(1)



    msg="OUTA MY WAY! I'm goin' till I can't"
    logging.info(msg)
    wallfollowing.say(msg)
    time.sleep(2)

    wallfollowing.follow_wall(egpg,right0_left1=0)

    time.sleep(1)

    wallfollowing.safe_turn(egpg,wallfollowing.CCW_180)


    msg="OUTA MY WAY! I'm goin' to the other end of this wall"
    logging.info(msg)
    wallfollowing.say(msg)
    time.sleep(3)

    distance_traveled_cm = wallfollowing.follow_wall(egpg,right0_left1=1)

    wall_length = wallfollowing.wall_length_from_dist_traveled(egpg,distance_traveled_cm)
    msg="wall length about {:.0f} cm".format(wall_length)
    logging.info(msg)
    wallfollowing.say(msg)

    wallfollowing.safe_turn(egpg,wallfollowing.CW_180)

    time.sleep(2)



    logging.info("==== THAT'S ALL FOR THIS TEST OF WALL FOLLOWING ====")
    wallfollowing.say("THAT'S ALL FOR THIS TEST OF WALL FOLLOWING")

if __name__ == '__main__':
    main()

