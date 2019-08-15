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
#    > ./leds.py -c 5     turn all leds green

import easygopigo3
import sys
sys.path.append("/home/pi/Carl/plib")
import myconfig
from time import sleep
import argparse

WHITE_BRIGHT = (255, 255, 255) # color 0
RED = (255, 0, 0)            # color 1
ORANGE = (255, 125, 0)       # color 2
YELLOW = (255, 255, 0)       # color 3
YELLOW_GREEN = (125, 255, 0) # color 4
GREEN  = (0, 255, 0)         # color 5
TURQUOISE = (0, 255, 125)    # color 6
CYAN = (0, 255, 255)         # color 7 light blue
CYAN_BLUE = (0, 125, 255)    # color 8 
BLUE = (0, 0, 255)           # color 9
VIOLET = (125, 0, 255)       # color 10
MAGENTA = (255, 0, 255)      # color 11
MAGENTA_RED = (255, 0, 125)  # color 12
COLOR_LIST = [WHITE_BRIGHT, RED, ORANGE, YELLOW, YELLOW_GREEN, GREEN, TURQUOISE, CYAN, CYAN_BLUE, BLUE, VIOLET, MAGENTA, MAGENTA_RED]

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

def all_color(egpg=None, colornum=5):
        if colornum < len(COLOR_LIST):
            egpg.set_led(egpg.LED_WIFI,COLOR_LIST[colornum][0], COLOR_LIST[colornum][1], COLOR_LIST[colornum][2])
            egpg.set_eye_color(COLOR_LIST[ colornum ]) 
            egpg.open_eyes()
        else:
            print("ERROR: all_color({}) larger than {}".format(colornum,len(COLOR_LIST)))

def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--set", action="store", default=None, help="set all leds 'on' or 'off'")
    ap.add_argument("-c", "--colornum", type=int, action="store", default=None, help="set all leds to color ")
    args = vars(ap.parse_args())
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    myconfig.setParameters(egpg)
    set = args["set"]
    colornumber = args['colornum']

    if set==None:
        if colornumber == None:
            print("leds.py: Test all_on()")
            all_on(egpg)
            sleep(5)
            print("leds.py: Test all_off()")
            all_off(egpg)
        else:
            all_color(egpg,colornumber)
    elif set=='on':
        all_on(egpg)
    else:
        all_off(egpg)

if (__name__ == '__main__'): main()
