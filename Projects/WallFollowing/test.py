#!/usr/bin/env python3

import easygopigo3
import easysensors
import time
import sys

"""
    This program demonstrates a form of wall following consisting of three zones:
    Zones:  1) Too Close To Wall or Driving toward Wall
            2) Roughly Aligned With Wall At Chosen Distance
            3) Too Far From Wall or Driving away from Wall

    Direction of t
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
ALIGNED_ZONE_DISTANCE = 0.5  # amount the diagonal measurement can vary before adjusting heading
BIAS_INCREMENT = 10

def follow_wall(egpg):
    #
    distance_reading = egpg.ds.read_inches()
    print("distance reading: {}".format(distance_reading))
    egpg.set_speed(FOLLOWING_SPEED)
    bias = 0

    # loop as long as can see the wall and no obstacle or corner present
    while (LOST_WALL_DISTANCE > distance_reading > SAFE_FOLLOW_DISTANCE):
        if (distance_reading > (FOLLOW_DIAGONAL+ALIGNED_ZONE_DISTANCE)):
            # pointing away from wall or too far from wall
            bias -= BIAS_INCREMENT  # slow right wheel
        elif (distance_reading < FOLLOW_DIAGONAL):
            # pointing toward the wall or too close
            bias += BIAS_INCREMENT  # speed up right wheel
        else:  # Must be roughly aligned with wall
            bias = 0
        egpg.set_motor_dps(egpg.MOTOR_LEFT, FOLLOWING_SPEED)
        egpg.set_motor_dps(egpg.MOTOR_RIGHT, FOLLOWING_SPEED + bias)
        distance_reading = egpg.ds.read_inches() 
        print("distance reading: {} right wheel bias: {}".format(distance_reading,bias))
        time.sleep(0.1)
    egpg.stop()
    print("GOT A PROBLEM HERE")
    if wall_ended(egpg):
        print("NO WALL")
    else:
        print("AT OBSTACLE OR CORNER")
    time.sleep(1)

def wall_ended(egpg):
    return (egpg.ds.read_inches() > LOST_WALL_DISTANCE)


def safe_to_turn(egpg):
    egpg.pan.rotate_servo(SERVO_CENTER)
    time.sleep(1)
    distance_reading = egpg.ds.read_inches()
    safe_in_front = (distance_reading > (TURNING_CIRCLE - DISTANCE_SENSOR_TO_WHEELS))
    return safe_in_front

def backup_for_turning_room(egpg):
    distance_reading = egpg.ds.read_inches()
    backup_distance = TURNING_CIRCLE - (distance_reading + DISTANCE_SENSOR_TO_WHEELS)
    print("BACKING UP {} INCHES FOR TURNING CLEARANCE".format(backup_distance))
    egpg.drive_cm( (-1.0*backup_distance*CM_PER_INCH), blocking=True)


def main():

    print("==== WALL FOLLOWING ====")
    print("\n Point me along a wall on my right side please")
    try:
        egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
        egpg.ds = egpg.init_distance_sensor('RPI_1')
        egpg.pan = egpg.init_servo()
    except:
        print("Initialization Failure - Cannot Proceed")
        sys.exit(1)
    time.sleep(10)

    # testing bias
    print("testing bias = 0")
    bias = 0
    egpg.set_motor_dps(egpg.MOTOR_LEFT, FOLLOWING_SPEED)
    egpg.set_motor_dps(egpg.MOTOR_RIGHT, FOLLOWING_SPEED + bias)

    print("testing bias = -20")
    bias = -20
    egpg.set_motor_dps(egpg.MOTOR_LEFT, FOLLOWING_SPEED)
    egpg.set_motor_dps(egpg.MOTOR_RIGHT, FOLLOWING_SPEED + bias)

    print("testing bias = +20")
    bias = 20
    egpg.set_motor_dps(egpg.MOTOR_LEFT, FOLLOWING_SPEED)
    egpg.set_motor_dps(egpg.MOTOR_RIGHT, FOLLOWING_SPEED + bias)
    egpg.stop()


    egpg.pan.rotate_servo(SERVO_FOR_WALL_ON_RIGHT)
    time.sleep(1)

    print("OUTA MY WAY! I'm goin' till I can't")
    follow_wall(egpg)
    time.sleep(5)

    if not safe_to_turn(egpg):
        backup_for_turning_room(egpg)
        time.sleep(5)

    print("TURNING AROUND")
    egpg.turn_degrees(CCW_180,blocking=True)
    time.sleep(5)

    egpg.pan.rotate_servo(SERVO_FOR_WALL_ON_LEFT)
    time.sleep(1)
    print("OUTA MY WAY! I'm goin' till I can't")
    follow_wall(egpg)
    time.sleep(5)

    if not safe_to_turn(egpg):
        backup_for_turning_room(egpg)
        time.sleep(5)


    print("TURNING BACK AROUND")
    egpg.turn_degrees(CW_180,blocking=True)
    time.sleep(5)



    print("==== GUESS THAT'S ALL SHE WROTE ====")


if __name__ == '__main__':
    main()

