#!/usr/bin/python3

# File: leds.py
#
# Methods:
#    leds.all_on(egpg)   turn two red blinker leds on and two "eyes" on bright white
#    leds.all_off(egpg)  turn two red blinker leds off and two "eyes" off


import easygopigo3
import sys
sys.path.append("/home/pi/Carl/plib")
import myconfig
from time import sleep

WHITE_BRIGHT = (255, 255, 255)

def all_on(egpg=None):
        egpg.blinker_on("left")
        egpg.blinker_on("right")
        egpg.led_on("left")
        egpg.led_on("right")
        egpg.set_eye_color(WHITE_BRIGHT)
        egpg.open_eyes()

def all_off(egpg=None):
        egpg.blinker_off("left")
        egpg.blinker_off("right")
        egpg.led_off("left")
        egpg.led_off("right")
        egpg.close_eyes()


def main():
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    myconfig.setParameters(egpg)

    print("leds.py: Test all_on()")
    all_on(egpg)
    sleep(5)
    print("leds.py: Test all_off()")
    all_off(egpg)

if (__name__ == '__main__'): main()
