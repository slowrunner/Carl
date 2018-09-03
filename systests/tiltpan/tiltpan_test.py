#!/usr/bin/python
#
# tiltpan_test.py    test plib/tiltpan.py
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
        print("tiltpan centered")
        tiltpan.tiltpan_center()
        sleep(5)
        print("pan(45)")
        tiltpan.pan(45)
        sleep(5)
        print("pan(135)")
        tiltpan.pan(135)
        sleep(5)
        print("pan(PAN_CENTER)")
        tiltpan.pan(tiltpan.PAN_CENTER)
        print("tilt(45)")
        tiltpan.tilt(45)
        sleep(5)
        print("tilt(-45)")
        tiltpan.tilt(-45)
        sleep(5)
        print("tilt(TILT_CENTER)")
        tiltpan.tilt(tiltpan.TILT_CENTER)

        tiltpan.tiltpan_center()
        print('UP too far')
        tiltpan.tilt(90)
        print("tilt_position:",tiltpan.tilt_position)
        sleep(5)
        print('DOWN too far')
        tiltpan.tilt(-90)
        print("tilt_position:",tiltpan.tilt_position)
        sleep(5)
        print("YES")
        tiltpan.nod_yes()
        sleep(2)
        print("NO")
        tiltpan.nod_no()
        sleep(2)
        print("IDK")
        tiltpan.nod_IDK()
        sleep(2)

if __name__ == "__main__":
    main()

