#!/usr/bin/env python3

"""
FILE: find_aruco_drive.py

PURPOSE: Find an ArUco marker and drive to be 90cm (~36") away from marker
         uses a form of [Brooks 84/85/86] Subsumption Architecture For A Mobile Robot

REFERENCES:
    "Mobile Robots: Inspiration To Implementation", Jones, Flynn, Seiger
    https://en.wikipedia.org/wiki/Subsumption_architecture
    https://people.csail.mit.edu/brooks/papers/how-to-build.pdf

BEHAVIOR SET ACTIVE:
 - aruco_drive
 - aruco_find
 - aruco_sensor
 - arbitrate
 - motors
"""

import time
import logging
import subsumption_w_aruco as subsumption


# MAIN

subsumption.TALK = False

def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

    logging.info("==== ArUco Find And Drive ====")
    subsumption.say("R. U co. Find and Drive")

    subsumption.inhibit_drive = True

    try:
        subsumption.setup()
        while True:
            # do main things
            time.sleep(1)
    except KeyboardInterrupt:
        print("")
        msg="Ctrl-C Detected in Main"
        logging.info(msg)
        subsumption.say(msg)

    except Exception as e:
        logging.info("Handling main exception: %s",e)

    finally:
        subsumption.teardown()
        logging.info("==== ArUco Find And Drive Done ====")
        subsumption.say("R. U co. Find and Drive Done.")


if __name__ == "__main__":
    main()

