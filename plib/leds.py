#!/usr/bin/python3

# File: leds.py
#
# Methods:
#    leds.all_on(egpg)   turn two red blinker leds on and two "eyes" on bright white
#    leds.all_off(egpg)  turn two red blinker leds off and two "eyes" off
#
# Usage:
#    import leds
#    egpg=easygopigo3.EasyGoPiGo3()
#    leds.all_on(egpg)
#    leds.all_off(egpg)
#
#    or from command line:
#    > ./leds.py          performs test on/off
#    > ./leds.py -s on    turns leds on
#    > ./leds.py -s off   turns leds off
#

import easygopigo3
import sys
sys.path.append("/home/pi/Carl/plib")
import myconfig
from time import sleep
import argparse

WHITE_BRIGHT = (255, 255, 255)

def all_on(egpg=None):
        egpg.blinker_on("left")
        egpg.blinker_on("right")
        egpg.led_on("left")
        egpg.led_on("right")
        egpg.set_eye_color(WHITE_BRIGHT)
        egpg.open_eyes()
        # can set wifi led to white, but it will reset to red shortly
        egpg.set_led(egpg.LED_WIFI,255,255,255)

def all_off(egpg=None):
        egpg.blinker_off("left")
        egpg.blinker_off("right")
        egpg.led_off("left")
        egpg.led_off("right")
        egpg.close_eyes()
        # can turn wifi led off but it will turn on shortly
        egpg.set_led(egpg.LED_WIFI,0,0,0)

def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--set", action="store", default=None, help="set all leds 'on' or 'off'")
    args = vars(ap.parse_args())
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    myconfig.setParameters(egpg)
    set = args["set"]

    if set==None:
        print("leds.py: Test all_on()")
        all_on(egpg)
        sleep(5)
        print("leds.py: Test all_off()")
        all_off(egpg)
    elif set=='on':
        all_on(egpg)
    else:
        all_off(egpg)

if (__name__ == '__main__'): main()
