#!/usr/bin/env python3

"""
# FILE:  forward_test.py

# PURPOSE:  Test VirtualBumper for GoPiGo3 forward()

"""

from easygopigo3 import EasyGoPiGo3
from virtualbumper import VirtualBumper
from time import sleep
import logging
import atexit
import subprocess

TALK = True

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

def say(phrase,blocking=True):
    if TALK:
        volume="-a{}".format(str(125))  # result "-a125"
        phrase = str(phrase)
        phrase = phrase.replace(' mm', ' millimeters ')
        phrase = phrase.replace(' cm', ' centimeters ')
        if blocking:
            subprocess.run(["/usr/bin/espeak-ng","-s150","-ven+f5",volume, phrase])
        else:
            subprocess.Popen(["/usr/bin/espeak-ng","-s150","-ven+f5",volume, phrase])


def main():

    logging.info("=== VIRTUAL BUMPERS FORWARD TEST ===")

    egpg = EasyGoPiGo3(use_mutex=True)
    atexit.register(egpg.stop)
    egpg.bumper = VirtualBumper(egpg)

    egpg.set_speed(300)

    emergency_stop = False

    BUMPER_CHECK_RATE = 15  # times per second
    drive_time = 2  # seconds

    say("Forward {} second test checking bumper {} times per second".format(drive_time, BUMPER_CHECK_RATE))
    egpg.forward()
    logging.info("*** forward({}) test checking bumper {} times per second ***".format(drive_time, BUMPER_CHECK_RATE))
    for i in range(int(drive_time * BUMPER_CHECK_RATE)):
        if egpg.bumper.bumped() == True:
            egpg.stop()
            logging.info("*** EMERGENCY STOP ***")
            say("Emergency Stop")
            emergency_stop = True
            break
        sleep(1.0/BUMPER_CHECK_RATE)

    if not emergency_stop:
        egpg.stop()
        logging.info("*** normal stop() ***")
        say("Normal Stop")

if __name__ == "__main__": main()

