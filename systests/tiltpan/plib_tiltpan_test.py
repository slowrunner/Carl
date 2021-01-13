#!/usr/bin/python
#
# my_tiltpan_test.py    test plib/tiltpan.py
#                       with plib/easygopigo3.py
#

#
from __future__ import print_function
from __future__ import division

# import the modules

import sys
# insert plib after current directory, before every place else
sys.path.insert(1,'/home/pi/Carl/plib')

from time import sleep
import easygopigo3  # uses plib/easygopigo3.py
import tiltpan


# ##### MAIN ######

def main():
        print("Test using plib versions of easygopigo3 and gopigo3")

        egpg = easygopigo3.EasyGoPiGo3(use_mutex=True,noinit=True)
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

