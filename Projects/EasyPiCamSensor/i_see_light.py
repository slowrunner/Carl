#!/usr/bin/env python3

# file: i_see_light.py

# Usage:  ./i_see_light.py

# Comments when someone turns a room light on or off
# IF has not spoken in the last 10 seconds

# Uses Pi Camera via the EasyPiCamSensor class light() method
#     which returns average light intensity value of 0-100

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

def print_w_date_time(reading):
    time_now = time.strftime("%Y-%m-%d %H:%M:%S")
    print("\n{} Intensity now {:.1f}".format(time_now, reading))


epcs = easypicamsensor.EasyPiCamSensor()  # creates 320x240 10FPS sensor
tts= espeakng.Speaker()   # set up default text-to-speech object

current_intensity = epcs.light()   # get average image light intensity now
last_intensity = current_intensity
think_before_talking_again = 10    # wait 10 seconds before talking again
just_said_something = 0
threshold = 7    # required intensity change before commenting

print_w_date_time(current_intensity)

while  True:
    try:
        current_intensity = epcs.light()
        if (current_intensity - last_intensity) > threshold:
                # someone turned a light on
                last_intensity = current_intensity
                print_w_date_time(current_intensity)

                alert = "Thanks, it was kind of dark over here"
                print(alert)
                if just_said_something == 0:
                    tts.say(alert)
                    just_said_something = think_before_talking_again

        elif (last_intensity - current_intensity) > threshold:
                # someone turned a light off
                last_intensity = current_intensity
                print_w_date_time(current_intensity)

                alert = "Did you know I'm afraid of the dark?"
                print(alert)
                if just_said_something == 0:
                    tts.say(alert)
                    just_said_something = think_before_talking_again

        time.sleep(1)    # wait 1 second between checks
        if just_said_something > 0: just_said_something -= 1
    except KeyboardInterrupt:
        alert = "Sure.  Exiting stage right."
        time_now = time.strftime("%Y-%m-%d %H:%M:%S")
        print("\n{} {}".format(time_now, alert))
        tts.say(alert)
        time.sleep(2)
        exit(0)



