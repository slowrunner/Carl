#!/usr/bin/env python3
#
# stop.py

"""
Documentation:  STOP motors

"""

# from __future__ import print_function # use python 3 syntax but make it compatible with python 2
# from __future__ import division       #                           ''

import sys
try:
    sys.path.append('/home/pi/Carl/plib')
    import speak
    import myconfig
    Carl = True
except:
    Carl = False
import easygopigo3 # import the EasyGoPiGo3 class
from time import sleep


# MAIN

def main():
    try:
        egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    except:
        strToLog = "Could not instantiate an EasyGoPiGo3"
        print(strToLog)
        exit(1)
    if Carl:
        myconfig.setParameters(egpg)

    try:
        # Do Something Once
        egpg.stop()
        print("Stopped Motors")
        sleep(1)

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)


if (__name__ == '__main__'):  main()
