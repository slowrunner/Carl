#!/usr/bin/env python3

# FILE: i_see_colors_in_motion.py

# USAGE:  ./i_see_colors_in_motion.py      print motion detections
#         ./i_see_colors_in_motion.py -v   print and speak detections

# Report colors and left,right,up,down motion detections
# Checks color and for motion occurrance 1 times per second
# (easypicamsensor uses a rolling 3 frames at 10fps to detect motion)

# Uses Pi Camera via the EasyPiCamSensor class motion_dt_x_y() method
#     which returns {None or datetime},{'none','left','right'},{'none','up','down'}
#
# Talks using espeak-ng via the espeakng Python module

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

def main():

    epcs = easypicamsensor.EasyPiCamSensor()  # creates 320x240 10FPS sensor
    tts= espeakng.Speaker()   # set up default text-to-speech object

    motion_dt,motion_x,motion_y = epcs.motion_dt_x_y()   # get current motion sensor values
    print_w_date_time("Initial Motion: x:{} y:{}".format(motion_x,motion_y),motion_dt)
    current_color = epcs.color()
    last_color = current_color
    print_w_date_time("Initial Color(): {}".format(current_color))

    while  True:
        try:
            # get current motion sensor state (and reset it to 'none')
            motion_dt,motion_x,motion_y = epcs.motion_dt_x_y()
            if (motion_dt is not None):
                # motion seen
                move_color = epcs.color()
                if (motion_x == 'none'):
                    alert = "Somthing {} moved {}".format(move_color,motion_y)
                elif (motion_y == 'none'):
                    alert = "Somthing {} moved {}".format(move_color,motion_x)
                else:
                    alert = "Somthing {} moved {} and {}".format(move_color,motion_x,motion_y)
                print_w_date_time(alert,motion_dt)
                if verbose: tts.say(alert)
                print("Sleeping for 5 seconds")
                epcs.save_image_to_file("motion_capture.jpg")
                time.sleep(5) # wait for a while after seeing motion
                epcs.motion_dt_x_y()  # throw away any motion while waiting
                alert = "Watching for motion and colors again"
                if verbose: tts.say(alert)
                print_w_date_time(alert+"\n")
                continue       # skip the wait between checks
            current_color = epcs.color()
            if (current_color != last_color):
                last_color = current_color
                alert = "Is that {}?".format(current_color)
                print_w_date_time(alert)
                if verbose: tts.say(alert)

            time.sleep(1)    # wait between checks
        except KeyboardInterrupt:
            alert = "Sure.  Exiting stage right."
            print("\n")  # move to new line after ^C
            print_w_date_time(alert,dt.datetime.now())
            if verbose: tts.say(alert)
            time.sleep(2)
            exit(0)



if __name__ == '__main__': main()
