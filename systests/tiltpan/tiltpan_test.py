#!/usr/bin/python
#
# tiltpan_test.py    test plib/tiltpan.py
#

#
from __future__ import print_function
from __future__ import division

# import the modules

import sys
sys.path.append('/home/pi/Carl/plib')  # use DI easygopigo3

import tiltpan
from time import sleep
import easygopigo3


# ##### MAIN ######

def main():
        print("Test using DI easygopigo3")
        egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
	egpg.tp = tiltpan.TiltPan(egpg)

        print("tiltpan centered")
        egpg.tp.tiltpan_center()
        sleep(1)
        print("pan(45)")
        egpg.tp.pan(45)
        sleep(1)
        print("pan(135)")
        egpg.tp.pan(135)
        sleep(1)
        print("pan(PAN_CENTER)")
        egpg.tp.pan(tiltpan.PAN_CENTER)
        print("tilt(45)")
        egpg.tp.tilt(45)
        sleep(1)
        print("tilt(-45)")
        egpg.tp.tilt(-45)
        sleep(1)
        print("tilt(TILT_CENTER)")
        egpg.tp.tilt(tiltpan.TILT_CENTER)

        egpg.tp.tiltpan_center()
        print('UP too far')
        egpg.tp.tilt(90)
        print("tilt_position:",egpg.tp.tilt_position)
        sleep(1)
        print('DOWN too far')
        egpg.tp.tilt(-90)
        print("tilt_position:",egpg.tp.tilt_position)
        sleep(1)
        print("YES")
        egpg.tp.nod_yes()
        sleep(2)
        print("NO")
        egpg.tp.nod_no()
        sleep(2)
        print("IDK")
        egpg.tp.nod_IDK()
        sleep(2)

if __name__ == "__main__":
    main()

