#!/usr/bin/env python3
#
# watershed.py

"""
Documentation:

"""

# from __future__ import print_function # use python 3 syntax but make it compatible with python 2
# from __future__ import division       #                           ''

import sys
try:
    sys.path.append('/home/pi/Carl/plib')
    import speak
    import tiltpan
    import status
    import battery
    import myDistSensor
    import lifeLog
    import runLog
    import myconfig
    import myimutils   # display(windowname, image, scale_percent=30)
    Carl = True
except:
    Carl = False
import easygopigo3 # import the EasyGoPiGo3 class
import numpy as np
import datetime as dt
import argparse
from time import sleep
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import imutils
import cv2

# ARGUMENT PARSER
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to iaage file")
#ap.add_argument("-t", "--threshold", type=int, default=128, help="Threshold value")
# ap.add_argument("-l", "--loop", default=False, action='store_true', help="optional loop mode")
args = vars(ap.parse_args())
# print("Started with args:",args)
# filename = args['file']
# loopFlag = args['loop']

# CONSTANTS


# VARIABLES


# METHODS 



# MAIN

def main():
    if Carl: runLog.logger.info("Started")
    try:
        egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    except:
        strToLog = "Could not instantiate an EasyGoPiGo3"
        print(strToLog)
        if Carl: lifeLog.logger.info(strToLog)
        exit(1)
    if Carl:
        myconfig.setParameters(egpg)
        tp = tiltpan.TiltPan(egpg)
        tp.tiltpan_center()
        tp.off()

    try:
        # Do Somthing in a Loop
        loopSleep = 1 # second
        loopCount = 0
        keepLooping = False
        while keepLooping:
            loopCount += 1
            # do something
            sleep(loopSleep)

        # Do Something Once
        # load the image and convert to grayscale
        image = cv2.imread(args["image"])
        # pyramid mean shift to aid thresholding 
        shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)
        cv2.imshow("Input", image)

        # convert to grayscale, apply Otsu's thresholding
        gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
        # threshold() returns T,thresholded_image (T is the threshold value - same as 0 passed in)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        cv2.imshow("Thresh", thresh)

        # compute the exact Euclidean Distance (ED Transform) from every non-zero (foreground)
        # pixel to the nearest zero (background) pixel, then find peaks (center area of objects) in this
        # distance map
        D = ndimage.distance_transform_edt(thresh)
        localMax = peak_local_max(D, indices=False, min_distance=20, labels=thresh)

        # perform connected component analysis on the local peaks,
        # using 8-connectivity, then apply Watershed algorithm
        markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]

        # watershed assumes markers are local minima (valleys), use -D to turn peaks to valleys
        labels = watershed( -D, markers, mask=thresh)
        print("[INFO] {} unique segments found".format(len(np.unique(labels)) -1))
        # (each pixel has been "labeled" with a height, all pixels with same height belong to same object)

        # loop over the unique labels, gather those pixels on a maxk
        for label in np.unique(labels):
            # if label is zero (background pixels), ignore it
            if label == 0:
                continue

            # allocate memory for the label region and draw it on the mask
            mask = np.zeros(gray.shape, dtype="uint8")
            mask[labels == label] = 255  # unmask pixels of this region

            # detect contours in the mask and grab the largest one
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            c = max(cnts, key=cv2.contourArea)

            # draw a circle enclosing the object
            ((x, y), r) = cv2.minEnclosingCircle(c)
            cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
            cv2.putText(image, "#{}".format(label), (int(x) - 10, int(y)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # show the output image
        cv2.imshow("Output", image)
        cv2.waitKey(0)

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
