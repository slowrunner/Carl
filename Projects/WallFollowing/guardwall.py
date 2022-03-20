#!/usr/bin/env python3

import easygopigo3
import time
import logging
import subprocess
import wallfollowing
"""

    FILE:  guardwall.py

    This program demonstrates using wallfollowing
    with end of wall and corner detection.

    The bot will right-wall follow to end of wall,
    turn 180
    left-wall follow to end of wall,
    turn 180
    right wall follow to center of wall
    turn 90
    Exit

    Start program with wall on right side of robot
    about 15 cm from the wall.

    Note: Only stock GoPiGo3 APIs, no plib code used
"""


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

def main():
    wallfollowing.TALK = True

    logging.info("==== GUARD WALL ====")
    msg="Point me along a wall on my right side, about 15 cm away, please"
    logging.info(msg)
    wallfollowing.say(msg)
    try:   # Wall Following expects an EasyGoPiGo3 object with a pan servo mounted ToF distance sensor
        egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
        egpg.ds = egpg.init_distance_sensor('RPI_1')
        egpg.pan = egpg.init_servo()
    except:
        logging.info("Initialization Failure - Cannot Proceed")
        sys.exit(1)
    time.sleep(10)


    msg="OUTA MY WAY! I'm goin' till I can't"
    logging.info(msg)
    wallfollowing.say(msg)
    right_followed_wall_cm = wallfollowing.follow_wall(egpg,right0_left1=0)
    time.sleep(1)

    if not wallfollowing.safe_to_turn(egpg):
        wallfollowing.backup_for_turning_room(egpg)
        time.sleep(1)

    msg="TURNING AROUND"
    logging.info(msg)
    wallfollowing.say(msg)
    egpg.turn_degrees(wallfollowing.CCW_180,blocking=True)
    time.sleep(1)

    msg="OUTA MY WAY! I'm goin' till I can't"
    logging.info(msg)
    wallfollowing.say(msg)
    left_followed_wall_cm = wallfollowing.follow_wall(egpg,right0_left1=1)
    time.sleep(1)

    if not wallfollowing.safe_to_turn(egpg):
        wallfollowing.backup_for_turning_room(egpg)
        time.sleep(1)

    msg="TURNING BACK AROUND"
    logging.info(msg)
    wallfollowing.say(msg)
    egpg.turn_degrees(wallfollowing.CW_180,blocking=True)
    time.sleep(1)

    msg="OUTA MY WAY! I'm goin' to center of wall"
    logging.info(msg)
    wallfollowing.say(msg)
    center_of_wall = left_followed_wall_cm / 2.0
    right_followed_wall_mm = wallfollowing.follow_wall(egpg,right0_left1=0,travel_limit_cm=center_of_wall)
    time.sleep(1)

    if not wallfollowing.safe_to_turn(egpg):
        wallfollowing.backup_for_turning_room(egpg)
        time.sleep(1)

    msg="TURNING TO GUARD WALL"
    logging.info(msg)
    wallfollowing.say(msg)
    egpg.turn_degrees(wallfollowing.CCW_90,blocking=True)
    time.sleep(1)



    logging.info("==== NOBODY BETTER MESS WITH ME NOW ====")
    wallfollowing.say("NOBODY BETTER MESS WITH ME NOW!")

if __name__ == '__main__':
    main()

