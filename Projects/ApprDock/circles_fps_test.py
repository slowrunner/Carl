#!/usr/bin/env python3

# OPENCV CIRCLES TEST

# USAGE
# ./circles_test.py
# ./circles_test.py --display 1

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


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())
show = args["display"]

MIN_RADIUS = 14 # 7
MIN_DIST = MIN_RADIUS * 2
MAX_RADIUS = 36 # 18

test_frame = None
processed_frame = None
annotated_frame = None
contours_found = []
circles_found = []
circles_found_keep = circles_found

# OpenCV Processing
def processImage(image, processed_frame, annotated_frame, contours_found, circles_found, show):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (3, 3), 0)
    # thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)
    # dilated = cv2.dilate(thresh, None, iterations=2)
    processed_frame = gray.copy()
    annotated_frame = image.copy()
    # circles = cv2.HoughCircles(processed_frame, cv2.HOUGH_GRADIENT, 1.2, MIN_DIST, param1=30, param2=35, minRadius=MIN_RADIUS, maxRadius=MAX_RADIUS)
    circles = cv2.HoughCircles(processed_frame, cv2.HOUGH_GRADIENT, 1.2, MIN_DIST,  minRadius=MIN_RADIUS, maxRadius=MAX_RADIUS)
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
    """
    # grab contours
    cnts = cv2.findContours(processed_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_found = imutils.grab_contours(cnts)
    circles_this_frame = []
    for c in contours_found:
         (x,y), radius = cv2.minEnclosingCircle(c)
        ctr = ( int(x), int(y) )
        radius = int(radius)
        circles_this_frame += [(ctr,radius)]
        image = cv2.circle(image, ctr, radius, (255, 0, 0), 2)
        circles_found += [circles_this_frame]
    """

    if show > 0:
        cv2.imshow("frame", image)
        cv2.imshow("processed_frame", processed_frame)
        if len(circles_found) > 0: cv2.imshow("annotated", annotated_frame)
        cv2.waitKey(1) & 0xFF

# initialize the camera and stream
camera = PiCamera()
# camera.resolution = (320, 240)
camera.resolution = (640, 480)
camera.framerate = 32
# rawCapture = PiRGBArray(camera, size=(320, 240))
rawCapture = PiRGBArray(camera, size=(640, 480))
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
	processImage(test_image, processed_frame, annotated_frame, contours_found, circles_found, show)

	# clear the stream in preparation for the next frame and update
	# the FPS counter
	rawCapture.truncate(0)
	fps.update()

	if len(circles_found) > 0: circles_found_keep = circles_found

	# check to see if the desired number of frames have been reached
	if i == args["num_frames"]:
		break

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


# do a bit of cleanup
cv2.destroyAllWindows()
stream.close()
rawCapture.close()
camera.close()

# created a *threaded *video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from `picamera` module...")
vs = PiVideoStream().start()
time.sleep(2.0)
fps = FPS().start()

# loop over some frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	# frame = imutils.resize(frame, width=400)
	test_image = frame
	circles_found = []
	# Perform processing to see effect on fps
	processImage(test_image, processed_frame, annotated_frame, contours_found, circles_found, show)

	# update the FPS counter
	fps.update()

	if len(circles_found) > 0:
		circles_found_keep = circles_found
		# print("{} circles found".format(len(circles_found_keep)))

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
vs.stop()


if len(circles_found_keep) > 0:
    circles_found_keep = circles_found_keep[0]
    print("{} circles:".format( len(circles_found_keep), circles_found_keep))

    circle_cntr = 0
    for c in circles_found_keep:
        circle_cntr += 1
        print("circle {} ctr: ({},{}) radius: {}".format(circle_cntr, c[0], c[1], c[2]))

# check to see if the results should be displayed to our screen
if show > 0:
    # cv2.imshow("test_image", test_image)
    # cv2.imshow("processed", processed_frame)
    # cv2.imshow("annotated", annotated_frame)
    key = cv2.waitKey(0)


# do a bit of cleanup
cv2.destroyAllWindows()


