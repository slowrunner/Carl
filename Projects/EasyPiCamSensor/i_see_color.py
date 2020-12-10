#!/usr/bin/env python3

# file: i_see_color.py

# Report opinion of what color is held in front of the camera

# Uses Pi Camera via the EasyPiCamSensor class color() method
#     which returns a center pixel color estimate

# Talks using espeak-ng via the espeakng Python module
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

import time

def print_w_date_time(color):
    time_now = time.strftime("%Y-%m-%d %H:%M:%S")
    print("\n{} Color Estimate {}".format(time_now, color))

def main():

    epcs = easypicamsensor.EasyPiCamSensor()  # creates 320x240 10FPS sensor
    tts= espeakng.Speaker()   # set up default text-to-speech object

    current = epcs.color()   # get average image light intensity now
    last = current

    print_w_date_time(current)

    while  True:
        try:
            # current = epcs.color(verbose=True)
            current = epcs.color()
            if (current != last):
                # new color estimate
                last = current
                print_w_date_time(current)

                alert = "Is that {}?".format(current)
                print_w_date_time(alert)
                tts.say(alert)


            time.sleep(1)    # wait between checks
        except KeyboardInterrupt:
            alert = "Sure.  Exiting stage right."
            time_now = time.strftime("%Y-%m-%d %H:%M:%S")
            print("\n{} {}".format(time_now, alert))
            tts.say(alert)
            time.sleep(2)
            exit(0)



if __name__ == '__main__': main()
