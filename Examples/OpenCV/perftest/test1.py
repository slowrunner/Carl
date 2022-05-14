#!/usr/bin/env python3

"""
@file test1.py
@brief This program is used to compare OpenCV performance
"""

import sys
import math
import cv2 as cv
import numpy as np
# pip3 install linetimer
from linetimer import CodeTimer
from datetime import datetime

def display(windowname, image, scale_percent=30):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    imagesmall = cv.resize(image, dim, interpolation = cv.INTER_AREA)
    cv.imshow(windowname, imagesmall)

def testfunc(src):
    # Find edges in image
    # - image (8-bit)
    # - threshold1 for hysteresis procedure
    # - threshold2 for hysteresis procedure
    # - aperatureSize for Sobel operator
    # - L2gradiant flag (False: Normal,  True:more accurate)
    dst = cv.Canny(src, 50, 200, None, 3)

    # Convert canny result to grayscale
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)

    # Get lines on the canny image using Probabilistic Hough Transform
    # - Input Array
    # - Output Array of lines
    # - rho: Distance resolution of the accumulator in pixels
    # - theta:  Angle resolution of the accumulator in radians
    # - threshold: Only return lines with enough votes
    # - minLineLength=0
    # - maxLineGap=0

    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            # print("Line[{}]: [{}, {}], [{}, {}]".format(i, l[0], l[1], l[2], l[3]))
            # Draw lines on canny image
            # cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv.LINE_AA)
            cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv.LINE_AA)
"""
    try:
        # cv.imshow("Source", src)
        display("Source", src, 30)
        # cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
        # display("Detected Lines (in red) - Standard Hough Line Transform", cdst, scale_percent=30)
        # cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
        display("Detected Lines (red) - Probabilistic Line Transform", cdst, scale_percent=30)

        cv.waitKey()
    except Exception as e:
        print("Exception: {}".format(str(e)))
    return 0
"""



def main(argv):

    default_file = 'image1.jpg'
    filename = argv[0] if len(argv) > 0 else default_file
    # Loads an image
    try:
        src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)
    except:
        print ('Error opening image!')
        print ('Usage: test1.py [image_name -- default ' + default_file + '] \n')
        return -1

    with CodeTimer('houghlines image1'):
        testfunc(src)

    repeats = 10
    start = datetime.now()
    for i in range(repeats):
        testfunc(src)
    end = datetime.now()
    time_taken = (end - start)/repeats
    print('Average execution time from {} runs:'.format(repeats), time_taken)
    print('Approximately {:.1f} FPS'.format(1.0/time_taken.total_seconds()))
if __name__ == "__main__":
    main(sys.argv[1:])
