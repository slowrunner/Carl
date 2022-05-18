#!/usr/bin/env python3

"""
FILE: test_aruco_sensor.py

PURPOSE: Test ArUco marker sensor behavior

REFERENCES:
"""
import subsumption_w_aruco as subsumption

import time
import logging

subsumption.inhibit_scan = True
subsumption.inhibit_drive = True
subsumption.TALK = False
subsumption.inhibit_aruco_drive = True
subsumption.inhibit_aruco_find = True
subsumption.inhibit_aruco_sensor = True

def stop():
            subsumption.mot_trans  = 0
            subsumption.mot_rot    = 0
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(3)

def test_aruco_sensor_behavior():

            logging.info("==== TEST ArUco Sensor BEHAVIOR ====")
            subsumption.inhibit_aruco_sensor = False

            while True:
               time.sleep(1)

            logging.info("==== ArUco TEST COMPLETE ====")
            subsumption.say("R. U co. Sensor Behavior Test Complete")



# MAIN

def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

    logging.info("==== test_aruco_sensor.py ====")
    subsumption.say("Test main.")
    try:
        subsumption.setup()
        # while True:
        # do main things
        test_aruco_sensor_behavior()

    except KeyboardInterrupt:
        print("")
        msg="Ctrl-C Detected in Main"
        logging.info(msg)
        subsumption.say(msg)

    except Exception as e:
        logging.info("Handling main exception: %s",e)

    finally:
        subsumption.teardown()
        logging.info("==== Test Done ====")
        subsumption.say("Test done")


if __name__ == "__main__":
    main()

