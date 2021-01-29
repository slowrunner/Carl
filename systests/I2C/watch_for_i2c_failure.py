#!/usr/bin/env python3

# FILE: watch_for_i2c_failure.py

# USAGE:  ./watch_for_i2c_failure.py      print motion detections, speak i2c bus issue
#         ./watch_for_i2c_failure.py -v   print and speak detections, speak i2c bus issue
#         ./watch_for_i2c_failure.py -h   print help

# PURPOSE:  Stress sensor to find fatal i2c bus Errno 121


# OPERATION:
#     Reports when left,right,up,down motion occurs
#     Checks for motion occurred since last check 10 times per second
#     (easypicamsensor uses a rolling 3 frames at 10fps to detect motion)
#
#     Checks DistanceSensor using HW i2c, bus failure occurred if distance is zero.
#
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

import easygopigo3

import time
import datetime as dt
import argparse
import traceback


# ARGUMENT PARSER (to add optional -v or --verbose to speak results using TTS
ap = argparse.ArgumentParser()
ap.add_argument("-v","--verbose", default=False, action='store_true',help="optional speak results")
args = vars(ap.parse_args())
verbose = args['verbose']


def print_w_date_time(alert,event_time=None):
    if event_time is None: event_time = dt.datetime.now()
    str_event_time = event_time.strftime("%Y-%m-%d %H:%M:%S")
    print("\n{} watch_for_i2c_failure:: {}".format(str_event_time,alert))



# ** MAIN **

def main():
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    print_w_date_time("Easy Go Pi Go Instantiated")

    egpg.ds = egpg.init_distance_sensor()
    print_w_date_time("Easy Distance Sensor Instantiated")

    epcs = easypicamsensor.EasyPiCamSensor()  # creates 320x240 10FPS sensor
    print_w_date_time("Easy Pi Camera Sensor Instantiated")

    tts= espeakng.Speaker()   # set up default text-to-speech object

    motion_dt,motion_x,motion_y = epcs.motion_dt_x_y()   # get current motion sensor values
    print_w_date_time("Initial Motion: x:{} y:{}".format(motion_x,motion_y),motion_dt)

    current_dist_mm = egpg.ds.read_mm()
    ds_cm = current_dist_mm / 10.0
    ds_inch = current_dist_mm / 25.4
    print_w_date_time("Initial Distance: {:.1f} cm / {:.1f} inches".format(ds_cm,ds_inch))

    loop_cnt = 0

    while  True:
        loop_cnt += 1
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
                print_w_date_time("Sleeping for a second")
                time.sleep(1) # wait for a while after seeing motion

                epcs.motion_dt_x_y()  # throw away any motion during sleep
                alert = "Watching for motion again"
                if verbose: tts.say(alert)
                print_w_date_time(alert+"\n")

            try:
                current_dist_mm = egpg.ds.read_mm()
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except Exception as e:
                print_w_date_time("DISTANCE SENSOR EXCEPTION")
                print(str(e))
                current_dist_mm = 0

            if current_dist_mm == 0:
                alert = "Probable I 2 C bus failure"
                print_w_date_time(alert)
                tts.say(alert)
                time.sleep(30)
            else:
                if ( (loop_cnt % 100) == 1 ):
                    ds_cm = current_dist_mm / 10.0
                    ds_inch = current_dist_mm / 25.4
                    alert = "Distance: {:.1f} cm / {:.1f} inches".format(ds_cm,ds_inch)
                    print_w_date_time(alert)
                    if verbose: tts.say(alert)
            time.sleep(0.001)    # be a nice process
        except KeyboardInterrupt:
            alert = "Sure.  Exiting stage right."
            print("\n")  # move to new line after ^C
            print_w_date_time(alert,dt.datetime.now())
            if verbose: tts.say(alert)
            time.sleep(2)
            exit(0)
        except Exception as e:
            print("watch_for_i2c_failure main loop exception" + str(e))
            traceback.print_exc()


if __name__ == '__main__': main()
