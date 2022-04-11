#!/usr/bin/env python3

"""
FILE: test_subsumption.py

PURPOSE: Test an implementation of[Brooks 84/85/86] Subsumption Architecture For A Mobile Robot

REFERENCES:
    "Mobile Robots: Inspiration To Implementation", Jones, Flynn, Seiger
    https://en.wikipedia.org/wiki/Subsumption_architecture
    https://people.csail.mit.edu/brooks/papers/how-to-build.pdf
"""
import subsumption

import time
import logging

subsumption.inhibit_drive = True
subsumption.TALK = False

def test_motors_behavior():

            logging.info("==== TEST MOTORS BEHAVIOR ====")
            subsumption.say("Motor Behavior Test Will Begin In 5 seconds")
            time.sleep(5)

            subsumption.mot_trans  = 100
            subsumption.mot_rot    = 0
            time.sleep(1)

            subsumption.mot_trans  = 0
            subsumption.mot_rot    = 0
            time.sleep(1)

            subsumption.mot_trans  = -100
            subsumption.mot_rot    = 0
            time.sleep(1)


            subsumption.mot_trans = 0
            subsumption.mot_rot  = 100
            time.sleep(1)


            subsumption.mot_trans  = 0
            subsumption.mot_rot    = 0
            time.sleep(1)

            subsumption.mot_trans = 0
            subsumption.mot_rot  = -100
            time.sleep(1)

            subsumption.mot_trans  = 0
            subsumption.mot_rot    = 0
            time.sleep(1)


            subsumption.mot_trans  = 100
            subsumption.mot_rot  = 25
            time.sleep(1)
            subsumption.mot_rot  = 50
            time.sleep(1)
            subsumption.mot_rot  = 75
            time.sleep(1)
            subsumption.mot_rot  = 100
            time.sleep(1)

            subsumption.mot_rot  = 0
            subsumption.mot_trans = 0
            time.sleep(1)

            subsumption.mot_trans = 100
            time.sleep(1)
            subsumption.mot_rot  = -25
            time.sleep(1)
            subsumption.mot_rot  = -50
            time.sleep(1)
            subsumption.mot_rot  = -75
            time.sleep(1)
            subsumption.mot_rot  = -100
            time.sleep(1)

            subsumption.mot_trans = 0
            subsumption.mot_rot  = 0
            time.sleep(1)

            subsumption.mot_trans  = -100
            subsumption.mot_rot  = 25
            time.sleep(1)
            subsumption.mot_rot  = 50
            time.sleep(1)
            subsumption.mot_rot  = 75
            time.sleep(1)
            subsumption.mot_rot  = 100
            time.sleep(1)

            subsumption.mot_rot  = 0
            subsumption.mot_trans = 0
            time.sleep(1)

            subsumption.mot_trans = - 100
            time.sleep(1)
            subsumption.mot_rot  = -25
            time.sleep(1)
            subsumption.mot_rot  = -50
            time.sleep(1)
            subsumption.mot_rot  = -75
            time.sleep(1)
            subsumption.mot_rot  = -100
            time.sleep(1)

            subsumption.mot_trans = 0
            subsumption.mot_rot  = 0
            time.sleep(1)

            logging.info("==== MOTOR BEHAVIOR TEST COMPLETE ====")
            subsumption.say("Motor Behavior Test Complete")



# MAIN

def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

    logging.info("==== TEST SUBSUMPTION ====")
    subsumption.say("Test subsumption.")
    try:
        subsumption.setup()
        # while True:
        # do main things
        test_motors_behavior()

    except KeyboardInterrupt:
        print("")
        msg="Ctrl-C Detected in Main"
        logging.info(msg)
        subsumption.say(msg)

    except Exception as e:
        logging.info("Handling main exception: %s",e)

    finally:
        subsumption.teardown()
        logging.info("==== Subsumption Test Done ====")
        subsumption.say("Subsumption test done")


if __name__ == "__main__":
    main()

