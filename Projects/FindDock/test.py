#!/usr/bin/env python3

import numpy as np
import argparse
import cv2

def display(windowname, image, scale_percent=30):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    imagesmall = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow(windowname, imagesmall)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
original = image
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert to grayscale
grayed = image
image = cv2.GaussianBlur(image, (5, 5), 0)       # blur to reduce noisy pixels
blurred = image
canny = cv2.Canny(image, 30, 150)                # edge detection using Canny method

# cv2.imshow("Original", image)
display("Original",original)
display("Blurred", blurred)
display("Canny", canny)
cv2.waitKey(0)

sobelX = cv2.Sobel(image, cv2.CV_64F, 1, 0)
sobelY = cv2.Sobel(image, cv2.CV_64F, 0, 1)
sobelX = np.uint8(np.absolute(sobelX))
sobelY = np.uint8(np.absolute(sobelY))
sobelCombined = cv2.bitwise_or(sobelX, sobelY)

display("SobelXY", sobelCombined)
cv2.waitKey(0)

