#!/usr/bin/env python3

# FILE: i_see_motion.py

# USAGE:  ./i_see_motion.py      print motion detections
#         ./i_see_motion.py -v   print and speak detections
#         ./i_see_motion.py -h   print help

# PURPOSE:  Demonstrate Easy Pi Camera Sensor motion detection


# OPERATION:
#     Reports when left,right,up,down motion occurs
#     Checks for motion occurred since last check 10 times per second
#     (easypicamsensor uses a rolling 3 frames at 10fps to detect motion)

#     Uses Pi Camera via the EasyPiCamSensor class motion_dt_x_y() method
#     which returns {None or datetime},{'none','left','right'},{'none','up','down'}
#
#     Talks using espeak-ng via the espeakng Python module

import sys
if sys.version_info < (3,5):
    print("This program must be run with python3")
    exit(1)

try:
    import easypicamsensor
except Exception as e:
    print("import easypicamsensor exception:")
    print(str(e))
    exit(1)

try:
    import espeakng
except:
    print("espeakng Python module not available")
    print("Please run: pip3 install espeakng")
    exit(1)

import time
import datetime as dt
import argparse


# ARGUMENT PARSER (to add optional -v or --verbose to speak results using TTS
ap = argparse.ArgumentParser()
ap.add_argument("-v","--verbose", default=False, action='store_true',help="optional speak results")
args = vars(ap.parse_args())
verbose = args['verbose']


def print_w_date_time(alert,event_time=None):
    if event_time is None: event_time = dt.datetime.now()
    str_event_time = event_time.strftime("%Y-%m-%d %H:%M:%S")
    print("\n{} Motion(): {}".format(str_event_time,alert))



# ** MAIN **

def main():

    epcs = easypicamsensor.EasyPiCamSensor()  # creates 320x240 10FPS sensor
    tts= espeakng.Speaker()   # set up default text-to-speech object

    motion_dt,motion_x,motion_y = epcs.motion_dt_x_y()   # get current motion sensor values
    print_w_date_time("Initial Motion: x:{} y:{}".format(motion_x,motion_y),motion_dt)

    while  True:
        try:
            # get current motion sensor state (and reset it to 'none')
            motion_dt,motion_x,motion_y = epcs.motion_dt_x_y()
            if (motion_dt is not None):
                # motion seen
                if (motion_x == 'none'):  # up or down movement seen
                    alert = "Somthing moved {}".format(motion_y)
                elif (motion_y == 'none'):  # left or right movement seen
                    alert = "Somthing moved {}".format(motion_x)
                else:  # both left/right and up/down movement seen
                    alert = "Somthing moved {} and {}".format(motion_x,motion_y)
                print_w_date_time(alert,motion_dt)
                if verbose: tts.say(alert)
                print("Sleeping for 5 seconds")
                time.sleep(5) # wait for a while after seeing motion

                epcs.motion_dt_x_y()  # throw away any motion during sleep
                alert = "Watching for motion again"
                if verbose: tts.say(alert)
                print_w_date_time(alert+"\n")
                continue       # skip the loop after motion seen (goes to the try:)

            time.sleep(0.1)    # wait between checks
        except KeyboardInterrupt:
            alert = "Sure.  Exiting stage right."
            print("\n")  # move to new line after ^C
            print_w_date_time(alert,dt.datetime.now())
            if verbose: tts.say(alert)
            time.sleep(2)
            exit(0)



if __name__ == '__main__': main()
