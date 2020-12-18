#!/usr/bin/env python3

# FILE: test_noinit_easygopigo3.py

# PURPOSE:  Test the noinit=True option of the noinit_easygopigo3.EasyGoPiGo3() class
#           by instantiating an EasyGoPiGo3(noinit=True) ojbect to access battery voltage
#           without calling set_speed(DEFAULT_SPEED) and without initializing pigpio pins

import noinit_easygopigo3
import time
from statistics import mean

def main():
    print("Initializing an EasyGoPiGo3(noinit=True) object")
    noinit_egpg = noinit_easygopigo3.EasyGoPiGo3(use_mutex=True, noinit=True)

    print("Accessing the board using the noinit object")
    vBatt_l = []
    for i in range(3):
        time.sleep(0.1)
        vBatt_l += [noinit_egpg.volt()]
    vBatt = mean(vBatt_l)
    print("Battery: {:.1f} volts".format(vBatt))


if __name__ == '__main__': main()
