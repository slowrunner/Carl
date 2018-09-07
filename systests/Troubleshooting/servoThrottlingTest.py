#!/usr/bin/python
#
# servoThrottlingTest.py    Center Tilt and Pan Servos from max rotation 
#                           to test for 5v Throttling event
#

#
from __future__ import print_function
from __future__ import division

# import the modules

import sys
sys.path
sys.path.append('/home/pi/Carl/plib')
import tiltpan
from time import sleep

# ##### MAIN ######

def main():
  while True:
    try:
      print("tiltpan centered")
      tiltpan.tiltpan_center()
      sleep(2.0)
      print("max deflection")
      tiltpan.tilt(90)
      sleep(0.2)
      tiltpan.pan(0)
      sleep(2)
    except KeyboardInterrupt:
      print("Cntrl-C detected.  Exiting..")
      break
  tiltpan.tiltpan_center()
  tiltpan.off()

if __name__ == "__main__":
    main()

