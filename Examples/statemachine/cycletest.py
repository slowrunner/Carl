#!/usr/bin/env python3

"""
FILE:  drive.py
PURPOSE:  Demonstrate handling events and limiting cycle rate

REQUIRES:  python-statemachine
	   (pip3 install python-statemachine)

IMPLEMENTS:
 - waiting state: accepts a drive_request if no obstacle seen
 - driving state: stops driving if obstacle seen
 - all states: if exit_flag is set transition to exit state
 - main: simulates drive_request every 5 cycles
 - main: simulates obstacle every 10 cycles
 - main: simulates exit_flag after 60 cycles
 - main: exits after 65 cycles

"""
from statemachine import StateMachine, State
import logging
from time import sleep


NOTHING = 3000
distance_reading = NOTHING
OBSTACLE = 50
states_per_second = 1
exit_flag = False
drive_request = 0
motor_speed = 0

class DriveBehavior(StateMachine):
    "State Machine Example"

    # States
    startup    = State('Startup', initial = True)
    waiting    = State('Waiting')
    driving    = State('Driving')
    obstacle   = State('Obstacle')
    exit       = State('Exit')


    # Transitions
    s2w      = startup.to(waiting)
    w2d      = waiting.to(driving)
    w2o      = waiting.to(obstacle)
    d2o      = driving.to(obstacle)
    o2w      = obstacle.to(waiting)
    quit     = startup.to(exit) | waiting.to(exit) | driving.to(exit) | obstacle.to(exit)

    cycle = startup.to.itself() | waiting.to.itself() | driving.to.itself() | obstacle.to.itself() | exit.to.itself()

    # on_transitions
    def on_s2w(self):
        logging.info("transition")

    def on_w2o(self):
        logging.info("transition")

    def on_w2d(self):
        logging.info("transition accepted drive_request: {}".format(drive_request))
        motor_speed = drive_request

    def on_d2o(self):
        logging.info("transition stopping")
        motor_speed = 0

    def on_o2w(self):
        logging.info("transition")

    def on_cycle(self):
        logging.info("null transition")


    # entering states  (event detectors)

    def on_enter_startup(self):
        logging.info("checking events - ef:{} dist:{} req:{}".format(exit_flag, distance_reading, drive_request))
        if exit_flag:
            self.quit()
        else:
            self.s2w()  # auto transition

    def on_enter_waiting(self):
        logging.info("checking events - ef:{} dist:{} req:{}".format(exit_flag, distance_reading, drive_request))
        if exit_flag:
            self.quit()
        elif distance_reading <= OBSTACLE:    # should not drive?
            self.w2o()
        elif drive_request > 0:    # drive wanted?
            self.w2d()

    def on_enter_driving(self):
        logging.info("checking events - ef:{} dist:{} req:{}".format(exit_flag, distance_reading, drive_request))
        if exit_flag:
            self.quit()
        elif distance_reading <= OBSTACLE:
            self.d2o()

    def on_enter_obstacle(self):
        logging.info("checking events - ef:{} dist:{} req:{}".format(exit_flag, distance_reading, drive_request))
        if exit_flag:
            self.quit()
        elif distance_reading > OBSTACLE:
            self.o2w()  # go back to waiting

    def on_enter_exit(self):
        logging.info("wrapping up - ef:{} dist:{} req:{}".format(exit_flag, distance_reading, drive_request))








def main():
    global drive_request, distance_reading, exit_flag

    try:
	    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')
	    drive_behavior = DriveBehavior()

	    state_count = 0

	    while True:
	        logging.info("cycle: {}".format(state_count))
	        drive_behavior.cycle()
	        state_count += 1
	        sleep(1/states_per_second)
	        if  (state_count % 5) == 0:
	            drive_request = 10
	        else:
	            drive_request = 0

	        if (state_count % 10) == 0:
	            distance_reading = OBSTACLE
	        else:
	            distance_reading = NOTHING

	        if state_count == 60:
	            exit_flag = True

	        if state_count == 65:
	            exit()
    except KeyboardInterrupt:
        print("")
        logging.info("Cntrl-C: Exiting")

if __name__ == "__main__":
   main()
