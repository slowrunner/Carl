#!/usr/bin/python3

# file: test_ocv_frame.py

# Capture frames to OpenCV array

# based on https://picamera.readthedocs.io/en/release-1.13/recipes2.html#capturing-to-an-opencv-object

# captures 2fps at 640x480
#   htop shows 8 process/threads 3% of processor 5% memory

# captures 2fps at 320x480 8 threads 1% of processor 5% memory


# imports

from picamera import PiCamera
import time
import cv2
import datetime as dt
import numpy as np

# CONSTANTS
HRES = 320
VRES = 240
#HRES = 640
#VRES = 480
FRAMERATE = 30
WARMUPSLEEP = 5


try:
    # init the camera and stabilize
    print("PiCamera Started and Stabilizing")
    camera = PiCamera()
    camera.resolution = (HRES, VRES)
    camera.framerate = FRAMERATE

    # allow camera to warmup
    time.sleep(WARMUPSLEEP)

    keepLooping = True
    loopCount = 0
    dtStart = dt.datetime.now()
    print("Capturing Frames")
    while keepLooping:
        loopCount+=1

        # create empty flat array to hold frames
        frame = np.empty((VRES * HRES * 3,), dtype=np.uint8)

        # capture frame from the camera
        camera.capture(frame, 'bgr')

        # reshape flat array to [[VRES],[HRES],[3]]
        frame = frame.reshape((VRES, HRES, 3))

        #strTime = dt.datetime.now().strftime('%H:%M:%S.%f')[:-3]
        #print('%s captured %dx%d frame in loop %d' % (
        #        strTime,  frame.shape[0], frame.shape[1], loopCount))

        # show the frame
        #cv2.imshow("Frame", image)
        #cv2.waitKey(1)

except KeyboardInterrupt:
    print("\n*** Ctrl-C detected - Finishing up")

finally:
    dtEnd = dt.datetime.now()
    print("Closing Camera")
    camera.close()
    time.sleep(1)
    captureDuration = (dtEnd - dtStart).total_seconds()
    fps = loopCount/captureDuration
    print("Captured {} {}x{} frames in {:.1f} seconds - Average FPS: {:.1f}".format(loopCount, HRES, VRES, captureDuration, fps))

