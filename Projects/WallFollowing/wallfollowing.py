#!/usr/bin/env python3

import easygopigo3
import easysensors
import time
import sys
import logging
from math import pi
import subprocess
import numpy

"""

    FILE:  wallfollowing.py
    REF: https://www.youtube.com/watch?v=UhquY0m7qic

    This program demonstrates a form of wall following consisting of three zones:
    Zones:  1) Too Close to Wall (45 degree side sensor readings smaller than desired)
            2) Farther From Wall than desired but within limit
            3) Very Far From Wall (45 degree side sensor reading larger than limit)

    Starting Conditions:
            1) Roughly aligned to wall (+/- 30 deg)
            2) Roughly spaced from wall by turning_circle distance (16.5 cm)

    Target wall following path is 19 cm from wall
    to allow clearance behind the robot to turn away from wall 90 or 180 degrees


    Turning circle is roughly 16.5 cm. Allowing an extra 2.5 cm for baseboards.

    Wall      |
              | <------- sensor
              |
    Baseboard |\
              | |  <--- robot's rear chassis
    Floor     |_|______________________________


    Stopping Conditions (Diagonal Wall Following Distance = 27 cm):
    - No Wall: Distance reading > 1.5 x Diagonal Distance (approx 40 cm)
    - No Wall: Distance reading jumps up by 20% of Diagonal Distance (approx 5 cm)
    - Obstacle or Corner: Distance Reading is less than half Diagonal Distance

    Control Algorithm:
    - Set inside wheel proportional to error (1-percent_error/2)
    - Set outside wheel proportional to error (1+percent_error/2)
    - Too Close: error will be negative  (inside wheel speeds up, outside slows)
    - Too Far:   error will be positive  (inside wheel slows down, outside speeds up)
    - percent error allowed to vary in range from -50% to +50% of Diagonal Distance

    Note: Only stock GoPiGo3 APIs, no plib code used
"""

TURNING_CIRCLE = 16.5  # cm - "safe" distance from center of wheel-base to back corner of bot
BASE_BOARDS = 2.5     # cm - Bot turning circle ->|BaseBoards|<-Wall
FOLLOW_DIAGONAL = 1.414 * (TURNING_CIRCLE + BASE_BOARDS) # sqrt(2) times distance_to_wall (10.6 inches)
SAFE_FOLLOW_DISTANCE = 0.5 * FOLLOW_DIAGONAL # When to declare path blocked
LOST_WALL_DISTANCE = 1.5 * FOLLOW_DIAGONAL  # When to declare wall end
LOST_WALL_DIFFERENCE = FOLLOW_DIAGONAL / 5.0  # If distance jumps 20% declare lost wall
FOLLOWING_SPEED = 300  # Works in range 100-300
SERVO_FOR_WALL_ON_RIGHT = 45.0
SERVO_FOR_WALL_ON_LEFT  = 135.0
SERVO_CENTER = 90.0
DISTANCE_SENSOR_TO_WHEELS = 8.9 # cm from wheels to distance sensor
CW_180 = 180.0
CCW_180 = -180.0
CW_90  = 90.0
CCW_90 = -90.0

STEERING_MULTIPLIER = 0.5 / FOLLOW_DIAGONAL  # For distance {0..2xFollowDist} to {-0.5 .. +0.5} (-50%..+50%) 
LOOP_TIME = 0.05  # 20 times per second

TALK = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

def say(phrase):
    if TALK:
        vol=125  # whisper = 50, shout = 250, normal = 125
        phrase = phrase.replace(' mm', ' millimeters ')
        phrase = phrase.replace(' cm', ' centimeters ')
        # subprocess.check_output(['espeak-ng -s150 -ven-us+f5 -a'+str(vol)+' "%s"' % phrase], stdout=None, stderr=None, shell=True)
        subprocess.call(['espeak-ng -s150 -ven-us+f5 -a'+str(vol)+' "%s"' % phrase], stdout=None, stderr=None, shell=True)

def enc_to_dist_cm(egpg,enc_l,enc_r):
    enc_ave = (enc_l + enc_r) / 2.0

    # Wheel dia. is in mm so divide by 10 for cm
    return ( (egpg.WHEEL_DIAMETER * pi * enc_ave / 360.0 ) / 10)


def ave_dist_cm(egpg):
    dist_readings = 0
    for i in range(1,5):
        dist_readings += (egpg.ds.read_mm() / 10.0)
        dist_average = dist_readings / i
        time.sleep(0.1)
    return dist_average

def follow_wall(egpg,right0_left1=0,travel_limit_cm=0):
    #
    UNKNOWN = 0
    TOO_CLOSE = 1
    TOO_FAR = 2
    DISCONTINUITY = 3
    TRAVEL_LIMITED = 4

    egpg.set_speed(egpg.NO_LIMIT_SPEED)  # Set maximum wheel speed limit
    bias = 0
    start_l_enc, start_r_enc = egpg.read_encoders()
    status = UNKNOWN
    loopcnt = 0  # don't talk too often

    if right0_left1 == 0:
        egpg.pan.rotate_servo(SERVO_FOR_WALL_ON_RIGHT)
    else:
        egpg.pan.rotate_servo(SERVO_FOR_WALL_ON_LEFT)
    time.sleep(1)

    distance_reading = ave_dist_cm(egpg)
    last_distance_reading = distance_reading
    logging.info("distance reading: {:.1f} cm".format(distance_reading))


    # loop as long as can see the wall and no obstacle or corner present
    while (LOST_WALL_DISTANCE > distance_reading > SAFE_FOLLOW_DISTANCE):
        if travel_limit_cm > 0:
            curr_l_enc, curr_r_enc = egpg.read_encoders()
            dist_traveled_cm  = enc_to_dist_cm(egpg, (curr_l_enc - start_l_enc), (curr_r_enc - start_r_enc))
            if dist_traveled_cm > travel_limit_cm:
                egpg.stop()
                status = TRAVEL_LIMITED
                break

        if (distance_reading - last_distance_reading) > LOST_WALL_DIFFERENCE:
            status = DISCONTINUITY
            break

        last_distance_reading = distance_reading

        if (distance_reading > FOLLOW_DIAGONAL):
            # too far from wall
            if status != TOO_FAR:
                status == TOO_FAR
            # slow inside wheel proportional to error
            steering = (distance_reading-FOLLOW_DIAGONAL) * STEERING_MULTIPLIER  # slow inside wheel percent of outside wheel speed
            msg="too far"
            logging.info(msg)
            if ((loopcnt % 10) == 0):
                say(msg)
            loopcnt += 1
        else:
            # pointing toward the wall or too close
            if status != TOO_CLOSE:
                status == TOO_CLOSE
            # increase inside wheel percent of outside wheel speed
            steering = (distance_reading-FOLLOW_DIAGONAL) * STEERING_MULTIPLIER  # speed-up inside wheel percent of outside wheel speed
            msg="too close"
            logging.info(msg)
            if ((loopcnt % 10) == 0):
                say(msg)
            loopcnt += 1

        numpy.clip(steering, -0.5, 0.5)          # constrain steering to +/- 50 percent of speed

        if (right0_left1 == 0):    # right wall following
           inside_wheel = egpg.MOTOR_RIGHT
           outside_wheel = egpg.MOTOR_LEFT
        else:
           inside_wheel = egpg.MOTOR_LEFT
           outside_wheel = egpg.MOTOR_RIGHT
        egpg.set_motor_dps(inside_wheel, (FOLLOWING_SPEED * (1.0 - steering) ) )
        egpg.set_motor_dps(outside_wheel, (FOLLOWING_SPEED * (1.0 + steering) ) )
        distance_reading = egpg.ds.read_mm() / 10.0
        logging.info("distance reading: {:.1f} cm,  steering value: {:.2f}".format(distance_reading,steering))
        time.sleep(LOOP_TIME)

    egpg.stop()
    curr_l_enc, curr_r_enc = egpg.read_encoders()
    dist_traveled_cm  = enc_to_dist_cm(egpg, (curr_l_enc - start_l_enc), (curr_r_enc - start_r_enc))
    msg="Traveled {:.1f} cm following wall".format(dist_traveled_cm)
    logging.info(msg)
    say(msg)

    msg="GOT A PROBLEM HERE"
    logging.info(msg)
    say(msg)

    if status == TRAVEL_LIMITED:
        msg="travel limit of {:.0f} cm reached".format(travel_limit_cm)
        logging.info(msg)
        say(msg)
    elif status == DISCONTINUITY:
        msg="distance reading jumped 20%"
        logging.info(msg)
        say(msg)
    elif wall_ended(egpg):
        msg="NO WALL"
        logging.info(msg)
        say(msg)
    else:
        msg="OBSTACLE OR CORNER"
        logging.info(msg)
        say(msg)
    time.sleep(1)
    return dist_traveled_cm

def wall_ended(egpg):
    return (ave_dist_cm(egpg) > LOST_WALL_DISTANCE)


def safe_to_turn(egpg):
    egpg.pan.rotate_servo(SERVO_CENTER)
    time.sleep(1)
    distance_reading = ave_dist_cm(egpg)
    safe_in_front = (distance_reading > (TURNING_CIRCLE - DISTANCE_SENSOR_TO_WHEELS))
    return safe_in_front

def backup_for_turning_room(egpg):
    distance_reading = ave_dist_cm(egpg)
    backup_distance = TURNING_CIRCLE - (distance_reading + DISTANCE_SENSOR_TO_WHEELS)
    msg="BACKING UP {:.1f} INCHES FOR TURNING CLEARANCE".format(backup_distance)
    logging.info(msg)
    say(msg)
    egpg.drive_cm( (-1.0*backup_distance), blocking=True)


def main():

    logging.info("==== WALL FOLLOWING ====")
    msg="Point me along a wall on my right side please"
    logging.info(msg)
    say(msg)
    try:
        egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
        egpg.ds = egpg.init_distance_sensor('RPI_1')
        egpg.pan = egpg.init_servo()
    except:
        logging.info("Initialization Failure - Cannot Proceed")
        sys.exit(1)
    time.sleep(10)



    msg="OUTA MY WAY! I'm goin' till I can't"
    logging.info(msg)
    say(msg)
    follow_wall(egpg,right0_left1=0)
    time.sleep(1)

    if not safe_to_turn(egpg):
        backup_for_turning_room(egpg)
        time.sleep(1)

    msg="TURNING AROUND"
    logging.info(msg)
    say(msg)
    egpg.turn_degrees(CCW_180,blocking=True)
    time.sleep(1)

    msg="OUTA MY WAY! I'm goin' till I can't"
    logging.info(msg)
    say(msg)
    follow_wall(egpg,right0_left1=1)
    time.sleep(1)

    if not safe_to_turn(egpg):
        backup_for_turning_room(egpg)
        time.sleep(1)


    msg="TURNING BACK AROUND"
    logging.info(msg)
    say(msg)
    egpg.turn_degrees(CW_180,blocking=True)
    time.sleep(1)



    logging.info("==== GUESS THAT'S ALL SHE WROTE ====")
    say("GUESS THAT'S ALL SHE WROTE")

if __name__ == '__main__':
    main()

