#!/usr/bin/env python3

"""
FILE: test_escape_behavior.py

PURPOSE: Test an subsumption architecture escape behavior

REFERENCES:
    "Mobile Robots: Inspiration To Implementation", Jones, Flynn, Seiger p318
"""
import subsumption

import time
import logging

subsumption.inhibit_scan = False
subsumption.inhibit_drive = False
subsumption.TALK = False

def stop():
            subsumption.mot_trans  = 0
            subsumption.mot_rot    = 0
            time.sleep(3)

def test_escape_behavior():

            logging.info("==== TEST ESCAPE BEHAVIOR ====")
            subsumption.say("Escape Behavior Test Will Begin In 5 seconds")
            time.sleep(5)

            try:
                while True:
                    time.sleep(1.0)
            except KeyboardInterrupt:

                logging.info("==== ESCAPE BEHAVIOR TEST COMPLETE ====")
                subsumption.say("Escape Behavior Test Complete")



# MAIN

def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

    logging.info("==== TEST SUBSUMPTION ====")
    subsumption.say("Test subsumption.")
    try:
        subsumption.setup()
        # while True:
        # do main things
        test_escape_behavior()

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

