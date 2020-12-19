#!/usr/bin/env python3

# FILE: simple_braitenberg2A.py

# USAGE:  ./simple_braitenberg2A.py  Implements Braitenberg Vehicle 2a (with obstacle inhibition)

# PURPOSE:  Demonstrate Easy PiCamera Sensor as two (left and right) light intensity sensors
#           using Braitenberg Vehicle 2a: https://en.wikipedia.org/wiki/Braitenberg_vehicle
#           that exhibits "don't like light" synthetic emotion

# OPERATION:

#     Braitenberg Vehicle 2a has two symmetric sensors (left and right light detectors)
#     with each one stimulating the wheel on the respective side of the body

#     It obeys the following rule:
#         More light left -> left wheel turns faster -> turns towards the right, away from the light

#     The following rule is not part of the Vehicle 2a definition - Added for vehicle protection:
#         If the vehicle is too close to an obstacle, all motion is inhibited.

#     Uses Pi Camera via the EasyPiCamSensor class light_left_right() method
#     which returns an intensity value between 0 and 100 for left half and right half of sensor
#     for the stimulus

#     Uses EasyGoPiGo3.steer(left_percent,right_percent) to drive wheels
#       and stop() when too close to an obstacle

#     Uses the easy_distance_sensor.read() which returns distance in cm


# CONFIGURATIONS:
max_speed = 150    # speed when a light sensor reports maximum light (100)
obstacle_limit_cm =  20  # stop completely if obstacle within limit distance

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
    # requires an easygopigo3.py with corrected steer(l,r) method
    import easygopigo3
except Exception as e:
    print("This program must be run on a GoPiGo3")
    print(str(e))
    exit(1)

import time
import datetime as dt
import numpy as np

# UTILITIES

def print_w_date_time(alert,event_time=None):
    if event_time is None: event_time = dt.datetime.now()
    str_event_time = event_time.strftime("%Y-%m-%d %H:%M:%S")
    print("{} {}".format(str_event_time,alert))


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

    alert = "Starting Braitenberg Vehicle 2a in 5 seconds"
    print_w_date_time(alert)

    # Instantiate an Easy PiCamera Sensor object (5 second camera warm-up)
    egpg.epcs = easypicamsensor.EasyPiCamSensor()  # creates 320x240 10FPS sensor


    # set max speed
    egpg.set_speed(max_speed)

    # save current sensor view to file
    egpg.epcs.save_image_to_file('start_braitenburg2a.jpg')

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
                left_stimulus = left_light
                right_stimulus = right_light

                # Report input values and response values
                alert = "light -    left: {:>5.1f} right: {:>5.1f} dist: {}".format(
                                  left_light,right_light,distance_ahead_in_cm)
                print_w_date_time(alert)
                alert = "Stimulus - left: {:>5.1f} right: {:>5.1f}".format(
                                  left_stimulus,right_stimulus)
                print_w_date_time(alert)

                if left_light > right_light:
                    alert = "left"
                else:
                    alert = "right"
                print_w_date_time(alert)
                print("\n")

                # Braitenberg Vehicle 2a definition:
                # Connect left light to left wheel, right light to right wheel
                # (This implementation adds configurable difference amplifier)
                egpg.steer(left_stimulus,right_stimulus)

                # Sense distance to any obstacle in front
                distance_ahead_in_cm = egpg.ds.read()

            # obstruction seen
            egpg.stop()
            alert = "Obstruction at {:.0f} centimeters".format(distance_ahead_in_cm)
            print_w_date_time(alert)
            time.sleep(2)
    except KeyboardInterrupt:
        # Stop vehicle loop and prepare to exit

        # Stop all forward motion immediately
        egpg.stop()

        # Report exiting
        alert = "Sure.  Exiting Braitenberg2B.py"
        print("\n")  # move to new line after ^C
        print_w_date_time(alert)

        # save final sensor view to file
        egpg.epcs.save_image_to_file('final_braitenburg2a.jpg')

        # Allow everything to stop/close/finish
        time.sleep(2)

        # EXIT MAIN and simple_braitenberg2a.py
# END MAIN()



if __name__ == '__main__': main()
