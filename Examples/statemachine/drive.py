#!/usr/bin/env python3

"""
REQUIRES:  python-statemachine
	   (pip3 install python-statemachine)


"""
from statemachine import StateMachine, State
import logging

angle_turned = 0

def turn_complete():
    global angle_turned, turn_angle

    turn_angle += 1
    return angle_turned >= turn_angle

def see_markter():
    return True

distance_reading = 100
APPROACH_DISTANCE = 50

def docking_distance():
    global distance_reading

    distance_reading -= 1
    return distance_reading <= APPROACH_DISTANCE

class DriveBehavior(StateMachine):
    "State Machine Test"
    # States
    startup    = State('Startup', initial = True)
    driving    = State('Driving')
    atApproach = State('AtApproach')
    turning180 = State('Turning180')
    ready      = State('Ready')


    # entering states

    def on_enter_driving(self):
        logging.info("on_enter_driving")

    def on_enter_atApproach(self):
        logging.info("on_enter_atApproach")

    def on_enter_turning180(self):
        logging.info("on_enter_turning180")

    def on_enter_ready(self):
        logging.info("on_enter_ready")

    cycle = startup.to(driving) | driving.to(atApproach) | atApproach.to(turning180) | turning180.to(ready) | ready.to(startup)


"""
    # Transitions
    marker = startup.to(driving)
    neardock = driving.to(atApproach)
    turning = atApproach.to(turning180)
    complete = turning180.to(ready)



    # actions

    def on_marker(self):
        logging.info("on_marker")

    def on_neardock(self):
        logging.info("on_neardock")

    def on_turning(self):
        logging.info("on_turning")

    def on_complete(self):
        logging.info("on_complete")

"""


"""
    def process(self):
        logging.info("executing process()")
        if self.is_startup:
            logging.info("process-startup")
        elif self.is_driving:
            logging.info("process-driving")
        elif self.is_atApproach:
            logging.info("process-atApproach")
        elif self.is_turning180:
            logging.info("process-turning180")
        elif self.is_ready:
            logging.info("process-ready")
"""


drive_behavior = DriveBehavior()

while True:
    drive_behavior.cycle()


