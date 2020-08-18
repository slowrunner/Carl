#!/usr/bin/env python3
#
# lanes.py

"""
Documentation:

    from https://www.youtube.com/watch?v=eLTLtUVuuy4
         "OpenCV Python Tutorial - Find Lanes for Self-Driving Cars"
         sample image and video from github.com/rslim087a

Purpose: lanes.py estimates and displays lane boundries in a single image or a video

Usage:
   ./lanes.py -f image.jpg
   ./lanes.py -f video.mp4
   ./lanes.py -f <file> -n   computes but does not display result on image/frames
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

import os
import cv2
import myimutils
import matplotlib.pyplot as plt

# ARGUMENT PARSER
#ap = argparse.ArgumentParser()
#ap.add_argument("-f", "--file", required=True, help="path to input file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
#ap.add_argument("-n", "--noshow", default=False, action='store_true', help="optional do not show video result")
#args = vars(ap.parse_args())
# print("Started with args:",args)
#inFilename = args['file']
#noshow = args['noshow']

# CONSTANTS


# VARIABLES


# METHODS

# grayBlurCanny(image)
#
# 1) create grayscale copy of image
# 2) blur the gray copy
# 3) apply Canny edge detect with 150:50 thresholds
# return edge mask

def grayBlurCanny(image):
        # use canny to find high gradient pixels
        # recommended ration 3:1
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        # low_threshold = 50
        low_threshold = 15
        # high_threshold = 150
        high_threshold = 45
        return cv2.Canny(gray, low_threshold, high_threshold)

# region_of_interest(image)
#
# masks image to triangular ROI
# triangle has apex 35% down from top mid-width, and
#              base at bottom of frame of the center 70% of frame width (15% off both sides)

def region_of_interest(image):
    # return a triangular region of interest
    # print("image.shape:",image.shape)
    height = image.shape[0]
    width  = image.shape[1]
    bottom_of_frame = height
    left_limit = int(0.15 * width)
    right_limit = int(0.85 * width)
    lane_ctr = int(width * 0.5)  # originally 550 or 43%, slightly off to left
    lane_horizon = int(height * 0.35) # originally 250 or 35% down from top
    triangle = np.array([(left_limit, bottom_of_frame), (right_limit, bottom_of_frame),(lane_ctr, lane_horizon)])
    polygons = np.array([ triangle ])  # only one polygon in the polygons array
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

# display_lines(image, lines)
#
# creates an overlay with blue lines drawn on black/zeros
#
def display_lines(image, lines):
    line_image = np.zeros_like(image)
    blue = (255, 0, 0)
    width = 10
    if lines is not None:
        for line in lines:
            if line is not []:
                x1, y1, x2, y2 = line.reshape(4)
                # draw the line on the black array that is the shape of image
                cv2.line(line_image, (x1, y1), (x2, y2), blue, width)
    return line_image

# make_coordinates(image, line_parameters)
#
# converts slope,intercept into line endpoints 
#   representing the line from bottom of frame up to bottom 40% of frame

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0] # make lines start at bottom of the image
    y2 = int(y1*(3/5))  # make lines extend up 3/5ths of the image
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])

# average_slope_intercept(image, lines)
#
# returns single left lane and single right lane line parameters (m,b)
#  by averaging all left lines and averaging all right lane lines parameters (m,b)

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    found = 0
    if lines is not None: 
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            # returns m,b for y=mx+b line fit to points
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            if  slope < -1:
                left_fit.append((slope, intercept))
            elif 1 < slope:
                right_fit.append((slope, intercept))
    try:
        if len(left_fit) > 0:
            left_fit_average = np.average(left_fit, axis=0)
            left_line = make_coordinates(image, left_fit_average)
            found +=1
        else:
            # print("no left_line found")
            left_line = [int(image.shape[1]*0.15), image.shape[0], int(image.shape[1]*0.15), int(image.shape[0]*3/5)]
        if len(right_fit) > 0:
            right_fit_average = np.average(right_fit, axis=0)
            right_line = make_coordinates(image, right_fit_average)
            found +=1
        else:
            # print("no right_line found")
            right_line = [int(image.shape[1]*0.85), image.shape[0], int(image.shape[1]*0.85), int(image.shape[0]*3/5)]
        print("Found {} lane_lines".format(found))
        return np.array([left_line, right_line])
    except Exception as e:
        print(e, '\n')
        #print error to console
        return None

# find_lane_in(image or frame from video)
#
# Process:
#  1) create a grayscale image copy
#  2) blur the grayscale image
#  3) apply Canny edge detect to blurred grayscale image 
#     return edge mask 
#  4) crop edge mask to triangular region of interest
#  5) use Hough transform (binned r,theta normal to len/gap qualifed lines) to find lines
#  6) average left and right lane lines down to one left of lane, one right of lane line
#  7) create lane lines overlay
#  8) combine lane lines overlay over original image
#  returns image with lane lines drawn in bottom 40%

def find_lane_in(image):
        # use canny to find high gradient pixels 
        canny_image = grayBlurCanny(image)

        # use matplot to display image with x,y so we can grab the x,y for corners of a 
        # triangular region of interest
        #plt.imshow(canny_image)
        #plt.show()

        cropped_canny = region_of_interest(canny_image)
        # bin size  2 pixels by 1 degree (1deg = pi/180 radians)
        # threshold is number of "votes" or r,theta of lines are in the same bin
        #    empirically determined by author as 100
        # place holder array

        # myimutils.display("cropped_canny",cropped_canny)
        # cv2.waitKey(0)
        myimutils.display("cropped_canny",cropped_canny)
        cv2.waitKey(0)

        # cv2.imwrite("grayBlurCannyROI.jpg", cropped_canny)
        # lines = cv2.HoughLinesP(cropped_canny, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5  )
        lines = cv2.HoughLinesP(cropped_canny, 3, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5  )
        averaged_lines = average_slope_intercept(image, lines)
        line_image = display_lines(image, averaged_lines)
        image_weight = 0.8
        line_weight = 1
        gamma = 1
        # lines will be 20% more intense than image (image intensity reduced to 80%)
        combo_image = cv2.addWeighted(image, image_weight, line_image, line_weight, gamma)
        # myimutils.display("result",region_of_interest(canny_image) )
        return combo_image

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
        # ARGUMENT PARSER
        ap = argparse.ArgumentParser()
        ap.add_argument("-f", "--file", required=True, help="path to input file")
        ap.add_argument("-n", "--noshow", default=False, action='store_true', help="optional do not show video result")
        args = vars(ap.parse_args())
        # print("Started with args:",args)
        inFilename = args['file']
        noshow = args['noshow']
        frames = 0
        times = []
        imageSize = None
        # split the passed in file path to get the file extension
        filename, file_ext = os.path.splitext(inFilename)

        # if single image passed in, run find_lanes_in(image) once
        if file_ext == '.jpg':
            image = cv2.imread(inFilename)
            imageSize = image.shape
            frames += 1
            dtStart = dt.datetime.now()
            combo_image = find_lane_in(image)
            dtEnd = dt.datetime.now()
            times += [(dtEnd-dtStart).total_seconds()]
            if combo_image.shape[0] < 800:
                cv2.imshow("result", combo_image)
            else:
                myimutils.display("result", combo_image)
            cv2.waitKey(0)

        # if video passed in, run find_lanes_in(each frame)
        elif file_ext == '.mp4':
            cap = cv2.VideoCapture(inFilename)
            while(cap.isOpened()):
                frames += 1
                dtStart = dt.datetime.now()
                _, frame = cap.read()
                if frames == 1:  imageSize = frame.shape
                combo_image = find_lane_in(frame)
                dtEnd = dt.datetime.now()
                times += [(dtEnd-dtStart).total_seconds()]
                if noshow == False:
                    cv2.imshow("result", combo_image )
                    if cv2.waitKey(1) == ord('q'):
                        break
        else:
            print("File extension not recognized")

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    finally:
            print("Frames: {} Ave find_lane_in(frame): {:.1f}ms".format(frames, 1000 * np.average(times)))
            print("Frame Size: ", imageSize)
    if (egpg != None): egpg.stop()
    if Carl: runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
