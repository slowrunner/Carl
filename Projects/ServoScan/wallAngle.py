#!/usr/bin/env python
############################################################################################
# This program finds angle to a wall using the plib servoscan package
#
# History
# ------------------------------------------------
# Author     	Date      		Comments
# McDonley      July 2019     Created
#

#
from __future__ import print_function
from __future__ import division
#
import easygopigo3

import sys
sys.path.append('/home/pi/Carl/plib')

import runLog
from collections import Counter
import math
from time import sleep
import printmaps
import servoscan
import numpy as np
import tiltpan
import myconfig
import myDistSensor

debug = False			# True to print all raw values
IGNORE_OVER_CM = 230


# returns r, theta_degrees
def cart2polar(x,y):
    return np.hypot(x,y), math.degrees(math.atan2(y,x))

def cartl2polarl(xl,yl):
    rl = []
    tl = []
    if 0 < len(xl) == len(yl):
        for x,y in zip(xl,yl):
            r,t = cart2polar(x,y)
            rl += [r]
            tl += [t]
    return rl,tl

# polar2cart(r,theta) returns x,y
def polar2cart(r,theta_deg):
    return r * math.cos(math.radians(theta_deg)), r * math.sin(math.radians(theta_deg))

def polarl2cartl(rl, theta_degl):
    xl = []
    yl = []
    if 0 < len(rl) == len(theta_degl):
        for r,theta in zip(rl,theta_degl):
            x,y = polar2cart(r,theta)
            xl += [x]
            yl += [y]
    return xl,yl

def wallAngle(x_list,y_list):
        angle = float('nan')
        if len(y_list) == len(x_list) > 1:
            wall_mb = np.polyfit(x_list,y_list,1)
            #print ("wall_mb",wall_mb)
            #print ("wall_mb[0]",wall_mb[0])
            angle = np.arctan(wall_mb[0])
        return angle

# MAIN
def main():
    try:
        # Create an instance egpg of the GoPiGo3 class.
        egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)    # use_mutex=True for "thread-safety"
        myconfig.setParameters(egpg)

        ds = myDistSensor.init(egpg)
        tp = tiltpan.TiltPan(egpg)

        runLog.logger.info("Starting wallAngle.py at {0:0.2f}v".format(egpg.volt()))

        # Scan in front of GoPiGo3
        dist_l,ang_l=servoscan.ds_map(ds,tp,sector=60)
        closest_object = min(dist_l)
        tp.center()
        tp.off()

        # Print scan data on terminal
        printmaps.view180(dist_l,ang_l,grid_width=80,units="cm",ignore_over=IGNORE_OVER_CM)


        x_list,y_list = polarl2cartl(dist_l,ang_l)
        # print("x_list:",x_list)
        # print("y_list:",y_list)

        angle = wallAngle(x_list,y_list)
        if np.isnan(angle):
            print("Not enough points to determine wall angle")
        else:
            angle = np.degrees(angle)
            print("angle:{:.0f}".format(angle) )
            egpg.turn_degrees(angle)

    except KeyboardInterrupt:
	print("**** Ctrl-C detected.  Finishing Up ****")
    runLog.logger.info("Exiting  wallAngle.py at {0:0.2f}v".format(egpg.volt()))
    tp.center()
    sleep(2)
    tp.off()


if __name__ == "__main__":
	main()
