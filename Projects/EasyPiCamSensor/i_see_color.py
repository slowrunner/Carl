#!/usr/bin/env python3

# File: i_see_color.py [-v] [-h]

# Usage: i_see_color.py [-h] [-v]

# optional arguments:
#   -h, --help     show this help message and exit
#   -v, --verbose  optional speak results


# Report opinion of what color is held in front of the camera
# Using either RGB or HSV values for color matching method

# Note:  RGB has better performance and is the default method

# Uses Pi Camera via the EasyPiCamSensor class color() method
#     which returns a center pixel color estimate

# Talks using espeak-ng via the espeakng Python module

import traceback

try:
    import easypicamsensor
except:
    print("Could not locate easypicamsensor.py")
    traceback.print_exc()
    exit(1)

import time

# ARGUMENT PARSER (to add optional -v or --verbose to speak results using TTS
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-v","--verbose", default=False, action='store_true',help="optional speak results")
args = vars(ap.parse_args())
verbose = args['verbose']

if verbose:
    try:
        import espeakng
    except:
        print("espeakng Python module not available")
        print("Please run: pip3 install espeakng")
        exit(1)

def print_w_date_time(alert):
    time_now = time.strftime("%Y-%m-%d %H:%M:%S")
    print("{} i_see_color.py: {}".format(time_now, alert))

def main():

    if verbose: tts= espeakng.Speaker()   # set up default text-to-speech object

    print("Starting i_see_color.py")
    alert = "Warming Up The Camera"
    print(alert)
    if verbose: tts.say(alert)
    epcs = easypicamsensor.EasyPiCamSensor()  # creates 320x240 10FPS sensor

    current = epcs.color()   # get initial color
    last = "startup"

    print("\n")
    alert = "Select Color Matching Method"
    print(alert)
    if verbose:
        tts.say(alert)
        time.sleep(2)

    alert = "For RGB, Enter 1 or just press Return"
    print(alert)
    if verbose:
        tts.say(alert)
        time.sleep(3)

    alert = "For HSV, Enter 2"
    print(alert)
    if verbose:
        tts.say(alert)

    try:
        selection = input("Color Match Method [RGB]: ")
    except KeyboardInterrupt:
        selection = "EXIT"

    if (selection == '') or (selection == "1"):
        match_method = "RGB"
    elif (selection == "2"):
        match_method = "HSV"


    while  (selection != "EXIT"):
        try:
            # current = epcs.color()  # returns only the color
            current,dist,method = epcs.color_dist_method(method=match_method)  # returns the color, distance from nearest color, and method
            if (current != last):
                # new color estimate
                last = current
                alert = "New color: {} dist: {} method: {}".format(current,dist,method)
                print_w_date_time(alert)
                alert = "I think I see {}?".format(current)
                print_w_date_time(alert)
                print("\n")
                if verbose: tts.say(alert)


            time.sleep(2)    # wait between checks
        except KeyboardInterrupt:
            break

    alert = "Sure.  Exiting stage right."
    print("\n")  # move to new line after ^C
    print_w_date_time(alert)
    if verbose:
        tts.say(alert)
        time.sleep(2)



if __name__ == '__main__': main()
