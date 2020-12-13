#!/usr/bin/env python3

# file: i_see_motion.py

# Report when left,right,up,down motion occurs

# Uses Pi Camera via the EasyPiCamSensor class motion_x_y() method
#     which returns {'unknown','none','left','right'},{'unknown','none','up','down'}
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

def print_w_date_time(alert,event_time):
    if event_time is None: event_time = dt.datetime.now()
    str_event_time = event_time.strftime("%Y-%m-%d %H:%M:%S")
    print("\n{} Motion(): {}".format(str_event_time,alert))

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
                if (motion_x == 'none'):
                    alert = "Somthing moved {}".format(motion_y)
                elif (motion_y == 'none'):
                    alert = "Somthing moved {}".format(motion_x)
                else:
                    alert = "Somthing moved {} and {}".format(motion_x,motion_y)
                print_w_date_time(alert,motion_dt)
                # tts.say(alert)


            time.sleep(1)    # wait between checks
        except KeyboardInterrupt:
            alert = "Sure.  Exiting stage right."
            print("\n")  # move to new line after ^C
            print_w_date_time(alert,dt.datetime.now())
            # tts.say(alert)
            time.sleep(2)
            exit(0)



if __name__ == '__main__': main()
