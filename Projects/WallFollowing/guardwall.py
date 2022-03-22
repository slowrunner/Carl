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
    msg="Point me along a wall on my right side, about 20 cm away please"
    logging.info(msg)
    wallfollowing.say(msg)
    egpg = wallfollowing.init_robot()

    msg="OUTA MY WAY! I'm goin' till I can't"
    logging.info(msg)
    wallfollowing.say(msg)
    right_followed_wall_cm = wallfollowing.follow_wall(egpg,right0_left1=0)
    time.sleep(1)

    # safe_turn() will log and announce turn
    wallfollowing.safe_turn(egpg,wallfollowing.CCW_180)


    msg="OUTA MY WAY! I'm goin' to the other end of this wall"
    logging.info(msg)
    wallfollowing.say(msg)
    left_followed_distance_cm = wallfollowing.follow_wall(egpg,right0_left1=1)
    time.sleep(1)

    # Compute wall length knowing started at detected start of wall and traveled to end of wall
    wall_length = wallfollowing.wall_length_from_dist_traveled(egpg,left_followed_distance_cm)
    msg="wall length about {:0.1f} cm".format(wall_length)
    logging.info(msg)
    wallfollowing.say(msg)
    distance_to_center_of_wall_cm = wall_length/2.0

    # safe_turn() will log and announce turn
    wallfollowing.safe_turn(egpg,wallfollowing.CW_180)

    msg="OUTA MY WAY! I'm goin' to center of wall"
    logging.info(msg)
    wallfollowing.say(msg)
    distance_to_travel = distance_to_center_of_wall_cm - (wallfollowing.TURNING_CIRCLE/2.0 + wallfollowing.BASE_BOARDS) - FUDGE_FACTOR
    right_followed_wall_mm = wallfollowing.follow_wall(egpg,right0_left1=0,travel_limit_cm=distance_to_travel)

    msg="TURNING TO GUARD WALL"
    logging.info(msg)
    wallfollowing.say(msg)
    egpg.set_speed(150)
    wallfollowing.safe_turn(egpg,wallfollowing.CCW_90)


    logging.info("==== NOBODY BETTER MESS WITH ME NOW ====")
    wallfollowing.say("NOBODY BETTER MESS WITH ME NOW!")

if __name__ == '__main__':
    main()

