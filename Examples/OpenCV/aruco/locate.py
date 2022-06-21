#!/usr/bin/env python3

# FILE:  locate.py

# PURPOSE:  Find x,y,theta of camera to ArUco marker

# REQUIRES:  OpenCV, camera calibration/distortion matrices, ArUco DICT_4X$ marker

# REF:  https://www.youtube.com/watch?v=cIVZRuVdv1o

import numpy as np
import cv2
import cv2.aruco as aruco
import math

# ------------
# --- ROTATIONS  https://www.learnopencv.com/rotation-matrix-to-euler-angles/
# ------------

# Checks if a matrix is a valid rotation matrix
def isRotationMatrix(R):
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped )
def rotationMatrixToEulerAngles(R):
    assert (isRotationMatrix(R))

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2,1], R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])



marker_size = 88  # mm - might be 87.75mm

with open('camera_cal.npy', 'rb') as f:
    camera_matrix     = np.load(f)
    camera_distortion = np.load(f)

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

cap = cv2.VideoCapture(0)

camera_width = 640
camera_height = 480
camera_frame_rate = 40

cap.set(2, camera_width)
cap.set(4, camera_height)
cap.set(5, camera_frame_rate)

while True:

    ret, frame = cap.read()    # grab a frame

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale

    # -- Find all the aruco markers in the image
    corners, ids, rejected = aruco.detectMarkers(gray_frame, aruco_dict, camera_matrix, camera_distortion)

    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners)  # draw a box around each detected marker

        # get pose of all single markers  tvec is x,y,z from camera to marker,  rvec is rotation about x,y,z of marker
        rvec_list_all, tvec_list_all, _objPoints = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)

        # print("*** tvec list ***\n",tvec_list_all)
        # print("*** rvec list ***\n",rvec_list_all)

        # print("*** tvec marker 0 ***\n",tvec_list_all[0][0])
        # print("*** rvec marker 0 ***\n",rvec_list_all[0][0])

        rvec = rvec_list_all[0][0]
        tvec = tvec_list_all[0][0]

        aruco.drawAxis(frame, camera_matrix, camera_distortion, rvec, tvec, marker_size)

        rvec_flipped = rvec * -1
        tvec_flipped = tvec * -1
        rotation_matrix, jacobian = cv2.Rodrigues(rvec_flipped)
        realworld_tvec  = np.dot(rotation_matrix, tvec_flipped)

        pitch, roll, yaw = rotationMatrixToEulerAngles(rotation_matrix)

        tvec_str = "x=%4.0f y=%4.0f z=%4.0f direction=%4.0f"%(realworld_tvec[0], realworld_tvec[1], realworld_tvec[2], math.degrees(roll)  )
        cv2.putText(frame, tvec_str, (20,460), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1, cv2.LINE_AA)


    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break

cap.release()
cv2.destroyAllWindows()


