#!/usr/bin/env python3

"""
FILE: test_escape_behavior.py

PURPOSE: Test an subsumption architecture escape behavior

REFERENCES:
    "Mobile Robots: Inspiration To Implementation", Jones, Flynn, Seiger p318
"""
import subsumption_w_aruco as subsumption

import time
import logging

subsumption.inhibit_scan = True
subsumption.inhibit_drive = False
subsumption.TALK = False

def stop():
            subsumption.mot_trans  = 0
            subsumption.mot_rot    = 0
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0


def test_aruco_find_behavior():

            logging.info("==== TEST ARUCO FIND BEHAVIOR ====")
            subsumption.say("R. U co. Find test Will Begin In 5 seconds")
            time.sleep(5)
            subsumption.inhibit_aruco_find = False
            subsumption.aruco_find_behavior_active = True
            try:
                while subsumption.aruco_find_behavior_active:
                    time.sleep(1.0)
            except KeyboardInterrupt:
                pass
            subsumption.inhibit_aruco_find = True
            stop()
            if len(subsumption.aruco_markers) > 0:
                   markerID = subsumption.aruco_markers[0][0]
                   cX = subsumption.aruco_markers[0][1]
                   cY = subsumption.aruco_markers[0][2]
                   logging.info("ArUco Find Test: Marker: {} at [{}, {}]".format(markerID, cX, cY))
            else:
                logging.info("ArUco Find Test:  aruco_find_behavior did not find marker")

            logging.info("==== ARUCO FIND BEHAVIOR TEST COMPLETE ====")
            subsumption.say("R. U co. Find Behavior Test Complete")



# MAIN

def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

    logging.info("==== TEST SUBSUMPTION ====")
    subsumption.say("Test subsumption.")
    try:
        subsumption.setup()
        # while True:
        # do main things
        test_aruco_find_behavior()

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

