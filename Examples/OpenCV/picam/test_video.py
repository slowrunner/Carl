#!/usr/bin/python3

# based on https://www.pyimagesearch.com/2016/08/29/common-errors-using-the-raspberry-pi-camera-module/

# example capturing frames from video stream
# htop shows 7 process/threads  and 24% of processor
# each thread is shown as using 8% of memory

# imports

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# CONSTANTS
HRES = 640
VRES = 480
FRAMERATE = 32

# init the camera and a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (HRES, VRES)
camera.framerate = FRAMERATE
# PiRGBArray allows read frames from camera in NumPy format, compat with OpenCV
rawCapture = PiRGBArray(camera, size=(HRES, VRES))

# allow camera to warmup
time.sleep(0.1)


try:

    # capture frames from the camera
    # 
    # use_video_port = True tells to treat the stream as video
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array image
        # array is 3-dim (width, height, numChannels)
        image = frame.array

        # show th frame
        cv2.imshow("Frame", image)
        cv2.waitKey(1)


        # clear the stream in prep for next frame
        rawCapture.truncate(0)
except KeyboardInterrupt:
    print("\n*** Ctrl-C detected - Finishing up")
    time.sleep(1)

