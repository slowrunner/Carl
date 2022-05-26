#!/usr/bin/env python3

"""
FILE: test_aruco_drive.py

PURPOSE: Test ArUco drive behavior
         aruco_drive_behavior:
         - while aruco_marker in sight and  
                 distance > dock_ready_distance:  
           - drive to put marker at straight_forward_pixel
"""
import subsumption_w_aruco as subsumption

import time
import logging
import sys
sys.path.append('/home/pi/Carl/plib')
import status

subsumption.pan_angles = { "front": 90 }
subsumption.inhibit_scan = True
subsumption.inhibit_drive = False
subsumption.inhibit_escape = True
subsumption.inhibit_avoid = True
subsumption.TALK = False
subsumption.inhibit_aruco_drive = True
subsumption.inhibit_aruco_find = True
subsumption.inhibit_aruco_sensor = True
subsumption.DISPLAY_MARKERS = False        # Set True if running in windowed environment (VNC or ssh -X)
subsumption.inhibit_motors = False

def stop():
            subsumption.mot_trans  = 0
            subsumption.mot_rot    = 0
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0

def test_aruco_drive_behavior():

            logging.info("==== TEST ArUco Drive BEHAVIOR ====")
            subsumption.inhibit_aruco_drive = False

            count = 60
            while count > 0:
               status.printStatus(subsumption.egpg, ds=None)
               logging.info("")
               if len(subsumption.aruco_markers) > 0:
                   markerID = subsumption.aruco_markers[0][0]
                   cX = subsumption.aruco_markers[0][1]
                   cY = subsumption.aruco_markers[0][2]
                   distance_to_marker = subsumption.dist_reading_cm
                   logging.info("Marker: {} at [{}, {}] {:.1f} cm away".format(markerID, cX, cY, distance_to_marker))
               else:
                   logging.info("Test Aruco Drive: No Marker in view")

               time.sleep(1)
               count -= 1


            logging.info("==== ArUco Drive TEST COMPLETE ====")
            subsumption.say("R. U co. Drive Behavior Test Complete")



# MAIN

def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

    logging.info("==== test_aruco_drive.py ====")
    subsumption.say("Test aruco drive main.")
    try:
        subsumption.setup()
        # while True:
        # do main things
        test_aruco_drive_behavior()

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

