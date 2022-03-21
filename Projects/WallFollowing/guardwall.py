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

FUDGE_FACTOR = 8.0 # cm

def main():
    wallfollowing.TALK = True

    logging.info("==== GUARD WALL ====")
    msg="Point me along a wall on my right side, about 15 cm away please"
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
    time.sleep(2)
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

    msg="OUTA MY WAY! I'm goin' to the other end of this wall"
    logging.info(msg)
    wallfollowing.say(msg)
    time.sleep(3)
    left_followed_distance_cm = wallfollowing.follow_wall(egpg,right0_left1=1)
    time.sleep(1)

    # bot started the return trip with rear approximately at end of wall
    # wheels are about 13 cm from bot rear
    # wheels traveled distance returned from follow_wall
    # distance sensor is 8.9cm in front of wheels
    # distance to end of wall is either following diag cos(45) or about 2cm if corner/obstacle
    if egpg.ds.read_mm()/10.0 < wallfollowing.FOLLOW_DIAGONAL:
        dist_from_end_of_wall = 2.0
    else:
        dist_from_end_of_wall = wallfollowing.FOLLOW_DIAGONAL * 0.707 - 2.0  # allow for stop distance after end of wall detected
    wall_length = wallfollowing.BOT_REAR_TO_WHEELS + left_followed_distance_cm + wallfollowing.DISTANCE_SENSOR_TO_WHEELS + dist_from_end_of_wall
    msg="wall length about {:0.1f} cm".format(wall_length)
    logging.info(msg)
    wallfollowing.say(msg)
    time.sleep(3)
    distance_to_center_of_wall_cm = wall_length/2.0

    if not wallfollowing.safe_to_turn(egpg):
        wallfollowing.backup_for_turning_room(egpg)
        time.sleep(1)

    msg="TURNING BACK AROUND"
    logging.info(msg)
    wallfollowing.say(msg)
    time.sleep(1)
    egpg.turn_degrees(wallfollowing.CW_180,blocking=True)
    time.sleep(1)

    msg="OUTA MY WAY! I'm goin' to center of wall"
    logging.info(msg)
    wallfollowing.say(msg)
    time.sleep(2)
    distance_to_travel = distance_to_center_of_wall_cm - (wallfollowing.TURNING_CIRCLE/2.0 + wallfollowing.BASE_BOARDS) - FUDGE_FACTOR
    right_followed_wall_mm = wallfollowing.follow_wall(egpg,right0_left1=0,travel_limit_cm=distance_to_travel)
    time.sleep(1)

    if not wallfollowing.safe_to_turn(egpg):
        wallfollowing.backup_for_turning_room(egpg)
        time.sleep(1)

    msg="TURNING TO GUARD WALL"
    logging.info(msg)
    wallfollowing.say(msg)
    egpg.turn_degrees(wallfollowing.CCW_90,blocking=False)
    time.sleep(1)



    logging.info("==== NOBODY BETTER MESS WITH ME NOW ====")
    wallfollowing.say("NOBODY BETTER MESS WITH ME NOW!")

if __name__ == '__main__':
    main()

