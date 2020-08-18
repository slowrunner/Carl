#!/usr/bin/env python3

# Approach Dock 

# USAGE
# ./apprDock.py
# ./apprDock.py --display 1

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

# Carl's libraries
import sys
sys.path.append("/home/pi/Carl/plib")
import camUtils

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())
show = args["display"]

num_frames_to_test = 10

test_frame = None
processed_frame = None
annotated_frame = None
circles_found_keep = []

# OpenCV Processing
def processImage(image, show):
    global test_frame, processed_frame, annotated_frame, circles_found

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (3, 3), 0)
    # thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)
    # dilated = cv2.dilate(thresh, None, iterations=2)
    test_frame = image.copy()
    processed_frame = gray.copy()
    annotated_frame = image.copy()

    # circles = cv2.HoughCircles(processed_frame, cv2.HOUGH_GRADIENT, 1.2, MIN_DIST, param1=30, param2=35, minRadius=MIN_RADIUS, maxRadius=MAX_RADIUS)
    circles = cv2.HoughCircles(processed_frame, cv2.HOUGH_GRADIENT, 1.2, 5)
    # print("circles:", circles)
    if circles is not None:
        # convert the (x, y) coords and radius to ints
        # print("len(circles):", len(circles))
        circles_this_frame = np.round(circles[0]).astype("int")

        # print("circles_this_frame:", circles_this_frame)
        circles_found.append(circles_this_frame)
        if show > 0:
            for (x,y,r) in circles_this_frame:
                cv2.circle(annotated_frame, (x, y), r, (255, 0,0), 2)
                cv2.rectangle(annotated_frame, (x-2, y-2), (x+2, y+2), (255, 0, 0), -1)

        circles_found = circles_found[0]

        print("{} circles:".format( len(circles_found), circles_found))

        circle_cntr = 0
        for c in circles_found:
            circle_cntr += 1
            print("circle {} ctr: ({},{}) radius: {}".format(circle_cntr, c[0], c[1], c[2]))

    if show > 0:
        cv2.imshow("frame", image)
        cv2.imshow("processed_frame", processed_frame)
        if len(circles_found) > 0: cv2.imshow("annotated", annotated_frame)
        cv2.waitKey(1) & 0xFF

# initialize the camera and stream
camera = PiCamera()
camera.resolution = (320, 240)
# camera.resolution = (640, 480)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(320, 240))
# rawCapture = PiRGBArray(camera, size=(640, 480))
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

	circles_found = []
	# Perform processing to see effect on fps
	processImage(test_image, show)

	# clear the stream in preparation for the next frame and update
	# the FPS counter
	rawCapture.truncate(0)
	fps.update()

	if len(circles_found) > 0: 
		circles_found_keep = circles_found
	# check to see if the desired number of frames have been reached
	if i == num_frames_to_test:
		break

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

if (len(circles_found_keep) > 0) and show:
    cv2.waitKey(0)

# do a bit of cleanup
cv2.destroyAllWindows()
stream.close()
rawCapture.close()
camera.close()



