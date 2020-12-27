#!/usr/bin/env python3

# file: i_see_color.py

# Report opinion of what color is held in front of the camera

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

def print_w_date_time(color):
    time_now = time.strftime("%Y-%m-%d %H:%M:%S")
    print("\n{} Color Estimate {}".format(time_now, color))

def main():

    epcs = easypicamsensor.EasyPiCamSensor()  # creates 320x240 10FPS sensor
    tts= espeakng.Speaker()   # set up default text-to-speech object

    current = epcs.color()   # get initial color
    last = current
    print_w_date_time(current)

    while  True:
        try:
            # current = epcs.color()  # returns only the color
            current,dist,method = epcs.color_dist_method()  # returns the color, distance from nearest color, and method
            if (current != last):
                # new color estimate
                last = current
                alert = "New color: {} dist: {} method: {}".format(current,dist,method)
                print_w_date_time(alert)
                alert = "Is that {}?".format(current)
                print_w_date_time(alert)
                tts.say(alert)


            time.sleep(2)    # wait between checks
        except KeyboardInterrupt:
            alert = "Sure.  Exiting stage right."
            print("\n")  # move to new line after ^C
            print_w_date_time(alert)
            tts.say(alert)
            time.sleep(2)
            exit(0)



if __name__ == '__main__': main()
