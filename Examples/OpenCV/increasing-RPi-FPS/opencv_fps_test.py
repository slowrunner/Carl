#!/usr/bin/env python3

# USAGE
# python picamera_fps_demo.py
# python picamera_fps_demo.py --display 1

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

TEMPLATE_FILENAME = "./dockSignTemplate.jpg"
# OpenCV MatchTemplate Settings
# -----------------------------
MAX_SEARCH_THRESHOLD = .96 # default=.97 Accuracy for best search result of search_rect in stream images
MATCH_METHOD = 3
            # Valid MatchTemplate COMPARE_METHOD Int Values
            # ---------------------------------------------
            # 0 = cv2.TM_SQDIFF  = 0
            # 1 = cv2.TM_SQDIFF_NORMED = 1
            # 2 = cv2.TM_CCORR = 2
            # 3 = cv2.TM_CCORR_NORMED = 3    Default
            # 4 = cv2.TM_CCOEFF = 4
            # 5 = cv2.TM_CCOEFF_NORMED = 5
            #
            # For other comparison methods 
            # see http://docs.opencv.org/3.1.0/d4/dc6/tutorial_py_template_matching.html



# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())
show = args["display"]

# read template file for template matching
template_image = cv2.imread(TEMPLATE_FILENAME)
template_image = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

#-----------------------------------------------------------------------------------------------
def check_image_match(full_image, small_image):
    # Look for small_image in full_image and return best and worst results
    # Try other MATCH_METHOD settings 
    # For More Info See http://docs.opencv.org/3.1.0/d4/dc6/tutorial_py_template_matching.html
    result = cv2.matchTemplate( full_image, small_image, MATCH_METHOD)
    # Process result to return probabilities and Location of best and worst image match
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)  # find search rect match in new image
    return maxLoc, maxVal




# OpenCV Processing
def processImage(image,show):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (21, 21), 0)
    # thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.AdaptiveThreshold(gray, 255, cv2.CV_ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)
    # dilated = cv2.dilate(thresh, None, iterations=2)

    # find template image in camera image
    # best_match_xy, best_match_confidence = check_image_match(dilated, template_image)
    # print("xy: {} conf: {}".format(best_match_xy,best_match_confidence))

    # grab contours
    # cnts = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print("contours:",cnts)

    # check to see if the frame should be displayed to our screen
    if show > 0:
       cv2.imshow("dilated", thresh)
       key = cv2.waitKey(1) & 0xFF



# initialize the camera and stream
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))
stream = camera.capture_continuous(rawCapture, format="bgr",
	use_video_port=True)

# allow the camera to warmup and start the FPS counter
print("[INFO] sampling frames from `picamera` module...")
time.sleep(2.0)
fps = FPS().start()

# loop over some frames
for (i, f) in enumerate(stream):
	# grab the frame from the stream and resize it to have a maximum
	# width of 400 pixels
	frame = f.array
	frame = imutils.resize(frame, width=400)

	# check to see if the frame should be displayed to our screen
	if show > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

	# Perform processing to see effect on fps
	processImage(frame, show)

	# clear the stream in preparation for the next frame and update
	# the FPS counter
	rawCapture.truncate(0)
	fps.update()

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
	frame = imutils.resize(frame, width=400)

	# Perform processing to see effect on fps
	processImage(frame, show)

	# check to see if the frame should be displayed to our screen
	if show > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

	# update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
