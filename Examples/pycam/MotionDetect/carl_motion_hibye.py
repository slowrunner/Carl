#!/usr/bin/env python3
#  Needs python3 for list.copy()
#
# file: motion_detect.py
#
# based on https://github.com/waveform80/picamera_demos
#
# Motion Detect using picamera and numpy only
#
#   Selects a response based on motion trend to left (exits) or to right (greetings)
#   If running on my robot Carl, it speaks the responses


import sys
sys.path.append('/home/pi/Carl/plib/')
try:
    import speak
    import runLog
    import carlDataJson as cdj
    Carl = True
except:
    Carl = False

import os
import picamera
import numpy as np
from picamera.array import PiMotionAnalysis
import datetime
import random
from time import sleep
import argparse

# ARGUMENT PARSER
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--verbose", default=False, action='store_true', help="print info to console")
ap.add_argument("-d", "--debug", default=False, action='store_true', help="print detailed info to console")
args = vars(ap.parse_args())
verbose = args['verbose']     # value True or False
debug = args['debug']
if debug: verbose = True


# A simple demo of sub-classing PiMotionAnalysis to construct a motion detector

MOTION_MAGNITUDE = 60   # the magnitude of vectors required for motion
MOTION_VECTORS = 15 # 10     # the number of vectors required to detect motion
HELLO_COUNT = 100       # if number of vectors over this, probably a big person movement
GREETINGS = ["hi", "hello", "greetings earthling", "shah lowm.", "whats up?", "hi there", "I am glad you're here","Did you bring me anything?", "welcome back", "good morning, afternoon, evening, which ever the case may be", "Hows it going?", "Whats new?", "Hows everything?", "Hows your day going?", "Good to see you", "Nice to see you", "Long time no see.", "Halv you been?", "Hiya!", "Hows it going?", "Lovely to see you.", "hey there."]
EXITS = ["I hope yull come back soon.", "will you be gone long?", "i ull miss you.", "can I go with you?", "take care", "be careful out there.", "see you soon?", "Later.", "until next time.", "shah lowm", "leh heat rah oat"]
availableExits = EXITS.copy()
availableGreetings = GREETINGS.copy()
time_last_spoke = datetime.datetime.now()
NoTalkingTimeout = 60
sleeping = True
NOTDOCKED = 1

def getGreeting():
    global availableGreetings

    response = random.choice(availableGreetings)
    availableGreetings.remove(response)
    if (len(availableGreetings) == 0):
      availableGreetings = GREETINGS.copy()
    return response

def getExit():
    global availableExits

    response = random.choice(availableExits)
    availableExits.remove(response)
    if (len(availableExits) == 0):
      availableExits = EXITS.copy()
    return response

class MyMotionDetector(PiMotionAnalysis):

    def analyse(self, a):
        global time_last_spoke

        if not sleeping:

            raw_a = a
            # calc motion trend left or right
            trend_lr = np.mean(raw_a['x'].astype(np.float))  # negative for moving right, postive for moving left


            # Calculate the magnitude of all vectors with pythagoras' theorem
            a = np.sqrt(
                np.square(a['x'].astype(np.float)) +
                np.square(a['y'].astype(np.float))
                ).clip(0, 255).astype(np.uint8)
            # Count the number of vectors with a magnitude greater than our
            # threshold
            dtNow = datetime.datetime.now()
            vector_count = (a > MOTION_MAGNITUDE).sum()
            if vector_count > MOTION_VECTORS:
                ave_motion = np.average(a)
                timeStrNow = dtNow.strftime("%H:%M:%S.%f")[:12]
                if debug:
                    if trend_lr >= 0:
                        trend_lr_str = "Left"
                    else:
                        trend_lr_str = "Right"
                    print('{}: carl_motion_hibye: Detected motion -vectors: {} ave mag: {:.0f} Trend: {}'.format(timeStrNow,vector_count,ave_motion,trend_lr_str))
                    # print('Trend {:.1f}:'.format(trend_lr))
                if (vector_count > HELLO_COUNT):
                    if  ( (dtNow - time_last_spoke).total_seconds() > NoTalkingTimeout ):
                          if trend_lr > 0: response = getExit()
                          else: response = getGreeting()
                          if Carl: speak.say(response,100)
                          time_last_spoke = dtNow
                          if verbose: print('{}: carl_motion_hibye: **** {}'.format(timeStrNow,response))
                    else:
                        if verbose: print('{}: carl_motion_hibye: Holding my tongue'.format(timeStrNow))

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 24

    with MyMotionDetector(camera) as motion_detector:
        camera.start_recording(
            os.devnull, format='h264', motion_output=motion_detector)
        keepLooping = True
        try:
            if Carl:  runLog.logger.info("Started")
            while keepLooping:
                if (cdj.getCarlData("dockingState") == NOTDOCKED):
                    sleeping = False
                    camera.wait_recording(1)
                else:
                    sleeping = True
                    dtNow = datetime.datetime.now()
                    timeStrNow = dtNow.strftime("%H:%M:%S.%f")[:12]
                    if verbose: print('{}: carl_motion_hibye: sleeping'.format(timeStrNow))
                    sleep(10)
        except KeyboardInterrupt:
            keepLooping = False
            print("\n")  # leave ^C on line by itself
        finally:
            camera.stop_recording()
            if Carl:  runLog.logger.info("Exit")
