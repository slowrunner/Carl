#!/usr/bin/env python3

"""
FILE:  sensorModel.py

PURPOSE:  Contains beam and line sensor model methods that update an occupancy grid based on probability a cell is empty
          between the robot sensor and a detected object

USAGE:
          import sensorModel

          # Calculate log probabilities for a sensor with an angular beam width:
          Beam_log, occ = BeamModel(Map_log, Xr, Yr, SensorAngle, SensorReading, BeamWidth, ObjThickness, scale)
          # add the sensor probabilities onto the occupancy grid
          Map_log = np.add(Map_log, Beam_log)

          # Calculate log probabilities for a sensor with no/minimal angular beam width:
          Beam_log, occ = BeamModel(Map_log, Xr, Yr, SensorAngle, SensorReading, BeamWidth, ObjThickness, scale)
          # add the sensor probabilities onto the occupancy grid
          Map_log = np.add(Map_log, Beam_log)

          For a 5m by 5m (MAP_SIZE_cm=500) map of 1 cm pixels (scale factor 0.1 * sensor reading in mm)
          Xr,Yr = robot position Y up, X right
          SensorAngle: 0 up 90 right
          SensorReading: in mm
          SensorMaximum: reading whtn nothing in range
"""

import cv2
import numpy as np
import os
import math


#####################################################################################################################################
# Beam Model
# occmap = map array, Xr = Robot X coordinate, Yr = Robot Y coordinate, Rangle = Robot heading in degrees, SensorDist = Sensor reading in mm
# thickness = Object thickness in mm, Scale = float map scale
#
# Returns: Odds_log - Array of log odds probabilities. This can be added to existing log odds occ map to update map with latest beam sensor data.
#          occ - Array of occupied points for scan matching
#####################################################################################################################################
def BeamModel(occmap, Xr, Yr, Rangle, BeamWidth_deg, SensorDist, SensorMax, thickness, scale):

    # Rotate 90 for GoPiGo3 Map Coords 0 deg up
    Rangle = (Rangle - 90) % 360.0

    Beam_mask = np.zeros((occmap.shape),np.uint8)
    Beam_log = np.zeros((occmap.shape),np.single)
    robotpt = (Xr,Yr)

    mapSize = occmap.shape[0]
    # print("mapSize = {}".format(mapSize))

    thickness = int(thickness * scale)
    SensorDist = int(SensorDist * scale)

    cv2.ellipse(Beam_mask,(int(Xr),int(Yr)),(SensorDist, SensorDist), Rangle, -BeamWidth_deg/2.0, BeamWidth_deg/2.0, 255, -1) #Draw ellipse on to Beam mask
    pixelpoints = cv2.findNonZero(Beam_mask) #Find all pixel points in Beam cone

    occ = np.empty((0,1,2),int)

    for x in pixelpoints:

        Ximg = x[0][0]
        Yimg = x[0][1]
        dist = np.linalg.norm(robotpt - x) #Find euclidean distance to all points in Beam cone from robot location

        theta = (math.degrees(math.atan2((Yimg-Yr),(Ximg-Xr)))) - Rangle #Find angle from robot location to each cell in pixelpoints


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
# occmap = map array, Xr = Robot X coordinate, Yr = Robot Y coordinate, Rangle = Sensor heading in degrees, SensorDist = reading in mm
# thickness = Object thickness in mm, Scale = float map scale
#
# Returns: Line_log - Array of log odds probabilities. This can be added to existing log odds occ map to update map.
#          occ - Array of occupied points for scan matching
#####################################################################################################################################
def LineModel(occmap, Xr, Yr, Rangle, SensorDist, SensorMax, thickness, scale):

    # Rotate 90 for GoPiGo3 Map Coords 0 deg up
    Rangle = (Rangle - 90) % 360.0

    Line_mask = np.zeros((occmap.shape),np.uint8)
    Line_log = np.zeros((occmap.shape),np.single)

    if SensorDist == 0:
        print('Sensor Reading Zero')
        return Line_log

    robotpt = (Xr,Yr)
    Sensor_Max = int(SensorMax * scale) # int(600 * scale)

    thickness = int(thickness * scale)
    SensorDist = int(SensorDist * scale)

    XLine = Xr + float((math.cos(math.radians(Rangle)) * SensorDist))
    YLine = Yr + float((math.sin(math.radians(Rangle)) * SensorDist)) 

    cv2.line(Line_mask, (int(Xr),int(Yr)), (int(XLine),int(YLine)), 255, 1)
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

    Xr = MAP_SIZE_cm / 2.0
    Yr = MAP_SIZE_cm * 3.0 / 4.0

    scale = float(1)/10 # each pixel is 10 mm

    cv2.namedWindow("sensorModel", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("sensorModel", 500, 500)
    cv2.waitKey(1)

    Map_log = np.full((MAP_SIZE_cm,MAP_SIZE_cm),0,np.single)

    SensorMax = 3000 # reading when no obj detected
    ObjThickness = 10

    SensorAngle = +42.5 # deg
    SensorReading = 1970  # mm

    Line_log, occ = LineModel(Map_log, Xr, Yr, SensorAngle, SensorReading, SensorMax, ObjThickness, scale)
    Map_log = np.add(Map_log, Line_log)

    ObjThickness = 10
    SensorAngle = 30 # deg
    BeamWidth = 25    # deg
    SensorReading = 2000

    Beam_log, occ = BeamModel(Map_log, Xr, Yr, SensorAngle, BeamWidth, SensorReading, SensorMax, ObjThickness, scale)
    Map_log = np.add(Map_log, Beam_log)

    SensorAngle = 45 # deg
    SensorReading = 1600
    Yr = Yr - 50
    Beam_log, occ = BeamModel(Map_log, Xr, Yr, SensorAngle, BeamWidth, SensorReading, SensorMax, ObjThickness, scale)
    Map_log = np.add(Map_log, Beam_log)


    Map_P = 1 - (1/(1+(np.exp(Map_log))))
    Disp_img = 1-Map_P
    cv2.imshow("sensorModel", Disp_img)
    cv2.waitKey(1)


    cv2.waitKey(0) #Leave window open



if __name__ == "__main__":  testMain()



