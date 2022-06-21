#!/usr/bin/env python3

# CODE AND PROCESS
# REF: https://www.youtube.com/watch?v=XFBKwme5HYk

# CHECKERBOARD GENERATOR
# REF: https://calib.io/pages/camera-calibration-pattern-generator


# check camera version:
# ov5647 for the V1 module, and imx219 for the V2
import picamera
import numpy as np
import cv2, time

with picamera.PiCamera() as cam:
    cam_revision = cam.revision
    if cam_revision == "ov5647":
      cam_version = "v1"
    elif cam_revision == "imx219":
      cam_version = "v2"
    else:
      cam_version = "unknown"

    print("PiCamera Revision:",cam_revision)
    print("PiCamera Version: ",cam_version)

FRAME_RATE = 40

cv2.namedWindow("Image Feed")
cv2.moveWindow("Image Feed", 159, -25)

cap = cv2.VideoCapture(0)

# setup camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 40)              # v1 up to 90 FPS, v2 up to 42 FPS for full sensor images

prev_frame_time = time.time()
frame_count = 0
cal_image_count = 0

while True:
    ret, frame = cap.read()       # get a frame
    new_frame_time = time.time()  # save current time when captured the frame

    # process frame
    frame_count += 1

    # Write one frame per second out as jpg cal_image_nnn.jpg
    if frame_count == FRAME_RATE:
        cv2.imwrite("cal_image_{:03d}".format(cal_image_count) + ".jpg", frame)
        cal_image_count += 1
        frame_count = 0

    # calculate FPS and display on frame
    fps = 1/(new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    cv2.putText(frame, "FPS " + str(int(fps)), (10, 40), cv2.FONT_HERSHEY_PLAIN, 3, (100, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow("Image Feed", frame)

    # --- use "q" to quit
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"): break



cap.release()
cv2.destroyAllWindows()


