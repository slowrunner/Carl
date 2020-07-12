#!/usr/bin/env python3

import cv2
import numpy as np
import os
import math
from math import pi
import argparse
import json
from copy import deepcopy

"""
FILE:      myOcc_Grid.py
USAGE:   ./myOcc_Grid.py [-h] -f FOLDER [-o OUTFILE] [-s SIZE] [-v] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -f FOLDER, --folder FOLDER
                        path to data folder
  -o OUTFILE, --outfile OUTFILE
                        optional write final path map to OUTFILE (.png best)
  -s SIZE, --size SIZE  optional map size [400] in cm
  -v, --verbose         optional verbose DEBUG mode
  -d, --display         optional display path during analysis

"""

# ARGUMENT PARSER
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder", required=True, help="path to data folder")
ap.add_argument("-oi", "--outIMUfile", required=False, default=None, help="optional write final IMU occ grid to file (.png best)")
ap.add_argument("-oe", "--outENCfile", required=False, default=None, help="optional write final Encoders occ grid to file (.png best)")
ap.add_argument("-s", "--size", type=int, default=400, help="optional map size [400] in cm")
ap.add_argument("-v", "--verbose", default=False, action='store_true', help="optional verbose DEBUG mode")
# ap.add_argument("-fps", "--fps", type=int, default=4, help="video [4] frames with data capture per second")
ap.add_argument("-d", "--display", default=False, action='store_true', help="optional display path during analysis")
args = vars(ap.parse_args())
print("path_plot.py Started with args:",args)
dataFolder = args['folder']
# loopFlag = args['loop']
display = args['display']  # default False  -d or --display to show map as it is built
DEBUG = args['verbose']    # default False  -v or --verbose to set True
pathOutIMUFilename = args['outIMUfile']   # if requested filename for IMU occ grid image - png gives better qual than jpg
pathOutENCFilename = args['outENCfile']   # if requested filename for Encoders occ grid image - png gives better qual than jpg
MAP_SIZE_X_cm = args['size']   # default 400 -s or --size to change
MAP_SIZE_Y_cm = MAP_SIZE_X_cm  # always use square playing field

START_Xr = MAP_SIZE_X_cm / 2.0     # will start in center left/right of map
START_Yr = MAP_SIZE_Y_cm / 4.0 * 3 # will start in 1/4 up from bottom of map

WINDOW_H = 600  # window size in pixels
WINDOW_W = 600  # pixels

ROBOT_CONFIG_FILE = "/home/pi/Dexter/gpg3_config.json"

class Robot(object):
    def __init__(self,  x: int = 0, y: int = 0, heading: float = 0.0, enc_l: int = 0, enc_r: int = 0,  config_file_path=ROBOT_CONFIG_FILE, frame: int = 0):
        if (config_file_path != None): 
            self.load_robot_constants(config_file_path)
        self.frame = frame
        self.Xr_imu = x
        self.Yr_imu = y
        self.Xr_enc = x
        self.Yr_enc = y
        self.l_enc  = enc_l
        self.r_enc  = enc_r
        self.imu_offset = heading
        self.heading_imu = heading
        self.heading_enc = heading
        self.traveled_mm = 0

    def __repr__(self):
        if DEBUG: print("__repr__ executing")

        rs = { 'wheel_diameter'      : self.wheel_diameter ,
               'wheel_base_width'    : self.wheel_base_width ,
               'wheel_circumference' : self.wheel_circumference ,
               'wheel_base_circumference' : self.wheel_base_circumference ,
               'frame'                : self.frame ,
               'Xr_imu'              : self.Xr_imu ,
               'Yr_imu'              : self.Yr_imu ,
               'Xr_enc'              : self.Xr_enc ,
               'Yr_enc'              : self.Yr_enc ,
               'l_enc'               : self.l_enc ,
               'r_enc'               : self.r_enc ,
               'imu_offset'          : self.imu_offset ,
               'heading_imu'         : self.heading_imu ,
               'heading_enc'         : self.heading_enc,
               'traveled_mm'         : self.traveled_mm }

        return rs

    def __str__(self):

        rstr = "\nwheel_diameter:{:5.2f}".format(self.wheel_diameter) \
            +  "\nwheel_base_width:{:6.2f}".format(self.wheel_base_width) \
            +  "\nwheel_circumference:{:6.2f}".format(self.wheel_circumference) \
            +  "\nwheel_base_circumference:{:6.2f}".format(self.wheel_base_circumference) \
            +  "\nframe: {:d}".format(self.frame) \
            +  "\nXr_imu: {:8.1f}".format(self.Xr_imu) \
            +  "\nYr_imu: {:8.1f}".format(self.Yr_imu) \
            +  "\nXr_enc: {:8.1f}".format(self.Xr_enc) \
            +  "\nYr_enc: {:8.1f}".format(self.Yr_enc) \
            +  "\nl_enc:  {:8.0f}".format(self.l_enc) \
            +  "\nr_enc:  {:8.0f}".format(self.r_enc) \
            +  "\nimu_offset: {:5.1f}".format(self.imu_offset) \
            +  "\nheading_imu: {:5.1f}".format(self.heading_imu) \
            +  "\nheading_enc: {:5.1f}".format(self.heading_enc) \
            +  "\ntraveled_mm: {:9.0f}".format(self.traveled_mm)

        return rstr


    def __eq__(self, other):
        return NotImplemented


    def load_robot_constants( self, config_file_path="/home/pi/Dexter/gpg3_config.json" ):
        with open(config_file_path, 'r') as json_file:
            data = json.load(json_file)
            if data['wheel-diameter'] > 0 and data['wheel-base-width'] > 0:
                self.wheel_diameter = data['wheel-diameter']
                self.wheel_base_width = data['wheel-base-width']
                self.wheel_circumference = self.wheel_diameter * pi
                self.wheel_base_circumference = self.wheel_base_width * pi

            else:
                self.wheel_diameter = 66.5
                self.wheel_base_width = 117
                self.wheel_circumference = self.wheel_diameter * pi
                self.wheel_base_circumference = self.wheel_base_width * pi

def enc_to_dist_mm(robot,prev_robot):
    d_enc_l = robot.l_enc - prev_robot.l_enc
    d_enc_r = robot.r_enc - prev_robot.r_enc
    d_enc_ave = (d_enc_l + d_enc_r) / 2.0
    dist = robot.wheel_circumference * d_enc_ave / 360.0
    if DEBUG: print("[enc_to_dist_mm] d_enc_l: {} d_enc_r: {} d_enc_ave: {} dist: {}".format(d_enc_l, d_enc_r, d_enc_ave,dist))
    return dist

def enc_to_angle_deg(robot,prev_robot):
    d_enc_l = robot.l_enc - prev_robot.l_enc
    d_enc_r = robot.r_enc - prev_robot.r_enc
    d_enc_diff = (d_enc_l - d_enc_r) / 2.0
    return robot.wheel_diameter * d_enc_diff / robot.wheel_base_width

def plotOccGrid(dataFolder):

    robot = Robot(START_Xr, START_Yr,frame=0)
    prev_robot = Robot(START_Xr, START_Yr, frame= -1)

    os.chdir(dataFolder) #Path to data folder

    #  Distance Sensor Beam Width is 25 degrees
    ds_beam = 25.0

    scale = float(1) / 10  # 1 pixel = 10 mm

    if display:
        cv2.namedWindow("IMU Grid", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("IMU Grid", WINDOW_W, WINDOW_H)
        cv2.namedWindow("Encoder Grid", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Encoder Grid", WINDOW_W, WINDOW_H)
        cv2.waitKey(50)

    map_image = np.zeros((MAP_SIZE_X_cm,MAP_SIZE_Y_cm,3),np.uint8)
    imu_image = np.zeros((MAP_SIZE_X_cm,MAP_SIZE_Y_cm,3),np.uint8)
    enc_image = np.zeros((MAP_SIZE_X_cm,MAP_SIZE_Y_cm,3),np.uint8)

    # font = cv2.FONT_HERSHEY_SIMPLEX
    # fontScale = 0.5
    colorBlue = (255, 0 , 0)
    colorRed  = (0,   0 , 255)
    # fontLineW = 2  # pixels
    # bottLft =  ( 5 , MAP_SIZE_Y_cm -5 )
    # bottRt  =  ( MAP_SIZE_X_cm -35 , MAP_SIZE_Y_cm -5)
    # cv2.putText(map_image, 'imu', bottLft, font, fontScale, colorRed, fontLineW, cv2.LINE_AA)
    # cv2.putText(map_image, 'enc', bottRt, font, fontScale, colorBlue, fontLineW, cv2.LINE_AA)

    if display: cv2.waitKey(50)

    f = open("Data.txt", "r")
    lineCnt = 0
    for line in f:
        lineCnt += 1
        if lineCnt == 1:
            if DEBUG: print("header: {}".format(line))
            continue
        if DEBUG: print("data  : {}".format(line))
        robot.frame = lineCnt

        # mylist = [int(x) for x in line.split(',')]
        mylist = [item for item in line.split(',')]

        # dt, l_enc, r_enc, imu_heading, pan_angle, ds_mm
        #  0    1      2        3           4         5
        robot.heading_imu = float(mylist[3])

        robot.l_enc = int(mylist[1])
        robot.r_enc = int(mylist[2])

        if lineCnt == 2:    # first data line
            robot.imu_offset = robot.heading_imu
            prev_robot = deepcopy(robot)
            prev_robot.frame = 1

        # compute distance travelled
        enc_dist_mm = enc_to_dist_mm(robot, prev_robot)
        robot.traveled_mm += enc_dist_mm
        if DEBUG:
            if enc_dist_mm > 0: print("enc_dist_mm: {:4.1f}".format(enc_dist_mm))

        # compute rotation according to encoders
        d_enc_heading = enc_to_angle_deg(robot, prev_robot)

        # compute rotation according to imu
        d_imu_heading = (robot.heading_imu - prev_robot.heading_imu)/2

        # compute new encoder heading
        robot.heading_enc = (prev_robot.heading_enc + d_enc_heading) % 360.0

        # Fsonar = mylist[3]*10
        Fsonar = 0
        # Rsonar = mylist[4]*10
        Rsonar = 0
        DS = int(mylist[5])


        robot.Xr_imu = prev_robot.Xr_imu + float((math.cos(math.radians((prev_robot.heading_imu + d_imu_heading)-90-robot.imu_offset)) * enc_dist_mm * scale))
        robot.Yr_imu = prev_robot.Yr_imu + float((math.sin(math.radians((prev_robot.heading_imu + d_imu_heading)-90-robot.imu_offset)) * enc_dist_mm * scale))

        robot.Xr_enc = prev_robot.Xr_enc + float((math.cos(math.radians((prev_robot.heading_enc + d_enc_heading)-90)) * enc_dist_mm * scale))
        robot.Yr_enc = prev_robot.Yr_enc + float((math.sin(math.radians((prev_robot.heading_enc + d_enc_heading)-90)) * enc_dist_mm * scale))


        cv2.line(imu_image, (int(prev_robot.Xr_imu),int(prev_robot.Yr_imu)), (int(robot.Xr_imu),int(robot.Yr_imu)), colorRed, 1)
        cv2.line(enc_image, (int(prev_robot.Xr_enc),int(prev_robot.Yr_enc)), (int(robot.Xr_enc),int(robot.Yr_enc)), colorBlue, 1)

        if DEBUG:
            print("prev_robot:",prev_robot)
            print("robot:",robot)

        prev_robot = deepcopy(robot)


        if display:
            cv2.imshow("IMU Grid", imu_image)
            cv2.imshow("Encoder Grid", enc_image)
            cv2.waitKey(10)

    if (pathOutIMUFilename != None):
        cv2.imwrite(pathOutIMUFilename, imu_image)
    if (pathOutENCFilename != None):
        cv2.imwrite(pathOutENCFilename, imu_image)

    cv2.waitKey(0)

if __name__ == '__main__': plotOccGrid(dataFolder)
