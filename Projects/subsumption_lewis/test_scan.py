#!/usr/bin/env python3

"""
FILE: test_scan.py

PURPOSE: Test an subsumption scanning behavior

REFERENCES:
    "Mobile Robots: Inspiration To Implementation", Jones, Flynn, Seiger
"""
import subsumption

import time
import logging

subsumption.inhibit_scan = False
subsumption.inhibit_drive = True
subsumption.TALK = False

def stop():
            subsumption.mot_trans  = 0
            subsumption.mot_rot    = 0
            time.sleep(3)

def test_scan_behavior():

            logging.info("==== TEST SCAN BEHAVIOR ====")

            while True:
               time.sleep(1)

            logging.info("==== SCAN TEST COMPLETE ====")
            subsumption.say("Scan Behavior Test Complete")



# MAIN

def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

    logging.info("==== TEST SUBSUMPTION ====")
    subsumption.say("Test subsumption.")
    try:
        subsumption.setup()
        # while True:
        # do main things
        test_scan_behavior()

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

