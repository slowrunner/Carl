#!/usr/bin/env python3

"""
FILE: test_aruco_sensor.py

PURPOSE: Test ArUco marker sensor behavior

REFERENCES:
"""
import subsumption_w_aruco as subsumption

import time
import logging
import sys
sys.path.append('/home/pi/Carl/plib')
import status

subsumption.inhibit_scan = True
subsumption.inhibit_drive = True
subsumption.TALK = False
subsumption.inhibit_aruco_drive = True
subsumption.inhibit_aruco_find = True
subsumption.inhibit_aruco_sensor = False

def stop():
            subsumption.mot_trans  = 0
            subsumption.mot_rot    = 0
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            # time.sleep(3)

def test_aruco_sensor_behavior():

            logging.info("==== TEST ArUco Sensor BEHAVIOR ====")
            subsumption.inhibit_aruco_sensor = False

            count = 60
            while count > 0:
               status.printStatus(subsumption.egpg, ds=None)
               if len(subsumption.aruco_markers) > 0:
                   markerID = subsumption.aruco_markers[0][0]
                   cX = subsumption.aruco_markers[0][1]
                   cY = subsumption.aruco_markers[0][2]
                   logging.info("Marker: {} at [{}, {}]".format(markerID, cX, cY))
               time.sleep(1)
               count -= 1

            logging.info("==== Inhibit ArUco Sensor True ====")
            subsumption.inhibit_aruco_sensor = True
            count = 60
            while count > 0:
               status.printStatus(subsumption.egpg, ds=None)
               if len(subsumption.aruco_markers) > 0:
                   markerID = subsumption.aruco_markers[0][0]
                   cX = subsumption.aruco_markers[0][1]
                   cY = subsumption.aruco_markers[0][2]
                   logging.info("Marker: {} at [{}, {}]".format(markerID, cX, cY))
               time.sleep(1)
               count -= 1

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

