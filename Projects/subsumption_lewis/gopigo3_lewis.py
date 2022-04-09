#!/usr/bin/env python3

"""
FILE: gopigo3_lewis.py

PURPOSE: Implement MR:I2I "Lewis And Clark Program" p314
         to illustrate [Brooks 84/85/86] Subsumption Architecture For A Mobile Robot

REFERENCES:
    "Mobile Robots: Inspiration To Implementation", Jones, Flynn, Seiger
    https://en.wikipedia.org/wiki/Subsumption_architecture
    https://people.csail.mit.edu/brooks/papers/how-to-build.pdf

ADAPTATIONS:
    The RugWarrior Pro robot had sensors:

    - front located "45 degree cross eyed" IR obstacle detector
      left
      front (left and right)
      right

    - 360 degree bumper that detected contact from
      left
      front (left and right)
      right
      right rear (right and rear)
      rear
      left rear  (left and rear)

   On the GoPiGo3 a single pan servo mounted IR distance sensor
   continuously scans 5 directions:
   - Sets Obstacle Detected:
      left front  (135 degree pan and Distance < 20 cm)
      front       ( 90 degree pan and Distance < 14 cm)
      right front ( 45 degree pan and Distance < 20 cm)

   - Sets "Bumper/Contact" when:
      left        ( 180 degree pan and distance < 5 cm)
      left front  ( 135 degree pan and distance < 5 cm)
      front       (  90 degree pan and distance < 5 cm)
      right front (  45 degree pan and distance < 5 cm)
      right       (   0 degree pan and distance < 5 cm)
"""

import easygopigo3
import easysensors
import time
import sys
import logging
import subprocess


# Lewis and Clark
# Behavior Set: Move and don't get stuck


SAFE_TURNING_CIRCLE_RADIUS = 20    # cm - safe for GoPiGo3 to turn away if no object within this distance
MIN_TURNING_CIRCLE_RADIUS  =  5    # cm - safe for GoPiGo3 to turn toward objects farther than this distance

BUMP_DISTANCES =     { "front":  5, "right front":  7, "right":  5, "left front":   7, "left":   5 }
OBSTACLE_DISTANCES = { "front": 20, "right front": 28, "right": 20, "left front":  28, "left":  20 }
PAN_ANGLES =         { "front": 90, "right front": 45, "right":  0, "left front": 135, "left": 180 }

TALK = False

obstacles =         { "front": False, "right front": False, "right":  False, "left front": False, "left": False }
bumps     =         { "front": False, "right front": False, "right":  False, "left front": False, "left": False }

robot = None

# ==== UTILITY FUNCTIONS ====


def init_robot(ds_port="RPI_1",pan_port="SERVO1"):
    try:
        egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
        egpg.ds = egpg.init_distance_sensor(port=ds_port)
        egpg.pan = egpg.init_servo(port=pan_port)
        msg="Created EasyGoPiGo3 with Distance Sensor on Pan Servo"
        logging.info(msg)
        msg="Created Easy Go Pi Go 3 with Distance Sensor on Pan Servo"
        say(msg)
        return egpg
    except:
        logging.info("Initialization Failure - Cannot Proceed")
        sys.exit(1)

def ps_off(egpg):          # turn pan servo off
    # set PWM freq to 0 to stop holding position
    egpg.pan.disable_servo()
    logging.info("Pan Servo Off")

def ps_center(egpg):
    egpg.pan.rotate_servo(PAN_ANGLES["front"])
    logging.info("Pan Servo Centered")
    time.sleep(1)

def stop(egpg):
    egpg.stop()
    msg="Emergency Stop Requested"
    logging.info(msg)
    say(msg)

def say(phrase,blocking=True):
    if TALK:
        volume="-a{}".format(str(125))  # result "-a125"
        phrase = str(phrase)
        phrase = phrase.replace(' mm', ' millimeters ')
        phrase = phrase.replace(' cm', ' centimeters ')
        # logging.info("Starting say")
        # subprocess.Popen(["/usr/bin/espeak-ng", phrase])
        if blocking:
            subprocess.run(["/usr/bin/espeak-ng","-s150","-ven+f5",volume, phrase])
        else:
            subprocess.Popen(["/usr/bin/espeak-ng","-s150","-ven+f5",volume, phrase])
        # logging.info("Completed say")


# ===== BEHAVIORS =======


# PAN BEHAVIOR

# pan servo object is assumed to be at egpg.pan

def pan_behavior(egpg):
    try:
        try:
            msg="Starting pan behavior"
            logging.info(msg)
            say(msg)

            egpg.pan.rotate_servo(PAN_ANGLES["front"])
        except Exception as e:
            msg="Could not center pan servo"
            logging.info(msg)
            say(msg)

            logging.info("Exception {}".format(str(e)))
        pan_behavior_active = True
        while pan_behavior_active:
            for direction in PAN_ANGLES:
                angle = PAN_ANGLES[direction]
                try:
                    egpg.pan.rotate_servo(angle)
                except Exception as e:
                    msg="Cound not pan to {} degrees".format(angle)
                    logging.info(msg)
                    logging.info("Exception {}".format(str(e)))
                    pan_behavior_active = False
                try:
                    dist_reading_cm = egpg.ds.read_mm()/10.0  # read() returns whole centimeters so use read_mm()/10.0
                    msg="distance {:.0f} cm looking {} at {} degrees".format(dist_reading_cm,direction,angle)
                    logging.info(msg)

                except Exception as e:
                    msg="Exception reading distance sensor"
                    logging.info(msg)
                    logging.info("Exception {}".format(str(e)))
                    pan_behavior_active = False
                time.sleep(1.0)
    except KeyboardInterrupt:
        raise KeyboardInterrupt

# SETUP AND TEAR DOWN BEHAVIOR

def setup():
    global robot

    try:
        robot = init_robot(ds_port="RPI_1", pan_port="SERVO1")

        pan_behavior(robot)
    except KeyboardInterrupt:
        raise KeyboardInterrupt


def teardown():
    msg="Tear Down Process Initiated"
    logging.info(msg)
    say(msg)

    ps_center(robot)
    ps_off(robot)

# MAIN

def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

    logging.info("==== LEWIS AND CLARK - SUBSUMPTION ARCHITECTURE EXAMPLE ====")
    say("Lewis and Clark. Subsumption Architecture Example.")
    try:
        setup()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n")
        msg="Ctrl-C Detected"
        logging.info(msg)
        say(msg)

        teardown()

if __name__ == "__main__":
    main()

