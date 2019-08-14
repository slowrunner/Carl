#!/usr/bin/python3

# file: test_ocv_video.py

# example capturing OpenCV frames as fast as possible from video stream

# based on https://www.pyimagesearch.com/2016/08/29/common-errors-using-the-raspberry-pi-camera-module/
# and https://github.com/waveform80/picamera/issues/195  for PiCameraValueError on ctrl-C


# At 640x480 captures at 29fps using 10-20% processor (desktop meter)  5% memory
# htop shows 7 process/threads 

# at 320x240 captures at 59fps using 10% processor (desktop meter) 5% memory


# imports

from picamera.array import PiRGBArray
from picamera import PiCamera
from picamera import PiCameraValueError
from picamera import PiCameraError

import time
import cv2
import datetime as dt


# CONSTANTS
HRES = 320
VRES = 240
#HRES = 640
#VRES = 480
FRAMERATE = 60
WARMUPSLEEP = 5

# init the camera
print("PiCamera Started and Stabilizing")
camera = PiCamera()
camera.resolution = (HRES, VRES)
camera.framerate = FRAMERATE
# allow camera to warmup
time.sleep(WARMUPSLEEP)

# PiRGBArray allows read frames from camera in NumPy format, compat with OpenCV
rawCapture = PiRGBArray(camera, size=(HRES, VRES))



try:
    keepLooping = True
    loopCount = 0
    dtStart = dt.datetime.now()
    print("Capturing Frames")
    # capture frames from the camera
    # use_video_port = True tells to treat the stream as video
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        loopCount += 1
        # grab the raw NumPy array image
        # array is 3-dim (width, height, numChannels)
        image = rawCapture.array

        # show th frame
        #cv2.imshow("Frame", image)
        #cv2.waitKey(1)


        # clear the stream in prep for next frame
        rawCapture.truncate(0)

#except PiCameraValueError:   # expected error when interrupt the capture_continuous
except PiCameraError:   # expected error when interrupt the capture_continuous
    print("\nStopping capture_continuous")

except KeyboardInterrupt:
    print("\n*** Ctrl-C detected - Finishing up")
    camera.close()
    time.sleep(1)
finally:
    dtEnd = dt.datetime.now()
    captureDuration = (dtEnd - dtStart).total_seconds()
    fps = loopCount/captureDuration
    print("Captured {} {}x{} frames in {:.1f} seconds - Average FPS: {:.1f}".format(loopCount, HRES, VRES, captureDuration, fps))

