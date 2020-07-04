#!/usr/bin/env python3

import cv2
import numpy as np
import os
import math
from math import pi
import argparse
import json
from copy import deepcopy


# ARGUMENT PARSER
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder", required=True, help="path to data folder")
ap.add_argument("-o", "--outfile", required=False, default=None, help="optional write final path map to OUTFILE (.png best)")
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
pathOutputFilename = args['outfile']   # if requested filename for path image - png gives better qual than jpg
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
               'heading_enc'         : self.heading_enc }

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
            +  "\nheading_enc: {:5.1f}".format(self.heading_enc)

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

def plotPath(dataFolder):

    robot = Robot(START_Xr, START_Yr,frame=0)
    prev_robot = Robot(START_Xr, START_Yr, frame= -1)

    os.chdir(dataFolder) #Path to data folder




    # Sonarangle = 15
    ds_beam = 12.5

    scale = float(1) / 10  # 1 pixel = 10 mm

    if display:
        cv2.namedWindow("Path Map", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Path Map", WINDOW_W, WINDOW_H)
        cv2.waitKey(50)

    map_image = np.zeros((MAP_SIZE_X_cm,MAP_SIZE_Y_cm,3),np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    colorBlue = (255, 0 , 0)
    colorRed  = (0,   0 , 255)
    fontLineW = 2  # pixels
    bottLft =  ( 5 , MAP_SIZE_Y_cm -5 )
    bottRt  =  ( MAP_SIZE_X_cm -35 , MAP_SIZE_Y_cm -5)
    cv2.putText(map_image, 'imu', bottLft, font, fontScale, colorRed, fontLineW, cv2.LINE_AA)
    cv2.putText(map_image, 'enc', bottRt, font, fontScale, colorBlue, fontLineW, cv2.LINE_AA)

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


        '''
        scaledFs = int (Fsonar*scale)
        scaledRs = int (Rsonar*scale)

        #cv2.ellipse(map_image,(int(Xr),int(Yr)),(scaledFs,scaledFs), imu_angle, -Sonarangle, Sonarangle, (0,255,0), -1)
        Xsf = Xr + float((math.cos(math.radians(imu_angle)) * Fsonar*scale))
        Ysf = Yr + float((math.sin(math.radians(imu_angle)) * Fsonar*scale))

        #cv2.ellipse(map_image,(int(Xr),int(Yr)),(scaledRs,scaledRs), angle, -Sonarangle, Sonarangle, (0,255,0), -1)
        Xsr = Xr + float((math.cos(math.radians(imu_angle)) * Rsonar*scale))
        Ysr = Yr + float((math.sin(math.radians(imu_angle)) * Rsonar*scale))

        XDS = Xr + float((math.cos(math.radians(imu_angle-45)) * DS*scale))
        YDS = Yr + float((math.sin(math.radians(imu_angle-45)) * DS*scale)) 

        cv2.line(map_image, (int(Xr),int(Yr)), (int(Xsf),int(Ysf)), (0,255,0), 1)
        cv2.line(map_image, (int(Xr),int(Yr)), (int(Xsr),int(Ysr)), (0,255,0), 1)
        cv2.line(map_image, (int(Xr),int(Yr)), (int(XDS),int(YDS)), (0,255,0), 1)
        '''

        cv2.line(map_image, (int(prev_robot.Xr_imu),int(prev_robot.Yr_imu)), (int(robot.Xr_imu),int(robot.Yr_imu)), (0,0,255), 1)
        cv2.line(map_image, (int(prev_robot.Xr_enc),int(prev_robot.Yr_enc)), (int(robot.Xr_enc),int(robot.Yr_enc)), (255,0,0), 1)

        if DEBUG:
            print("prev_robot:",prev_robot)
            print("robot:",robot)

        prev_robot = deepcopy(robot)


        if display:
            cv2.imshow("Path Map", map_image)
            cv2.waitKey(10)

    if (pathOutputFilename != None):
        cv2.imwrite(pathOutputFilename, map_image)
    cv2.waitKey(0)

if __name__ == '__main__': plotPath(dataFolder)
