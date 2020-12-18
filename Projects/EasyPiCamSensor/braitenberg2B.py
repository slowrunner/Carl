#!/usr/bin/env python3

# FILE: braitenberg2B.py

# USAGE:  ./braitenberg2B.py         Implements Braitenberg Vehicle 2b (with obstacle inhibition)
#         ./braitenberg2B.py -h      Show help message and exit
#         ./braitenberg2B.py -v      Robot provides spoken commentary on current stimulus and response
#         ./braitenberg2B.py -g 2    Amplify light difference (default is 1.5)
#         ./braitenberg2B.py -s      Show image from PiCamera in window

#          usage: braitenberg2B.py [-h] [-v] [-g GAIN] [-s]

#          optional arguments:
#            -h, --help                 show this help message and exit
#            -v, --verbose              optional speak results
#            -g GAIN, --gain GAIN       light difference amplification gain [1.5] 
#            -s, --show                 show image from PiCamera in window


# PURPOSE:  Demonstrate Easy PiCamera Sensor as two (left and right) light intensity sensors
#           using Braitenberg Vehicle 2B: https://en.wikipedia.org/wiki/Braitenberg_vehicle


# OPERATION:

#     Braitenberg Vehicle 2B has two symmetric sensors (left and right light detectors)
#     with each one stimulating a wheel on the opposite side of the body

#     It obeys the following rule:
#         More light left -> right wheel turns faster -> turns towards the left, closer to the light

#     This simulation implements a light difference amplification when optional gain > 1.0
#         The default gain of 1.5 gave the most reliable light seeking success for my GoPiGo3

#     The following rule is not part of the Vehicle 2B definition - Added for vehicle protection:
#         If the vehicle is too close to an obstacle, all motion is inhibited.

#     Uses Pi Camera via the EasyPiCamSensor class light_left_right() method
#     which returns an intensity value between 0 and 100 for left half and right half of sensor
#     for the stimulus

#     Uses EasyGoPiGo3.steer(left_percent,right_percent) to drive wheels
#       and stop() when too close to an obstacle

#     Uses the easy_distance_sensor.read() which returns distance in cm

#     Talks using espeak-ng via the espeakng Python module


# CONFIGURATIONS:
max_speed = 150    # speed when a light sensor reports maximum light (100)
obstacle_limit_cm =  20  # stop completely if obstacle within limit distance
stimulus_bias = 20  # add to both sides

# IMPORTS
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
import matplotlib.pyplot as plt
import matplotlib.image as mplimg

# ARGUMENT PARSER (to add optional -v or --verbose to speak results using TTS
ap = argparse.ArgumentParser()
ap.add_argument("-v","--verbose", default=False, action='store_true',help="optional speak results")
ap.add_argument("-g","--gain", default=1.5, type=float, help="light difference amplification gain [1.5]")
ap.add_argument("-s","--show", default=False, action='store_true',help="show PiCam image in window")
args = vars(ap.parse_args())
verbose = args['verbose']
gain = float(args['gain'])
show = args['show']


# UTILITIES

def print_w_date_time(alert,event_time=None):
    if event_time is None: event_time = dt.datetime.now()
    str_event_time = event_time.strftime("%Y-%m-%d %H:%M:%S")
    print("{} {}".format(str_event_time,alert))


# AMPLIFY_DIFF(left,right,amplifier) will amplify the difference between left and right values
#    Examples for input values: left 30, right 20
#    gain 1: difference in 10, difference out 10

#    gain 2: difference in 10, difference out 20
#            output values:  left 35, right 15 
def amplify_diff(left,right,amplifier):
    amp_diff = (left - right) * (amplifier-1.0) / 2.0  # gain of 1 gives zero amplification
    left_out = (left + amp_diff)
    right_out = (right - amp_diff)
    if left_out < 0: left_out = 0
    if right_out < 0: right_out = 0
    return left_out,right_out

def apply_bias(left,right,bias):
    return left+bias,right+bias

# ** MAIN **

def main():
    # Instantiate an Easy GoPiGo3 robot object
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)

    # Instantiate an Easy Distance Sensor object using HARDWARE I2C (for reliability)
    try:
        egpg.ds = egpg.init_distance_sensor(port='RPI_1')
    except Exception as e:
        print("Exception instantiating Dexter/ModRobotics I2C Distance Sensor")
        print(str(e))
        exit(1)

    # Instantiate a Text-To-Speech Object
    egpg.tts= espeakng.Speaker()   # set up default text-to-speech object

    alert = "Starting Braitenberg Vehicle 2B with gain of {} in 5 seconds".format(gain)
    print_w_date_time(alert)
    if verbose: egpg.tts.say(alert)

    # Instantiate an Easy PiCamera Sensor object (5 second camera warm-up)
    egpg.epcs = easypicamsensor.EasyPiCamSensor()  # creates 320x240 10FPS sensor


    # set max speed 
    egpg.set_speed(max_speed)

    # save current sensor view to file
    egpg.epcs.save_image_to_file('start_braitenburg2B.jpg')

    if show:
        img_cnt = 1
        img = egpg.epcs.get_image()
        imgplot = plt.imshow(img)
        # plt.show()
        plt.pause(1)

    try:
        while True:
            # Sense distance to any obstacle in front
            distance_ahead_in_cm = egpg.ds.read()

            # Perform Braitenberg Vehicle 2B LOOP:
            # Check forward path is clear
            while distance_ahead_in_cm > obstacle_limit_cm:

                # No obstruction

                # Read (virtual) left and right light sensors
                left_light,right_light = egpg.epcs.light_left_right()

                # Apply requested amplification to the difference between the light values
                left_stimulus,right_stimulus = amplify_diff(left_light,right_light,gain)

                # Apply bias
                left_stimulus, right_stimulus = apply_bias(left_stimulus,right_stimulus,stimulus_bias)

                # Report input values and response values
                alert = "light -    left: {:>5.1f} right: {:>5.1f} dist: {}".format(
                                  left_light,right_light,distance_ahead_in_cm)
                print_w_date_time(alert)
                alert = "Stimulus - left: {:>5.1f} right: {:>5.1f} gain: {}".format(
                                  left_stimulus,right_stimulus,gain)
                print_w_date_time(alert)
                print("\n")

                if left_light > right_light:
                    alert = "left"
                else:
                    alert = "right"
                if verbose: egpg.tts.say(alert)

                # set max speed each time allows for multiple egpg programs initializing speed
                # egpg.set_speed(max_speed)
                # time.sleep(0.1)

                # Braitenberg Vehicle 2B definition:
                # Connect left light to right wheel, right light to left wheel
                # (This implementation adds configurable difference amplifier)
                egpg.steer(right_stimulus,left_stimulus)

                # Display what bot is seeing for -s option
                if show:
                    img_cnt += 1
                    if (img_cnt % 30) == 1:
                        img = egpg.epcs.get_image()
                        imgplot = plt.imshow(img)
                        plt.pause(0.0001)

                # Sense distance to any obstacle in front
                distance_ahead_in_cm = egpg.ds.read()

            # obstruction seen
            egpg.stop()
            alert = "Obstruction at {:.0f} centimeters".format(distance_ahead_in_cm)
            print_w_date_time(alert)
            if verbose: egpg.tts.say(alert)
            time.sleep(2)
    except KeyboardInterrupt:
        # Stop vehicle loop and prepare to exit

        # Stop all forward motion immediately
        egpg.stop()

        # Report exiting
        alert = "Sure.  Exiting Braitenberg2B.py"
        print("\n")  # move to new line after ^C
        print_w_date_time(alert)
        if verbose: 
           alert = "Sure.  Exiting Braitenberg Vehicle 2 B."
           egpg.tts.say(alert)

        # save final sensor view to file
        egpg.epcs.save_image_to_file('final_braitenburg2B.jpg')

        # Close any open image view windows
        if show:
           plt.close('all')

        # Allow everything to stop/close/finish
        time.sleep(2)

        # EXIT MAIN and braitenberg2B.py
# END MAIN()



if __name__ == '__main__': main()
