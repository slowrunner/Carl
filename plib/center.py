#!/usr/bin/python
#
# center.py    Center Tilt and Pan Servos
#

#
from __future__ import print_function
from __future__ import division

# import the modules

import sys
sys.path
sys.path.append('/home/pi/Carl/plib')

import tiltpan

# ##### MAIN ######

def main():
  print("tiltpan centered")
  tiltpan.tiltpan_center()

if __name__ == "__main__":
    main()

