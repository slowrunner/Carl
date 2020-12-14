#!/usr/bin/env python3

# FILE: face_the_light.py

# USAGE:  ./face_the_light.py     Robot scans light for 360 degrees, then turns to face brightest direction
#         ./face_the_light.py -v  Robot commentates scanning and turning to face the light
#         ./face_the_light.py -h  Show help message and exit

#          usage: face_the_light.py [-h] [-v]

#          optional arguments:
#            -h, --help     show this help message and exit
#            -v, --verbose  optional speak results

# OPERATION:
#     Uses Pi Camera via the EasyPiCamSensor class light() method
#     which returns an intensity value between 0 and 100

#     Talks using espeak-ng via the espeakng Python module

#     Spin turns use EasyGoPiGo3.turn_degrees(x,blocking=True)

# CONFIGURATIONS:
turn_speed = 150   # speed that makes spin turns on your robot most accurate

# Select num_readings by precision desired: (precision will be half the turn_angle)
#    8 readings (45deg turn_angle) = +/-22.5deg precision, 12=+/-15 deg, 24=+/-7.5 deg
#    Make sure turn_angle is less than camera FOV, 53 degrees, (more than 7 turns)
num_readings = 8  

import sys
if sys.version_info < (3,5):
    print("This program must be run with python3")
    exit(1)

try:
    import easypicamsensor
except:
    print("Could not locate easypicamsensor.py")
    exit(1)

try:
    import espeakng
except:
    print("espeakng Python module not available")
    print("Please run: pip3 install espeakng")
    exit(1)
try:
    import easygopigo3
except:
    print("This program must be run on a GoPiGo3")
    exit(1)

import time
import argparse
import datetime as dt
import numpy as np


# ARGUMENT PARSER (to add optional -v or --verbose to speak results using TTS
ap = argparse.ArgumentParser()
ap.add_argument("-v","--verbose", default=False, action='store_true',help="optional speak results")
args = vars(ap.parse_args())
verbose = args['verbose']




def print_w_date_time(alert,event_time=None):
    if event_time is None: event_time = dt.datetime.now()
    str_event_time = event_time.strftime("%Y-%m-%d %H:%M:%S")
    print("\n{} {}".format(str_event_time,alert))

def do_360_light_scan(egpg,verbose=False):
    first_heading = 0
    turn_angle = 360.0 / num_readings
    light_reading_for_heading = {}
    for heading in np.arange(first_heading,360.0,turn_angle):
        light_reading = egpg.epcs.light()
        light_reading_for_heading[int(heading)] = light_reading
        alert = "heading: {:.0f} light: {:.0f}".format(heading,light_reading)
        print_w_date_time(alert)
        if verbose: egpg.tts.say(alert)
        # set speed for best turn accuracy (each time allows for multiple egpg programs)
        egpg.set_speed(turn_speed)
        egpg.turn_degrees(turn_angle,blocking=True)
        time.sleep(1) # let sensor the light reading at this heading
    return light_reading_for_heading

def find_heading_for_max_reading(reading_by_heading_dict):
    heading_w_max_reading = max(reading_by_heading_dict, key=reading_by_heading_dict.get)
    # Don't need but this is how to get it
    # max_value = reading_by_heading_dict[heading_w_max_reading]
    return heading_w_max_reading


# ** MAIN **

def main():
    # Instantiate an Easy GoPiGo3 robot object
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)

    # Instantiate an Easy PiCamera Sensor object
    egpg.epcs = easypicamsensor.EasyPiCamSensor()  # creates 320x240 10FPS sensor

    # Instantiate a Text-To-Speech Object
    egpg.tts= espeakng.Speaker()   # set up default text-to-speech object

    try:
        light_reading_for_heading_dict = do_360_light_scan(egpg,verbose)
        heading_w_max_light = find_heading_for_max_reading(light_reading_for_heading_dict)
        max_light = light_reading_for_heading_dict[heading_w_max_light]
        alert = "max light value: {:.1f} seen at heading: {}".format(max_light,heading_w_max_light)
        print_w_date_time(alert)
        if verbose: egpg.tts.say(alert)
        time.sleep(2)
        alert = "Turning to heading {} to face the light".format(heading_w_max_light)
        print_w_date_time(alert)
        if verbose: egpg.tts.say(alert)
        # set speed for best turn accuracy
        egpg.set_speed(turn_speed)
        egpg.turn_degrees(heading_w_max_light, blocking=True)

    except KeyboardInterrupt:
        alert = "Sure.  Exiting stage right."
        print("\n")  # move to new line after ^C
        print_w_date_time(alert)
        if verbose: egpg.tts.say(alert)
        time.sleep(2)



if __name__ == '__main__': main()
