#!/usr/bin/env python3

# file: teach_me_colors.py

# Loop
#   Report opinion of what color is held in front of the camera
#   Ask if correct?
#   If "No", relearn one or all colors
#   Save color table in config_easypicamsensor.json.new


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

try:
    import espeakng
except:
    print("espeakng Python module not available")
    print("Please run: pip3 install espeakng")
    exit(1)

import time
import argparse


# ARGUMENT PARSER (to add optional -v or --verbose to speak results using TTS
ap = argparse.ArgumentParser()
ap.add_argument("-v","--verbose", default=False, action='store_true',help="optional speak results")
args = vars(ap.parse_args())
verbose = args['verbose']


def main():

    print("Warming Up The Camera")
    epcs = easypicamsensor.EasyPiCamSensor()  # creates 320x240 10FPS sensor
    if verbose: tts= espeakng.Speaker()   # set up default text-to-speech object
    print("Initialization Complete\n")

    last = ""
    while  True:
        try:
            alert = "Press Return To Test A Color"
            if verbose: tts.say(alert)
            print("\n")
            go = input(alert)
            current,dist,method = epcs.color_dist_method()  # returns the color, distance from nearest color, and method
            alert = "Color Estimate: {} dist: {} method: {}".format(current,dist,method)
            print(alert)
            alert = "Is that {}? ".format(current)
            if verbose: tts.say(alert)
            answer = input(alert)
            if (answer == "") or (answer[0]=='y'):
                pass
            else:
                print("Current Color Table")
                epcs.print_colors()

                epcs.learn_colors()

            time.sleep(1)    # wait between checks
        except KeyboardInterrupt:
            print("\n")  # move to new line after ^C
            if verbose:
                alert = "Saving colors to config easy pi cam sensor dot json dot new"
                tts.say(alert)
            epcs.save_colors(path="config_easypicamsensor.json.new")
            alert = "Saved colors to config_easypicamsensor.json.new"
            print(alert)

            alert = "Exiting teach_me_colors.py"
            print(alert)
            if verbose:
                alert = "Exiting teach me colors dot p y"
                tts.say(alert)
            time.sleep(2)
            exit(0)



if __name__ == '__main__': main()
