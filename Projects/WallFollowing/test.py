#!/usr/bin/env python3

import easygopigo3
import easysensors
import time
import sys
import logging
from math import pi
import subprocess

"""
    This program demonstrates a form of wall following consisting of three zones:
    Zones:  1) Too Close to Wall (45 degree side sensor readings gets smaller than threshold)
            2) Roughly Aligned With Wall At Chosen Distance
            3) Too Far From Wall (45 degree side sensor readings gets larger than threshold)
    Starting Conditions:  
            1) Roughly aligned to wall (+/- 30 deg)
            2) Roughly spaced from wall by turning_circle distance (6.5 in)


    Note: Only stock GoPiGo3 APIs, no plib code used
"""

TURNING_CIRCLE = 6.5  # inches - "safe" distance from center of wheel-base to back corner of bot
BASE_BOARDS = 1.0     # inches - Bot turning circle ->|BaseBoards|<-Wall
FOLLOW_DIAGONAL = 1.414 * (TURNING_CIRCLE + BASE_BOARDS) # sqrt(2) times distance_to_wall
SAFE_FOLLOW_DISTANCE = 0.5 * FOLLOW_DIAGONAL # When to declare path blocked
LOST_WALL_DISTANCE = 2.0 * FOLLOW_DIAGONAL  # When to declare wall end
FOLLOWING_SPEED = 150
CM_PER_INCH = 2.54
SERVO_FOR_WALL_ON_RIGHT = 45.0
SERVO_FOR_WALL_ON_LEFT  = 135.0
SERVO_CENTER = 90.0
DISTANCE_SENSOR_TO_WHEELS = 3.5 # inches from wheels to distance sensor
CW_180 = 180.0
CCW_180 = -180.0
ALIGNED_ZONE_DISTANCE = 1.0  # amount the diagonal measurement can vary before adjusting heading
BIAS_INCREMENT = 0.005 * FOLLOWING_SPEED

TALK = True

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

def say(phrase):
    if TALK:
        vol=125  # whisper = 50, shout = 250, normal = 125
        subprocess.check_output(['espeak-ng -s150 -ven-us+f5 -a'+str(vol)+' "%s"' % phrase], stderr=subprocess.STDOUT, shell=True)

def enc_to_dist_mm(egpg,enc_l,enc_r):
    enc_ave = (enc_l + enc_r) / 2.0
    return egpg.WHEEL_DIAMETER * pi * enc_ave / 360.0


def ave_dist_inches(egpg):
    dist_readings = 0
    for i in range(1,10):
        dist_readings += egpg.ds.read_inches()
        dist_average = dist_readings / i 
        time.sleep(0.1)
    return dist_average

def follow_wall(egpg,right0_left1=0):
    #
    distance_reading = egpg.ds.read_inches()
    logging.info("distance reading: {}".format(distance_reading))
    egpg.set_speed(egpg.DEFAULT_SPEED)  # Set maximum wheel speed limit to 300DPS
    bias = 0
    start_l_enc, start_r_enc = egpg.read_encoders()

    loopcnt = 0  # don't talk too often

    # loop as long as can see the wall and no obstacle or corner present
    while (LOST_WALL_DISTANCE > distance_reading > SAFE_FOLLOW_DISTANCE):
        if (distance_reading > (FOLLOW_DIAGONAL+ALIGNED_ZONE_DISTANCE)):
            # pointing away from wall or too far from wall

            msg="too far"
            logging.info(msg)
            if ((loopcnt % 10) == 0):
                say(msg)
            loopcnt += 1
            bias -= BIAS_INCREMENT  # slow inside wheel
        elif (distance_reading < FOLLOW_DIAGONAL):
            # pointing toward the wall or too close
            msg="too close"
            logging.info(msg)
            if ((loopcnt % 10) == 0):
                say(msg)
            loopcnt += 1

            bias += BIAS_INCREMENT  # speed up inside wheel
        else:  # Must be roughly aligned with wall
            msg="in zone"
            logging.info(msg)
            if ((loopcnt % 10) == 0):
                say(msg)
            loopcnt += 1

            bias = 0
        if (right0_left1 == 0):    # right wall following
           inside_wheel = egpg.MOTOR_RIGHT
           outside_wheel = egpg.MOTOR_LEFT
        else:
           inside_wheel = egpg.MOTOR_LEFT
           outside_wheel = egpg.MOTOR_RIGHT
        egpg.set_motor_dps(inside_wheel, (FOLLOWING_SPEED  + bias))
        egpg.set_motor_dps(outside_wheel, FOLLOWING_SPEED)
        distance_reading = egpg.ds.read_inches()
        logging.info("distance reading: {} inside wheel bias: {}".format(distance_reading,bias))
        time.sleep(0.1)
    egpg.stop()
    curr_l_enc, curr_r_enc = egpg.read_encoders()
    dist_traveled = enc_to_dist_mm(egpg, (curr_l_enc - start_l_enc), (curr_r_enc - start_r_enc))
    msg="Traveled {:.0f} mm following wall".format(dist_traveled)
    logging.info(msg)
    say(msg)

    msg="GOT A PROBLEM HERE"
    logging.info(msg)
    say(msg)

    if wall_ended(egpg):
        msg="NO WALL"
        logging.info(msg)
        say(msg)
    else:
        msg="AT OBSTACLE OR CORNER"
        logging.info(msg)
        say(msg)
    time.sleep(1)

def wall_ended(egpg):
    return (ave_dist_inches(egpg) > LOST_WALL_DISTANCE)


def safe_to_turn(egpg):
    egpg.pan.rotate_servo(SERVO_CENTER)
    time.sleep(1)
    distance_reading = ave_dist_inches(egpg)
    safe_in_front = (distance_reading > (TURNING_CIRCLE - DISTANCE_SENSOR_TO_WHEELS))
    return safe_in_front

def backup_for_turning_room(egpg):
    distance_reading = ave_dist_inches(egpg)
    backup_distance = TURNING_CIRCLE - (distance_reading + DISTANCE_SENSOR_TO_WHEELS)
    msg="BACKING UP {:.1f} INCHES FOR TURNING CLEARANCE".format(backup_distance)
    logging.info(msg)
    say(msg)
    egpg.drive_cm( (-1.0*backup_distance*CM_PER_INCH), blocking=True)


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


    egpg.pan.rotate_servo(SERVO_FOR_WALL_ON_RIGHT)
    time.sleep(1)

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

    egpg.pan.rotate_servo(SERVO_FOR_WALL_ON_LEFT)
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

