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
    import servoscan
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
ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--file", required=True, help="path to input file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
ap.add_argument("-v", "--view", default=False, action='store_true', help="optional view images")
ap.add_argument("-t", "--talk", default=False, action='store_true', help="optional with TTS")
args = vars(ap.parse_args())
# print("Started with args:",args)
# filename = args['file']
viewFlag = args['view']
verbose  = args['talk']

# CONSTANTS
FOV_H_ANGLE    = 55.5  # empirical
FOV_V_ANGLE    = 41.0
POV_H_ANGLE    = 0.0
POV_ANGLE      = 1.84 # deg up   (325mm above floor at 2794mm)
POV_ELEVATION  = 235  # mm (9.25 inches) above floor
POV_TILT       = 2.0 # deg
OVERLAP_H_ANGLE = 3.1 # deg overlap of successive images to make 360 in 7 images 
HSVmin   = (29, 190, 100)  # green LEDs in HSV colorspace
HSVmax   = (99, 255, 255)
MAX_LED_RADIUS = 5
MAX_H_LED_SEPARATION = 20
MAX_V_LED_SEPARATION = 4
CAPTURE_HRES = 640
CAPTURE_VRES = 480
CTR_PIXEL_H_OFFSET = 64    # The image ctr is offset 64 pixels to left of robot ctr
STAGING_DISTANCE_INCHES = 30
DISTANCE_SENSOR_MAX_INCHES = 90
TOP_MASK_V_PERCENT = 0.625   # pixel 300 of 480 is highest Y (smallest value) of LEDs in image

# VARIABLES


# METHODS

def topMask(image):
    # LEDs will not be in upper portion of image, so mask out small Y values
    mask = np.zeros(image.shape[:2], dtype = "uint8")  # build mask the size of image

    # compute highest Y (smallest value) valid LEDs can appear in an image
    notMaskV = int(TOP_MASK_V_PERCENT * image.shape[0]) # 300 of 480, was 240 ( image.shape[0] // 2)

    # create a notMasked area from notMaskV to bottom of image
    cv2.rectangle(mask, (0,notMaskV), (image.shape[1], image.shape[0]), 255, -1)

    # apply the mask to the captured image (leaving only the lower portion of the image)
    maskedImage = cv2.bitwise_and(image, image, mask = mask)
    # cv2.imshow("top masked image",maskedImage)
    return maskedImage

def hsvGreenMask(image):
    # use HSV filter to mask out everything but green LEDs

    # usefult to blur the image first
    blurred = cv2.GaussianBlur(image, (3,3), 0)

    # convert image to hsv color space
    hsvImage = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsvMasked = cv2.inRange(hsvImage, HSVmin, HSVmax)
    # cv2.imshow("Masked View", hsvMasked)

    return hsvMasked

def circleDilate(mask):
    # generate a circular kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    # dilate to circle
    dilated = cv2.dilate(mask, kernel, iterations=2)
    if viewFlag: cv2.imshow("dilated mask",dilated)
    return dilated

def findLEDs(masked):

    ledsFound = []
    # find contours in the mask
    cnts = cv2.findContours(masked.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(cnts)
    print("Probable {} LEDs".format(len(contours)))
    if ( 2 >= len(contours) > 0 ):
      # find center and radius of each contour
      # if either radius is too big, throw out set
      for c in contours:
          (x,y),radius = cv2.minEnclosingCircle(c)
          ctr = ( int(x), int(y) )
          radius = int(radius)
          if (radius <= MAX_LED_RADIUS):
              ledsFound += [(ctr,radius,c)]
          else:
             # disqualify whole set if radius is too big
             print("Throwing out set, radius {} too big.".format(radius))
             ledsFound = []
             break
      # if two possible LEDS, check horizontal distance between them < MAX_LED_SEPARATION
      if (len(ledsFound) == 2):
          separation = abs(ledsFound[1][0][0] - ledsFound[0][0][0])
          if separation > MAX_H_LED_SEPARATION:
              print("Throwing out set, separation {} greater than MAX_H_LED_SEPARATION".format(separation) )
              ledsFound = []
      # if two possible LEDS, check vertical distance between them < MAX_H_LED_SEPARATION
      if (len(ledsFound) == 2):
          separation = abs(ledsFound[1][0][1] - ledsFound[0][0][1])
          if separation > MAX_V_LED_SEPARATION:
              print("Throwing out set, vertical separation {} greater than MAX_V_LED_SEPARATION".format(separation) )
              ledsFound = []
    elif (len(contours) > 2):
        print("Too many hits.  Ignoring")
    return ledsFound

def findDock(egpg):
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
        # fname = camUtils.snapJPG()

        image1 = camUtils.captureOCV()
        image = camUtils.fixTiltOCV(image1)
        if viewFlag: cv2.imshow("Corrected View at heading: {:.0f} deg".format(currentHeading),image)

        # mask off the top of image - no LEDs up there
        topMasked = topMask(image)

        # mask anything not LED green
        hsvGreenMasked = hsvGreenMask(topMasked)

        circleProcessed = circleDilate(hsvGreenMasked)
        greenLEDs = findLEDs(circleProcessed)


        if angleSearched == 0:
            angleSearched += FOV_H_ANGLE
        else:
            angleSearched += (FOV_H_ANGLE - OVERLAP_H_ANGLE)

        if ( 2 >= len(greenLEDs) > 0 ):
            foundDock = True
            if verbose:
                strToLog = "Found LEDs"
                runLog.logger.info(strToLog)
                speak.say(strToLog)
            for led in greenLEDs:
                if verbose:
                    print("LED ( Center(x,y),radius,contour):",led)
                else:
                    print("LED Center(x,y)",led[0]," radius:",led[1])
        elif (angleSearched < 360):
            angleToTurn = (FOV_H_ANGLE-OVERLAP_H_ANGLE)
            strToLog = "Turning {:.0f} degrees to heading {:.0f}".format(angleToTurn,(currentHeading+angleToTurn) )
            if verbose:
                runLog.logger.info(strToLog)
                speak.say(strToLog)
            print(strToLog)
            egpg.turn_degrees(angleToTurn)
            currentHeading = currentHeading + angleToTurn
    if foundDock:
        if (len(greenLEDs) > 1):
            dockPixel = (greenLEDs[0][0][0] + greenLEDs[1][0][0]) // 2
        else:  dockPixel = greenLEDs[0][0][0]
        # dockPixel = min((dockPixel + CTR_PIXEL_H_OFFSET),CAPTURE_HRES)  # correct for image horizontal offset from bot ctr
        dockPixel = dockPixel + CTR_PIXEL_H_OFFSET   # correct for image horizontal offset from bot ctr
        horizAngleToDock = camUtils.hAngle(dockPixel,CAPTURE_HRES,FOV_H_ANGLE)
        if verbose:
            strToLog = "Turning {:.0f} degrees to face probable dock".format(horizAngleToDock)
            runLog.logger.info(strToLog)
            speak.say(strToLog)
        egpg.turn_degrees(horizAngleToDock)
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
    if viewFlag:
        if verbose: speak.say("Waiting for key press to continue")
        cv2.waitKey(0)
    return foundDock

# MAIN

def main():
    if Carl: runLog.logger.info("Started")
    try:
        egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
        ds = myDistSensor.init(egpg)
        tp = tiltpan.TiltPan(egpg)
    except:
        strToLog = "Could not instantiate an EasyGoPiGo3"
        print(strToLog)
        if Carl: lifeLog.logger.info(strToLog)
        exit(1)
    if Carl:
        myconfig.setParameters(egpg)
        tp.tiltpan_center()
        sleep(0.5)
        tp.off()

    try:
        dtNow = dt.datetime.now()
        timeStrNow = dtNow.strftime("%H:%M:%S")[:8]
        strToLog ="Starting findDock() at {}".format(timeStrNow)
        print(strToLog)
        runLog.logger.info(strToLog)
        if verbose: speak.say(strToLog)

        foundDock = findDock(egpg)

        dtNow = dt.datetime.now()
        timeStrNow = dtNow.strftime("%H:%M:%S")[:8]
        if foundDock:
           print("findDock() reports success at {}".format(timeStrNow))
           # cv2.waitKey(0)
           distReading = myDistSensor.adjustReadingInMMForError(ds.read_mm()) / 25.4
           if distReading > STAGING_DISTANCE_INCHES:
              print  ("Distance Sensor: %0.1f inches" %  distReading)
              if distReading > DISTANCE_SENSOR_MAX_INCHES:
                  print("Distance greater than sensor maximum, requires two drives")
                  need_two_drives = True
                  dist_to_drive = (DISTANCE_SENSOR_MAX_INCHES - STAGING_DISTANCE_INCHES) * 0.75
              else:
                  need_two_drives = False
                  dist_to_drive = distReading - STAGING_DISTANCE_INCHES
              print("Pending Action: FORWARD {:.1f} inches".format(dist_to_drive))
              sleep(5)
              egpg.drive_inches(dist_to_drive)  # blocking
              sleep(1)
              if need_two_drives:
                  distReading = myDistSensor.adjustReadingInMMForError(ds.read_mm()) / 25.4
                  if (DISTANCE_SENSOR_MAX_INCHES > distReading > STAGING_DISTANCE_INCHES):
                      print  ("Distance Sensor: %0.1f inches" %  distReading)
                      dist_to_drive = distReading - STAGING_DISTANCE_INCHES
                      print("Pending Action: FORWARD {:.1f} inches".format(dist_to_drive))
                      sleep(5)
                      egpg.drive_inches(dist_to_drive)  # blocking
              strToLog = "Facing Dock at staging distance"
              print(strToLog)
              if verbose:
                  speak.say(strToLog)
                  runLog.logger.info(strToLog)
           else:
              print("Distance Sensor: %0.1f inches" % distReading)
              dist_to_drive = STAGING_DISTANCE_INCHES - distReading
              print("Pending Action: TURN 180, DRIVE {:.1f} inches".format(dist_to_drive))
              sleep(5)
              egpg.turn_degrees(180)
              sleep(1)
              egpg.drive_inches(dist_to_drive)  # blocking
              sleep(1)
              egpg.turn_degrees(180)
              strToLog = "Facing Dock at staging distance"
              print(strToLog)
              if verbose:
                  speak.say(strToLog)
                  runLog.logger.info(strToLog)
           # update dist to dock wall at heading
           distToDockWall = myDistSensor.adjustReadingInMMForError(ds.read_mm()) / 25.4
           print("Distance To Dock Wall: %0.1f inches" % distToDockWall)
           # find heading angle from wall
           angleToDockWall = servoscan.wallAngleScan(ds,tp,sector=45,verbose=True)
           if np.isnan(angleToDockWall) == False:
               if angleToDockWall > 0:
                   turnAngle =  abs(angleToDockWall) - 90
               elif angleToDockWall < 0:
                   turnAngle =  90 - abs(angleToDockWall)
               else:
                   turnAngle =  90
               print("Turn {:.0f} Parallel To Wall".format(turnAngle) )
               egpg.turn_degrees(turnAngle)
               distToDockNormal = distToDockWall * np.cos(np.radians(abs(angleToDockWall)))
               print("Distance To Dock Normal {:.1f} cm".format(distToDockNormal))
               egpg.drive_cm(distToDockNormal)
               egpg.turn_degrees(90*np.sign(angleToDockWall))
               print("ON POSITION FOR DOCKING APPROACH")
        else:
           strToLog = "findDock() reports failure at {}".format(timeStrNow)
           print(strToLog)
           if verbose:
               speak.say(strToLog)
               runLog.logger.info(strToLog)


    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
