#!/usr/bin/env python3
#  Needs python3 for list.copy()
#
# file: motion_detect.py
#
# from https://github.com/waveform80/picamera_demos
#
# Motion Detect using picamera and numpy only
#


import sys
sys.path.append('/home/pi/Carl/plib/')
try:
    import speak
    import lifeLog
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
HELLO_COUNT = 300       # if number of vectors over this, probably a big person movement
GREETINGS = ["hi", "hey", "hello", "greetings", "whats up?", "hi there", "howdy", "yo.", "I am glad you're home now","Did you bring me anything?"]
availableGreetings = GREETINGS.copy()
okToSayHi = False

class MyMotionDetector(PiMotionAnalysis):
    def analyse(self, a):
        global okToSayHi, availableGreetings

        # Calculate the magnitude of all vectors with pythagoras' theorem
        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)
        # Count the number of vectors with a magnitude greater than our
        # threshold
        vector_count = (a > MOTION_MAGNITUDE).sum()
        if vector_count > MOTION_VECTORS:
            ave_motion = np.average(a)
            timeStrNow = datetime.datetime.now().strftime("%H:%M:%S.%f")[:12]
            print('{}: Detected motion -vectors: {} ave mag: {:.0f}'.format(timeStrNow,vector_count,ave_motion))
            if (vector_count > HELLO_COUNT):
                if  okToSayHi:
                    response = random.choice(availableGreetings)
                    availableGreetings.remove(response)
                    if (len(availableGreetings) == 0):
                        availableGreetings = GREETINGS.copy()
                    if Carl: speak.say(response)
                    print(response)
                    okToSayHi = False
            else:
                okToSayHi = True


with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 24

    with MyMotionDetector(camera) as motion_detector:
        camera.start_recording(
            os.devnull, format='h264', motion_output=motion_detector)
        keepLooping = True
        try:
            if Carl:  lifeLog.logger.info("Started")
            while keepLooping:
                camera.wait_recording(1)
        except KeyboardInterrupt:
            keepLooping = False
        finally:
            camera.stop_recording()
            if Carl:  lifeLog.logger.info("Exit")
