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
    Carl = True
except:
    Carl = False

import os
import picamera
import numpy as np
from picamera.array import PiMotionAnalysis
import datetime
import random

# A simple demo of sub-classing PiMotionAnalysis to construct a motion detector

MOTION_MAGNITUDE = 60   # the magnitude of vectors required for motion
MOTION_VECTORS = 10     # the number of vectors required to detect motion
HELLO_COUNT = 100       # if number of vectors over this, probably a big person movement
GREETINGS = ["hi", "hey", "hello", "greetings", "whats up?", "hi there", "howdy", "yo.", "I am glad you're home now","Did you bring me anything?"]
EXITS = ["come back soon", "will you be gone long", "dont go, i ull miss you", "can I go too?"]
availableExits = EXITS.copy()
availableGreetings = GREETINGS.copy()
time_last_spoke = datetime.datetime.now()
NoTalkingTimeout = 60

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
            print('{}: Detected motion -vectors: {} ave mag: {:.0f}'.format(timeStrNow,vector_count,ave_motion))
            print('Trend {:.1f}:'.format(trend_lr))
            if (vector_count > HELLO_COUNT):
                if  ( (dtNow - time_last_spoke).total_seconds() > NoTalkingTimeout ):
                      if trend_lr > 0: response = getExit()
                      else: response = getGreeting()
                      if Carl: speak.say(response,100)
                      time_last_spoke = dtNow
                      print("\n\n***** ", response)

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
                camera.wait_recording(1)
        except KeyboardInterrupt:
            keepLooping = False
        finally:
            camera.stop_recording()
            if Carl:  runLog.logger.info("Exit")
