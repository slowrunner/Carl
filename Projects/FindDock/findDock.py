#!/usr/bin/env python3
#
# findDock.py

"""
Documentation:
   Uses OpenCV on successive images captured by the PyCam to find the recharging dock.
   Algorithm:
   1) Capture an image
   2) Mask for green LED(s) of the dock
   3) Find number and position in the image of green LED(s)
   4) If no LEDs and number of captures < "360 degrees of captures"
          turn capture width and continue from step 1
      else declare "dock not visible (at this location)"
   5) Calculate dock angle relative to heading angle using horiz LED position in image
   6) Estimate dock distance based on vertical LED position in image
   7) Point distance sensor toward dock, take distance reading
   8) Fuse estimate and reading for distance to dock
   9) Point distance sensor fwd and 10" away (for U turn clearance plus 1")
   10) If distance to dock GE 30" turn to face dock, otherwise turn away from dock
   11) While distance sensor reading > 9" (U turn clearance), drive to point 30" from dock
   12) If drove away from dock, turn to face dock
   13) Perform wall_scan() returns distance to wall, angle to wall normal
   14) Calculate turn angle to intersect wall normal from dock at 90 degrees
   15) Calculate distance from current position to dock-ctr-wall-normal
   16) Turn to intersect wall-normal-from-dock at 90 degrees
   17) While distance sensor reading > 9", drive to dock-wall-normal
   18) Turn to face dock

  Followed by approach_dock(), and then dock()

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
    import camUtils
    Carl = True
except:
    Carl = False
import easygopigo3 # import the EasyGoPiGo3 class
import numpy as np
import datetime as dt
import argparse
from time import sleep

import cv2
import imutils

# ARGUMENT PARSER
# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--file", required=True, help="path to input file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
# ap.add_argument("-l", "--loop", default=False, action='store_true', help="optional loop mode")
# args = vars(ap.parse_args())
# print("Started with args:",args)
# filename = args['file']
# loopFlag = args['loop']

# CONSTANTS
FOV_H_ANGLE    = 55.5
FOV_V_ANGLE    = 41.0
POV_H_ANGLE    = 0.0
POV_ANGLE      = 1.84 # deg up   (325mm above floor at 2794mm)
POV_ELEVATION  = 235  # mm (9.25 inches) above floor
POV_TILT       = 2.0 # deg
OVERLAP_H_ANGLE = 0.0 # deg overlap of successive images
HSVmin   = (29, 150, 100)  # green LEDs in HSV colorspace
HSVmax   = (99, 255, 255)

# VARIABLES


# METHODS

def topMask(image):
    # LEDs will not be in upper portion of image
    mask = np.zeros(image.shape[:2], dtype = "uint8")
    notMaskV = image.shape[0] // 2
    cv2.rectangle(mask, (0,notMaskV), (image.shape[1], image.shape[0]), 255, -1)
    cv2.imshow("top mask", mask)
    maskedImage = cv2.bitwise_and(image, image, mask = mask)
    cv2.imshow("top masked image",maskedImage)
    return maskedImage

def hsvGreenMask(image):
    # use HSV filter to mask out everything but green LEDs

    # usefult to blur the image first
    blurred = cv2.GaussianBlur(image, (3,3), 0)
    cv2.imshow("Blurred 3,3",blurred)
    # convert image to hsv color space
    hsvImage = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsvMasked = cv2.inRange(hsvImage, HSVmin, HSVmax)
    cv2.imshow("Masked View", hsvMasked)

    return hsvMasked

def circleErodeDilate(mask):
    # generate a circular kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
    # erode to clean 
    eroded = cv2.erode(mask, kernel, iterations=2)
    cv2.imshow("eroded mask",eroded)
    # dilate to circle
    dilated = cv2.dilate(eroded, kernel, iterations=2)
    cv2.imshow("dilated mask",dilated)
    return dilated

def findLEDs(masked):
    # find contours in the mask
    cnts = cv2.findContours(masked.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(cnts)
    print("Probable {} LEDs:".format(len(contours), contours))
    return contours

def findDock(egpg, verbose = True):
    foundDock = False
    angleSearched = 0
    greenLEDs = []
    currentHeading = 0
    while ( (not foundDock) and (angleSearched < 360)):
        if verbose:
            strToLog = "Capturing Image"
            runLog.logger.info(strToLog)
            speak.say(strToLog)

        # can use to fine tune FOV_H_ANGLE with OVERLAP_H_ANGLE=0 (turn_deg() accuracy)
        fname = camUtils.snapJPG()

        image = camUtils.captureOCV()
        cv2.imshow("View at heading: {:.0f} deg".format(currentHeading),image)

        # mask off the top of image - no LEDs up there
        topMasked = topMask(image)

        # mask anything not LED green
        hsvGreenMasked = hsvGreenMask(topMasked)

        # circleProcessed = circleErodeDilate(hsvGreenMasked)
        # greenLEDs = findLEDs(circleProcessed)

        greenLEDs = findLEDs(hsvGreenMasked)


        cv2.waitKey(0)
        cv2.destroyAllWindows()

        if angleSearched == 0:
            angleSearched += FOV_H_ANGLE
        else:
            angleSearched += (FOV_H_ANGLE - OVERLAP_H_ANGLE)

        if ( len(greenLEDs) > 0 ):
            foundDock = True
            if verbose:
                strToLog = "Found LEDs"
                runLog.logger.info(strToLog)
                speak.say(strToLog)
            print("LED Contours:",greenLEDs)
        elif (angleSearched < 360):
            angleToTurn = (FOV_H_ANGLE-OVERLAP_H_ANGLE)
            if verbose:
                strToLog = "Turning {:.0f} degrees to heading {:.0f}".format(angleToTurn,(currentHeading+angleToTurn) )
                runLog.logger.info(strToLog)
                speak.say(strToLog)
            egpg.turn_degrees(angleToTurn)
            currentHeading = currentHeading + angleToTurn
    if foundDock:
        if (len(greenLEDs) > 1):
            print("Need to analyse found items")
            #  pixelHV = np.average(greenLEDs)
            # horizAngleToDock = horizAngleToObjInFOV(pixelHV)
    else:
        angleToTurn = 360 - currentHeading
        if verbose:
            strToLog = "Not Found. Turning {:.0f} degrees to heading {:.0f}".format(angleToTurn,(currentHeading+angleToTurn) )
            runLog.logger.info(strToLog)
            speak.say(strToLog)
        egpg.turn_degrees(angleToTurn)
    if verbose:
        strToLog = "find Dock returning {}".format(foundDock)
        runLog.logger.info(strToLog)
        speak.say(strToLog)

    return foundDock

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
        tiltpan.tiltpan_center()
        sleep(0.5)
        tiltpan.off()

    try:
        dtNow = dt.datetime.now()
        timeStrNow = dtNow.strftime("%H:%M:%S")[:8]
        strToLog ="Starting findDock() at {}".format(timeStrNow)
        print(strToLog)
        # runLog.logger.info(strToLog)
        # speak.say(strToLog)

        foundDock = findDock(egpg)

        dtNow = dt.datetime.now()
        timeStrNow = dtNow.strftime("%H:%M:%S")[:8]
        if foundDock:
           print("findDock() reports success at {}".format(timeStrNow))
        else:
           print("findDock() reports failure at {}".format(timeStrNow))


    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
