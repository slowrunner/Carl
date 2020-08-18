#!/usr/bin/env python3

"""
FILE:  sensorModel.py

PURPOSE:  Contains beam and line sensor model methods that update an occupancy grid based on probability a cell is empty
          between the robot sensor and a detected object

FRAME:    Robot Frame is "Y:up, 0degrees:up, CW:positive, X:right", Map Frame: (OpenCV) Y:down X:right
          Robot X0,Y0 in Map Frame:  Xmap_Xr0,Ymap_Yr0
          Base model computation frame (from BigWheelBot): 0 deg right, CW positive, Y:down, X:right, 0,0 upper-left
USAGE:
          import sensorModel

          # Calculate log probabilities for a sensor with an angular beam width:
          Beam_log, occ = BeamModel(Map_log, Xr, Yr, Xmap_Xr0, Ymap_Yr0, SensorAngle, SensorReading, BeamWidth, ObjThickness, scale)
          # add the sensor probabilities onto the occupancy grid
          Map_log = np.add(Map_log, Beam_log)

          # Calculate log probabilities for a sensor with no/minimal angular beam width:
          Beam_log, occ = BeamModel(Map_log, Xr, Yr, Xmap_Xr0, Ymap_Yr0, SensorAngle, SensorReading, BeamWidth, ObjThickness, scale)
          # add the sensor probabilities onto the occupancy grid
          Map_log = np.add(Map_log, Beam_log)

          For a 5m by 5m (MAP_SIZE_cm=500) map of 1 cm pixels (scale factor 0.1 * sensor reading in mm)
          Xr,Yr = robot position Y up, X right
          SensorAngle: 0 up 90 right
          SensorReading: in mm
          SensorMaximum: reading when nothing in range
"""

import cv2
import numpy as np
import os
import math


#####################################################################################################################################
# Beam Model
#   occmap = map array, 
#   Xr = Robot X coordinate, Yr = Robot Y coordinate, 
#   Xmap_Xr0 = X on Map of robot X0, Ymap_Yr0 = Y on Map of robot Y0
#   Rangle = Robot heading in degrees, 
#   SensorDist = Sensor reading in mm
#   thickness = Object thickness in mm, 
#   Scale = float map scale
#   debug [False] will print info if True
#
# Returns: Odds_log - Array of log odds probabilities. This can be added to existing log odds occ map to update map with latest beam sensor data.
#          occ - Array of occupied points for scan matching
#####################################################################################################################################
def BeamModel(occmap, Xr, Yr, Xmap_Xr0, Ymap_Yr0, Rangle, BeamWidth_deg, SensorDist, SensorMax, thickness, scale, debug=False):

    if debug:
        print("\nBeamModel(): ")
        print("   Xr,Yr: {} {}  Xmap_Xr0,Ymap_Yr0: {} {}".format(Xr,Yr,Xmap_Xr0,Ymap_Yr0))
        print("   Rangle: {} BeamWidth: {} Range: {}  Max: {}".format(Rangle,BeamWidth_deg,SensorDist,SensorMax))
        print("   Thickness: {} scale: {}".format(thickness,scale))
        print("\n")

    # Rotate GoPiGo3 Map Coords 0 deg up to computation frame 0 degrees is to right
    Rangle = (Rangle - 90) % 360.0
    if debug: print("Sensor Heading in computation frame: {:5.1f} deg".format(Rangle))

    Beam_mask = np.zeros((occmap.shape),np.uint8)
    Beam_log = np.zeros((occmap.shape),np.single)

    # robotpt = (Xr,Yr)
    robotpt = (Xmap_Xr0 + Xr,Ymap_Yr0 - Yr)  # to computation frame from robot frame
    if debug: print("robot in map frame: X:{} Y:{}".format(robotpt[0], robotpt[1]))

    mapSize = occmap.shape[0]
    if debug: print("mapSize = {}".format(mapSize))

    thickness = int(thickness * scale)
    SensorDist = int(SensorDist * scale)

    #           image           ctr          mjr,minor axis length    rotAng    start angle          end angle  color:white  thickness(-1 = fill)
    # cv2.ellipse(Beam_mask,(int(Xr),int(Yr)),(SensorDist, SensorDist), Rangle, -BeamWidth_deg/2.0, BeamWidth_deg/2.0, 255, -1) #Draw ellipse on to Beam mask
    cv2.ellipse(Beam_mask,(int(robotpt[0]),int(robotpt[1])),(SensorDist, SensorDist), Rangle, -BeamWidth_deg/2.0, BeamWidth_deg/2.0, 255, -1) #Draw ellipse on to Beam mask
    pixelpoints = cv2.findNonZero(Beam_mask) #Find all pixel points in Beam cone

    occ = np.empty((0,1,2),int)

    for x in pixelpoints:

        Ximg = x[0][0]
        Yimg = x[0][1]
        dist = np.linalg.norm(robotpt - x) #Find euclidean distance to all points in Beam cone from robot location

        # theta = (math.degrees(math.atan2((Yimg-Yr),(Ximg-Xr)))) - Rangle #Find angle from robot location to each cell in pixelpoints
        theta = (math.degrees(math.atan2((Yimg-robotpt[1]),(Ximg-robotpt[0])))) - Rangle #Find angle from robot location to each cell in pixelpoints


        if theta < -180:                                                 #Note:numpy and OpenCV X and Y reversed
            theta = theta + 360
        elif theta > 180:
            theta = theta - 360

        sigma_t = 5
        A = 1 / (math.sqrt(2*math.pi*sigma_t))
        C = math.pow((theta/sigma_t),2)
        B = math.exp(-0.5*C)
        Ptheta = A*B

        Pdist = (SensorDist - dist/2)/SensorDist
        P = (Pdist*2)*Ptheta


        if dist > SensorDist - thickness and dist < SensorDist + thickness: #occupied region
            # if SensorDist < Sensor_Max: #Only update occupied region if reading is less than senor maximum.
            Px = 0.5 + Ptheta
            logPx = math.log(Px/(1-Px))
            Beam_log[Yimg][Ximg] = logPx
            #occ = np.append(occ,[x],0)
        else: #free region
            Px = 0.5 - P
            logPx = math.log(Px/(1-Px))
            Beam_log[Yimg][Ximg] = logPx


    return Beam_log, occ

#####################################################################################################################################
# Line Model
#   occmap = map array,
#   Xr = Robot X coordinate, Yr = Robot Y coordinate, robot frame
#   Xmap_Xr0 = X on Map of robot X0, Ymap_Yr0 = Y on Map of robot Y0
#   Rangle = Sensor heading in degrees in robot frame
#   SensorMax = value when the sensor does not detect anything within its maximum detection range
#   SensorDist = reading in mm
#   thickness = Object thickness in mm,
#   scale = float map scale
#   debug [False] will print info if True
#
# Returns: Line_log - Array of log odds probabilities. This can be added to existing log odds occ map to update map.
#          occ - Array of occupied points for scan matching
#####################################################################################################################################
def LineModel(occmap, Xr, Yr, Xmap_Xr0, Ymap_Yr0, Rangle, SensorDist, SensorMax, thickness, scale, debug=False):

    # Rotate GoPiGo3 Map Coords 0 deg up to computation frame 0 degrees is to right
    Rangle = (Rangle - 90) % 360.0
    if debug: print("Sensor Heading in computation frame: {:5.1f} deg".format(Rangle))

    Line_mask = np.zeros((occmap.shape),np.uint8)
    Line_log = np.zeros((occmap.shape),np.single)

    if SensorDist == 0:
        if debug: print('Sensor Reading Zero')
        return Line_log

    # robotpt = (Xr,Yr)
    robotpt = (Xmap_Xr0 + Xr,Ymap_Yr0 - Yr)  # to computation frame from robot frame
    if debug: print("robot in map frame: X:{} Y:{}".format(robotpt[0], robotpt[1]))

    Sensor_Max = int(SensorMax * scale) # int(600 * scale)

    thickness = int(thickness * scale)
    SensorDist = int(SensorDist * scale)

    # XLine = Xr + float((math.cos(math.radians(Rangle)) * SensorDist))
    XLine = robotpt[0] + float((math.cos(math.radians(Rangle)) * SensorDist))
    # YLine = Yr + float((math.sin(math.radians(Rangle)) * SensorDist))
    YLine = robotpt[1] + float((math.sin(math.radians(Rangle)) * SensorDist))

    cv2.line(Line_mask, (int(robotpt[0]),int(robotpt[1])), (int(XLine),int(YLine)), 255, 1)
    pixelpoints = cv2.findNonZero(Line_mask) #Find all pixel points in cone

    occ = np.empty((0,1,2),int)

    for x in pixelpoints:
        Ximg = x[0][0]
        Yimg = x[0][1]
        dist = np.linalg.norm(robotpt - x) #Find euclidean distance to all points in Line range from robot location

        Pdist = (SensorDist - (dist/2))/SensorDist

        if dist > SensorDist - thickness and dist < SensorDist + thickness: #occupied region
            if SensorDist < Sensor_Max: #Only update occupied region if Line reading is less than maximum.
                Px = 0.8
                logPx = math.log(Px/(1-Px))
                Line_log[Yimg][Ximg] = logPx
                #occ = np.append(occ,[x],0)
        else: #free region
            Px = 0.3 #0.5 - (Pdist/3)
            logPx = math.log(Px/(1-Px))
            Line_log[Yimg][Ximg] = logPx

    return Line_log, occ



def testMain():
    # Test Main

    print("Sensor Model Test Main")

    MAP_SIZE_cm = 500

    Xr = 0
    Yr = 0

    Xmap_Xr0 = MAP_SIZE_cm / 2.0
    Ymap_Yr0 = MAP_SIZE_cm * 3.0 / 4.0

    # Xr = Xmap_Xr0
    # Yr = Ymap_Yr0

    scale = float(1)/10 # each pixel is 10 mm

    cv2.namedWindow("sensorModel", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("sensorModel", 500, 500)
    cv2.waitKey(1)

    Map_log = np.full((MAP_SIZE_cm,MAP_SIZE_cm),0,np.single)

    SensorMax = 3000 # reading when no obj detected
    ObjThickness = 10

    SensorAngle = +42.5 # deg
    SensorReading = 1970  # mm

    Line_log, occ = LineModel(Map_log, Xr, Yr, Xmap_Xr0, Ymap_Yr0, SensorAngle, SensorReading, SensorMax, ObjThickness, scale, debug=True)
    Map_log = np.add(Map_log, Line_log)

    ObjThickness = 10
    SensorAngle = 30 # deg
    BeamWidth = 25    # deg
    SensorReading = 2000

    Beam_log, occ = BeamModel(Map_log, Xr, Yr, Xmap_Xr0, Ymap_Yr0, SensorAngle, BeamWidth, SensorReading, SensorMax, ObjThickness, scale, debug=True)
    Map_log = np.add(Map_log, Beam_log)

    SensorAngle = 45 # deg
    SensorReading = 1600
    Yr = Yr + 50
    Beam_log, occ = BeamModel(Map_log, Xr, Yr, Xmap_Xr0, Ymap_Yr0, SensorAngle, BeamWidth, SensorReading, SensorMax, ObjThickness, scale, debug=True)
    Map_log = np.add(Map_log, Beam_log)


    Map_P = 1 - (1/(1+(np.exp(Map_log))))
    Disp_img = 1-Map_P
    cv2.imshow("sensorModel", Disp_img)
    cv2.waitKey(1)


    cv2.waitKey(0) #Leave window open



if __name__ == "__main__":  testMain()



