#!/usr/bin/env python3

# RASPBERRY PI CAMERA CALIBRATION FOR ARUCO MARKER DETECTION
# REF: https://youtu.be/XFBKwme5HYk

# BOARD GENERATOR
# REF: https://calib.io/pages/camera-calibration-pattern-generator


import numpy as np
import cv2
import glob
import time

cb_width = 10  # squares in checkerboard width
cb_height = 8  # squares in checkerboard height
cb_square_size = 24.3  # mm

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
cb_3D_points = np.zeros(((cb_width-1) * (cb_height-1), 3), np.float32)
cb_3D_points[:,:2] = np.mgrid[0:cb_width-1, 0:cb_height-1].T.reshape(-1,2) * cb_square_size

# Arrays to store object points and image points from all the images
list_cb_3d_points = [] # 3D point in real world space
list_cb_2d_img_points = [] # 2D points in image plane

list_images = glob.glob('*.jpg')

for frame_name in list_images:
    img = cv2.imread(frame_name)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (cb_width-1,cb_height-1),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        list_cb_3d_points.append(cb_3D_points)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        list_cb_2d_img_points.append(corners2)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, (cb_width-1, cb_height-1), corners2,ret)
        cv2.imshow('img',img)
        cv2.waitKey(500)

cv2.destroyAllWindows()

print("Starting Camera Calibration - may take a while ..")
start_time = time.time()
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(list_cb_3d_points, list_cb_2d_img_points, gray.shape[::-1],None,None)
end_time = time.time()
print("Calibration completed in {:.0f} seconds".format(end_time - start_time))
print("\n")
print("Calibration Matrix: ")
print(mtx)
print("Distortion: ", dist)
print("\nCalibration rms: {}".format(ret))

with open('camera_cal.npy', 'wb') as f:
    np.save(f, mtx)
    np.save(f, dist)

print("Calibration/Distortion matrices written to camera_cal.npy")

print("Process Complete")
