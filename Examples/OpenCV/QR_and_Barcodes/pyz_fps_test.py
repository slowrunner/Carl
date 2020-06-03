#!/usr/bin/env python3

# PYZBAR OPENCV QR and Barcode TEST

# USAGE
# ./pyz_fps_test.py
#    OPTIONS:
#    -d (--display) 1
#    -n (--numframes) 100

# import the necessary packages
from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
import numpy as np
from pyzbar import pyzbar
from datetime import datetime

import sys
sys.path.append('/home/pi/Carl/plib')
import camUtils

# CONSTANTS

CAMERA_RESOLUTION = (320, 240)
# CAMERA_RESOLUTION = (640, 480)
# CAMERA_RESOLUTION = (1280, 960)
# CAMERA_RESOLUTION = (2560, 1920)
CAMERA_BRIGHTNESS = 60  # 50 default
CAMERA_CONTRAST =   60 # 60    # 0 default
CAMERA_SHARPNESS =  25   # 0 default
CAMERA_AWB_MODE =   'incandescent'
CAMERA_FRAMERATE =  10


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--numframes", type=int, default=1,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())
show = args["display"]
num_frames_to_test = args["numframes"]


test_frame = None
processed_frame = None
annotated_frame = None
found_keep = ()
uniq_found_keep = ()

# OpenCV Processing
def processImage(image, show):
    global test_frame, processed_frame, annotated_frame, found_keep, uniq_found_keep

    # test_frame = image.copy()
    test_frame = camUtils.fixTiltOCV(image)

    # gray = cv2.cvtColor(test_frame, cv2.COLOR_BGR2GRAY)
    # gblur = cv2.GaussianBlur(gray, (5, 5), 0)
    # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 4)
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    # dilated = cv2.dilate(thresh, None, iterations=2)

    processed_frame = test_frame.copy()
    annotated_frame = test_frame.copy()

    try:
        codes = pyzbar.decode(processed_frame)
    except Exception as e:
        print("pyzbar.decode():", str(e))

    if codes is not None:
        time_found = datetime.now()
        for code in codes:
            # extract bounding box
            (x, y, w, h) = code.rect

            # code date is a bytes obj, so convert to string
            codeData = code.data.decode("utf-8")
            codeType = code.type
            found_keep += (code,)


            if show > 0:
                cv2.rectangle(annotated_frame, (x,y), (x+w, y+h), (255, 0, 0), 2)
                text = "{} ({})".format(codeData, codeType)
                cv2.putText(annotated_frame, text, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 0, 255), 1)

                print("{}  {}\n".format(time_found, codeData))

            if codeData not in uniq_found_keep:
                uniq_found_keep += (code,)

    if show > 0:
        cv2.imshow("frame", image)
        cv2.imshow("processed_frame", processed_frame)
        cv2.imshow("annotated", annotated_frame)
        cv2.waitKey(1) & 0xFF

# initialize the camera and stream
camera = PiCamera()
camera.resolution = CAMERA_RESOLUTION
camera.brightness = CAMERA_BRIGHTNESS
camera.contrast =   CAMERA_CONTRAST
camera.sharpness =  CAMERA_SHARPNESS
camera.awb_mode =   CAMERA_AWB_MODE
camera.framerate =  CAMERA_FRAMERATE

rawCapture = PiRGBArray(camera, size=CAMERA_RESOLUTION )

stream = camera.capture_continuous(rawCapture, format="bgr",
	use_video_port=True)

# allow the camera to warmup and start the FPS counter
print("[INFO] sampling frames from `picamera` module...")
time.sleep(2.0)
fps = FPS().start()

# loop over some frames
for (i, f) in enumerate(stream):
	# grab the frame from the stream 
        # resize it to have a max width of 400 pixels
	frame = f.array
	# frame = imutils.resize(frame, width=400)

	test_image = frame

	# Perform processing to see effect on fps
	processImage(test_image, show)

	# clear the stream in preparation for the next frame and update
	# the FPS counter
	rawCapture.truncate(0)
	fps.update()


	# check to see if the desired number of frames have been reached
	if i == (num_frames_to_test-1):
		break

# stop the timer and display FPS information
fps.stop()
stream.close()
rawCapture.close()
camera.close()



print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
print("{} Distinct QR/BarCodes Found".format(len(uniq_found_keep)))
for code in uniq_found_keep:
    print("code", code.data.decode("utf-8"))
for code in uniq_found_keep:
    print("\n", code)


# check to see if should wait while results displayed on screen
if show > 0:
    key = cv2.waitKey(0)

# do a bit of cleanup
cv2.destroyAllWindows()


