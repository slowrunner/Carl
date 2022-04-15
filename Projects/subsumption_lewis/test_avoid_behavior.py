#!/usr/bin/env python3

"""
FILE: test_avoid_behavior.py

PURPOSE: Test an subsumption architecture avoid behavior

REFERENCES:
    "Mobile Robots: Inspiration To Implementation", Jones, Flynn, Seiger p318
"""
import subsumption

import time
import logging

subsumption.inhibit_scan = True
subsumption.inhibit_drive = False
subsumption.inhibit_cruise = True
subsumption.TALK = False

def stop():
            subsumption.mot_trans  = 0
            subsumption.mot_rot    = 0
            time.sleep(3)

def test_avoid_behavior():

            logging.info("==== TEST Avoid BEHAVIOR starts in 5 seconds ====")
            subsumption.say("Avoid Behavior Test Will Begin In 5 seconds")
            time.sleep(5)

            try:
                logging.info("Force Cruise Behavior Output")
                subsumption.cruise_trans = 100
                subsumption.cruise_rot = 0
                subsumption.cruise_behavior_active=True
                time.sleep(2)

                logging.info("Force front left obstacle")
                subsumption.obstacles["front left"] = True
                time.sleep(2)
                logging.info("Reset front left obstacle")
                subsumption.obstacles["front left"] = False
                time.sleep(2)

                logging.info("Force front obstacle")
                subsumption.obstacles["front"] = True
                time.sleep(2)
                logging.info("Reset front obstacle")
                subsumption.obstacles["front"] = False
                time.sleep(2)

                logging.info("Force front right obstacle")
                subsumption.obstacles["front right"] = True
                time.sleep(2)
                logging.info("Reset front right obstacle")
                subsumption.obstacles["front right"] = False
                time.sleep(2)

                logging.info("Terminate Cruise Behavior Output")
                subsumption.cruise_behavior_active = False
                time.sleep(10)
            except KeyboardInterrupt:

                logging.info("==== AVOID BEHAVIOR TEST COMPLETE ====")
                subsumption.say("Avoid Behavior Test Complete")



# MAIN

def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

    logging.info("==== TEST SUBSUMPTION ====")
    subsumption.say("Test subsumption.")
    try:
        subsumption.setup()
        # while True:
        # do main things
        test_avoid_behavior()

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

