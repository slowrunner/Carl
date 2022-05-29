#!/usr/bin/env python3

# FILE: stoplight.py

# Flash red five times, then loop: [ 5xGreen, 1 yellow, 1 red ] 
from statemachine import StateMachine, State
import time
import logging


class TrafficLightMachine(StateMachine):
    "A traffic light machine"

    # some class vars
    counter = 0
    flash = False

    # STATES
    green = State('Green')
    yellow = State('Yellow')
    red = State('Red', initial=True)

    # LEGAL TRANSITIONS
    grn2yel = green.to(yellow)
    yel2red = yellow.to(red)
    red2grn = red.to(green)
    red2red = red.to.itself()
    grn2grn = green.to.itself()
    toitself = red.to.itself() | green.to.itself() | yellow.to.itself()   # self.toitself() useful 
    flshred = red.from_(green,yellow,red)  # self.flshred() is legal from any state e.g. emergency red

    # ON TRANSITIONS
    def on_flshred(self):
        logging.info('flashing red')
        self.flash = True

    # ON ENTERING STATE
    def on_enter_green(self):
            logging.info('GO GO')
            time.sleep(1)
            self.counter += 1
            if self.counter == 5:
                self.counter = 0
                self.grn2yel()
            else:
                self.grn2grn()

    def on_enter_yellow(self):
        logging.info('Slow Down')
        time.sleep(1)
        self.run('yel2red')   # same as self.yel2red()

    def on_enter_red(self):
        logging.info('STOP.')
        time.sleep(1)
        if self.flash:
            self.counter += 1
            if self.counter == 5:
                self.counter = 0
                self.flash = False
                self.red2grn()
            else:
                self.flshred()
        else:
            self.run('red2grn')


# === TEST IT ===

# instantiate in initial state
stm = TrafficLightMachine()  

try:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')
    logging.info("Starting State: {}".format(stm.current_state))

    # execute flash red transition which sets machine "running"
    stm.flshred()

except KeyboardInterrupt:
    logging.info("ctrl-c: Exiting")


