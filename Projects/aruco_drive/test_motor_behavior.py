#!/usr/bin/env python3

"""
FILE: test_subsumption_w_aruco.py

PURPOSE: Test the addition of turn_degrees and drive_cm to subsumption architecture

"""
import subsumption_w_aruco as subsumption

import time
import logging

subsumption.inhibit_scan = True
subsumption.inhibit_drive = True
subsumption.TALK = False

def stop():
            subsumption.mot_trans  = 0
            subsumption.mot_rot    = 0
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(3)

def test_motors_behavior():
    try:
            logging.info("==== TEST MOTORS BEHAVIOR ====")
            subsumption.say("Motor Behavior Test Will Begin In 5 seconds")
            time.sleep(5)

            logging.info("==== test turn 90 degrees ====")
            subsumption.say("test turn 90 degrees will begin in 5 seconds")
            time.sleep(5) 

            subsumption.mot_trans  = 0
            subsumption.mot_rot    = 0
            subsumption.mot_deg    = 90
            subsumption.mot_cm     = 0
            logging.info("==== waiting 5 seconds for turn 90 degrees to complete ====")
            subsumption.say("waiting 5 seconds for turn 90 degrees to complete")
            time.sleep(5)

            stop()


            logging.info("==== test drive 10 cm ====")
            subsumption.say("test drive 10 cm will begin in 5 seconds")
            time.sleep(5)

            subsumption.mot_trans  = 0
            subsumption.mot_rot    = 0
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 100
            logging.info("==== waiting 5 seconds for drive 10 cm to complete ====")
            subsumption.say("waiting 5 seconds for drive 10 cm to complete")
            time.sleep(5)

            stop()

            return



            logging.info("==== Continuing prior motor behavior tests ====")
            subsumption.say("Prior tests will continue in 5 seconds")
            time.sleep(5)

            subsumption.mot_trans  = 100
            subsumption.mot_rot    = 0
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans  = -100
            subsumption.mot_rot    = 0
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans = 0
            subsumption.mot_rot  = 100
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)


            stop()

            subsumption.mot_trans = 0
            subsumption.mot_rot  = -100
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans  = 100
            subsumption.mot_rot  = 25
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans  = 100
            subsumption.mot_rot  = 50
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans  = 100
            subsumption.mot_rot  = 75
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans  = 100
            subsumption.mot_rot  = 100
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans = 100
            subsumption.mot_rot  = -25
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans = 100
            subsumption.mot_rot  = -50
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans = 100
            subsumption.mot_rot  = -75
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans = 100
            subsumption.mot_rot  = -100
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans  = -100
            subsumption.mot_rot  = 25
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans  = -100
            subsumption.mot_rot  = 50
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans  = -100
            subsumption.mot_rot  = 75
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans  = -100
            subsumption.mot_rot  = 100
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans = - 100
            subsumption.mot_rot  = -25
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans = - 100
            subsumption.mot_rot  = -50
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans = - 100
            subsumption.mot_rot  = -75
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans = - 100
            subsumption.mot_rot  = -100
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            logging.info("NOW TEST WITH TRANSLATE = 50")

            subsumption.mot_trans  = 50
            subsumption.mot_rot    = 0
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans  = -50
            subsumption.mot_rot    = 0
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans = 0
            subsumption.mot_rot  = 50
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)


            stop()

            subsumption.mot_trans = 0
            subsumption.mot_rot  = -50
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans  = 50
            subsumption.mot_rot  = 25
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans  = 50
            subsumption.mot_rot  = 50
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans  = 50
            subsumption.mot_rot  = 75
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans  = 50
            subsumption.mot_rot  = 100
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans = 50
            subsumption.mot_rot  = -25
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans = 50
            subsumption.mot_rot  = -50
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans = 50
            subsumption.mot_rot  = -75
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans = 50
            subsumption.mot_rot  = -100
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans  = -50
            subsumption.mot_rot  = 25
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans  = -50
            subsumption.mot_rot  = 50
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans  = -50
            subsumption.mot_rot  = 75
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans  = -50
            subsumption.mot_rot  = 100
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans = - 50
            subsumption.mot_rot  = -25
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans = - 50
            subsumption.mot_rot  = -50
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans = - 50
            subsumption.mot_rot  = -75
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            subsumption.mot_trans = - 50
            subsumption.mot_rot  = -100
            subsumption.mot_deg    = 0
            subsumption.mot_cm     = 0
            time.sleep(1)

            stop()

            logging.info("==== MOTOR BEHAVIOR TEST COMPLETE ====")
            subsumption.say("Motor Behavior Test Complete")

    except KeyboardInterrupt:
        logging.info("\nCtrl-C Detected. Exiting Test")
        subsumption.say("Control C detected.  Exiting Test")









# MAIN

def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

    logging.info("==== TEST SUBSUMPTION with ArUco MOTOR BEHAVIOR====")
    subsumption.say("Test subsumption with R. U co. motor behavior.")
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
        logging.info("==== Subsumption with ArUco Motor Behavior Test Done ====")
        subsumption.say("Subsumption with R. U co. Motor Behavior test done.")


if __name__ == "__main__":
    main()

