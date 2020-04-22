#!/usr/bin/env python3

# quiz
import numpy as np
import argparse
import cv2


def display(windowname, image, scale_percent=40):
    print('Original Dimensinos : ', image.shape)

    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    imagesmall = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    print('Resized Dimensions : ',imagesmall.shape)
    cv2.imshow(windowname, imagesmall)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
    help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = cv2.GaussianBlur(image, (5, 5), 0)
# cv2.imshow("Original", image)
display("Blurred",image)

canny1 = cv2.Canny(image, 200, 250)
display("Canny1", canny1)
canny2 = cv2.Canny(image, 240, 250)
display("Canny2", canny2)
canny3 = cv2.Canny(image, 10, 200)
display("Canny3", canny3)

cv2.waitKey(0)


"""
sobelX = cv2.Sobel(image, cv2.CV_64F, 1, 0)
sobelY = cv2.Sobel(image, cv2.CV_64F, 0, 1)

sobelX = np.uint8(np.absolute(sobelX))
sobelY = np.uint8(np.absolute(sobelY))

sobelCombined = cv2.bitwise_or(sobelX, sobelY)
# cv2.imshow("Sobel X", sobelX)
# cv2.imshow("Sobel Y", sobelY)
# cv2.imshow("Sobel Combined", sobelCombinedSmall)
#display("Sobel X", sobelX)
#display("Sobel Y", sobelY)
display("Sobel Combined", sobelCombined, 30)
cv2.waitKey(0)
"""
