#!/usr/bin/env python3

"""
FILE: gopigo3_lewis.py

PURPOSE: Implement MR:I2I "Lewis And Clark Program" p314
         to illustrate [Brooks 84/85/86] Subsumption Architecture For A Mobile Robot

REFERENCES:
    "Mobile Robots: Inspiration To Implementation", Jones, Flynn, Seiger
    https://en.wikipedia.org/wiki/Subsumption_architecture
    https://people.csail.mit.edu/brooks/papers/how-to-build.pdf

ADAPTATIONS:
    The RugWarrior Pro robot had sensors:

    - front located "45 degree cross eyed" IR obstacle detector
      left
      front (left and right)
      right

    - 360 degree bumper that detected contact from
      left
      front (left and right)
      right
      right rear (right and rear)
      rear
      left rear  (left and rear)

   On the GoPiGo3 a single pan servo mounted IR distance sensor
   continuously scans 5 directions:
   - Sets Obstacle Detected:
      left front  (135 degree pan and Distance < 20 cm)
      front       ( 90 degree pan and Distance < 14 cm)
      right front ( 45 degree pan and Distance < 20 cm)

   - Sets "Bumper/Contact" when:
      left        ( 180 degree pan and distance < 5 cm)
      left front  ( 135 degree pan and distance < 5 cm)
      front       (  90 degree pan and distance < 5 cm)
      right front (  45 degree pan and distance < 5 cm)
      right       (   0 degree pan and distance < 5 cm)
"""

import time
import logging
import subsumption

# Lewis and Clark
# Behavior Set: Move and don't get stuck


# MAIN

def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

    logging.info("==== LEWIS AND CLARK - SUBSUMPTION ARCHITECTURE EXAMPLE ====")
    subsumption.say("Lewis and Clark. Subsumption Architecture Example.")

    subsumption.TALK = True
    subsumption.inhibit_drive = False

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
        logging.info("==== Lewis and Clark Done ====")
        subsumption.say("Lewis and Clark done")


if __name__ == "__main__":
    main()

