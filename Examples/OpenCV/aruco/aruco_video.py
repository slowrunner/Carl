#!/usr/bin/env python3


# REF: https://pyimagesearch.com/2020/12/21/detecting-aruco-markers-with-opencv-and-python/
# Modified to print marker found value and location to console
# Modified to pass Gray image to opencv for ArUco detection
#          and use the color frame for output
#
# usage:
#  aruco_video.py  --type DICT_4X4_100

from imutils.video import VideoStream
import argparse
import imutils
import cv2
import sys
import time
# from picamera2 import Picamera2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str,
	default="DICT_ARUCO_ORIGINAL",
	help="type of ArUCo tag to detect")
args = vars(ap.parse_args())


# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

# verify that the supplied ArUCo tag exists and is supported by
# OpenCV
if ARUCO_DICT.get(args["type"], None) is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(
		args["type"]))
	sys.exit(0)

# load the ArUCo dictionary, grab the ArUCo parameters, and detect
# the markers
print("[INFO] detecting '{}' tags...".format(args["type"]))
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters_create()

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()

# vs = VideoStream(usePiCamera=True).start()
# cv2.startWindowThread()

# picam2 = Picamera2()
# picam2.configure(picam2.preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
# picam2.start()


time.sleep(2.0)


# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 1000 pixels
	colorframe = vs.read()
	# colorframe = picam2.capture_array()
	frame = cv2.cvtColor(colorframe, cv2.COLOR_BGR2GRAY)
	# frame = imutils.resize(frame, width=1000)
	# frame = imutils.resize(frame, width=1000)
	# detect ArUco markers in the input frame
	(corners, ids, rejected) = cv2.aruco.detectMarkers(frame,
		arucoDict, parameters=arucoParams)

	# verify *at least* one ArUco marker was detected
	if len(corners) > 0:
		# flatten the ArUco IDs list
		ids = ids.flatten()
		# loop over the detected ArUCo corners
		for (markerCorner, markerID) in zip(corners, ids):
			# extract the marker corners (which are always returned in
			# top-left, top-right, bottom-right, and bottom-left order)
			corners = markerCorner.reshape((4, 2))
			(topLeft, topRight, bottomRight, bottomLeft) = corners

			# convert each of the (x, y)-coordinate pairs to integers
			topRight = (int(topRight[0]), int(topRight[1]))
			bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
			bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
			topLeft = (int(topLeft[0]), int(topLeft[1]))

			# draw the bounding box of the ArUCo detection
			cv2.line(colorframe, topLeft, topRight, (0, 255, 0), 2)
			cv2.line(colorframe, topRight, bottomRight, (0, 255, 0), 2)
			cv2.line(colorframe, bottomRight, bottomLeft, (0, 255, 0), 2)
			cv2.line(colorframe, bottomLeft, topLeft, (0, 255, 0), 2)
			# compute and draw the center (x, y)-coordinates of the
			# ArUco marker
			cX = int((topLeft[0] + bottomRight[0]) / 2.0)
			cY = int((topLeft[1] + bottomRight[1]) / 2.0)
			cv2.circle(colorframe, (cX, cY), 4, (0, 0, 255), -1)
			# draw the ArUco marker ID on the frame
			cv2.putText(colorframe, str(markerID),
				(topLeft[0], topLeft[1] - 15),
				cv2.FONT_HERSHEY_SIMPLEX,
				0.5, (255, 0, 0), 2)

			print("Marker: {} at [{}, {}]".format(str(markerID), cX, cY))

	# show the output frame
	cv2.imshow("Frame", colorframe)
	key = cv2.waitKey(1) & 0xFF
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()


