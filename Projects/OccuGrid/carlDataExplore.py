#!/usr/bin/env python3
#
# carlDataExplore.py

"""
Documentation:

    ToF Distance Sensor beam width 25 degrees (~25cm at 1 meter)
    Ensure Carl is located at undock point
    ( ./carlDataLogger.py -fps 1 -display   in a different window)
    ./carlDataExplore.py
    Quits on Keyboard Interrupt

    Repeat:
        Sweeps distance sensor across FoV of picamera in 5 beam widths {-50 -25  0 +25 +50} degrees around heading
        If no fwd obstruction within 1 meter, drives forward half meter, otherwise break
    Save StartToRoomY distance (traveled + dist to obstruction)
    Set Target Distance = half distance traveled
    Turn 180 CW
    Repeat:
        Sweeps distance sensor across FoV of picamera in 5 positions {-50 -25 0 +25 +50} degrees around heading
        If no fwd obstruction within 1 meter, drives forward half meter or till target distance, otherwise break
    Turn 90 CW
    Repeat:
        Sweeps distance sensor across FoV of picamera in 5 positions {-50 -25 0 +25 +50} degrees around heading
        If no obstruction within 1 meter, drives forward half meter, otherwise break
    Turn 180 CW
    Repeat:
        Sweeps distance sensor across FoV of picamera in 5 positions {-50 -25 0 +25 +50} degrees around heading
        If no obstruction within 1 meter, drives forward half meter, otherwise break
    Turn 90 CW
    Repeat:
        Sweeps distance sensor across FoV of picamera in 5 positions {-50 -25 0 +25 +50} degrees around heading
        If no fwd obstruction within 1 meter, drives forward half meter, otherwise break
    Turn 90 CW
    Repeat:
        Sweeps distance sensor across FoV of picamera in 5 positions {-50 -25 0 +25 +50} degrees around heading
        If no obstruction within distance to original search line, drives forward to orig search line, otherwise break
    Turn 90 CW
    Repeat:
        Sweeps distance sensor across FoV of picamera in 5 positions {-50 -25 0 +25 +50} degrees around heading
        If no obstruction within distance 1 meter, drives forward half meter, otherwise break





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
    from my_safe_inertial_measurement_unit import SafeIMUSensor
    import myBNO055 as BNO055
    from my_easygopigo3 import EasyGoPiGo3
    Carl = True
except:
    Carl = False

# import easygopigo3 # import the EasyGoPiGo3 class
import os
import numpy as np
import datetime as dt
import argparse
from time import sleep
from imutils.video import VideoStream
import imutils
import cv2

# ARGUMENT PARSER
ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--file", required=True, help="path to input file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
# ap.add_argument("-l", "--loop", default=False, action='store_true', help="optional loop mode")
ap.add_argument("-fps", "--fps", type=int, default=5, help="video frames with data capture per second")
ap.add_argument("-d", "--display", default=False, action='store_true', help="optional display video")
args = vars(ap.parse_args())
print("carlDataLogger.py Started with args:",args)
# filename = args['file']
# loopFlag = args['loop']
fps = args['fps']
display = args['display']
loopSleep = 1.0/fps

# CONSTANTS
DEBUG = False
# DEBUG = True

IMUPORT = "AD1"
IMUMODE = BNO055.OPERATION_MODE_IMUPLUS
DSPORT  = "RPI_1"  # ONLY HW I2C to keep I2C bus alive reliably
CODEC   = "MJPG"

# NOTE: Carl has v1.3 PiCamera

# PiCamera v1.3 Specifications
# 5MP Sensor 2592x1944 pixels
# 35mm f2.9 (FF DSLR equiv focal length)
# Fixed Focus 1m - infinity
# Full FoV = 53 x 41 degrees
# Valid PiCamera v1.3 Resolutions
IMAGEWIDTH   = 320  # 320  640  1024  1280  1296  1296  1920  2592
IMAGEHEIGHT  = 240  # 240  480   600   960   730   972  1080  1944
# Aspect Ratio        4:3  4:3   4:3   4:3  16:9   4:3  16:9C  4:3
#     C = Cropped FoV

# VARIABLES
start_dt = dt.datetime.now()
l_enc = 0
r_enc = 0
dl_enc = 0     # delta since prior reading
dr_enc = 0
reading_dt = start_dt
dReading_dt = 0      # delta since prior reading
imu_heading = 0
ds_range_mm = 9999
pan_angle = 0
data_h = None        # handle to <dt>/Data.txt 
egpg = None          # EasyGoPiGo3 object with bound sensor objects ds,imu,tp (TiltPan) (via "monkey-patching")
video_h = None
vs = None


# METHODS

def do_setup():
    global egpg, data_h, video_h, vs

    timestr = start_dt.strftime("%Y%m%d-%H%M%S")
    print("carlDataLogger started at {}".format(timestr))

    # Instantiate my_easygopigo3.EasyGoPiGo3 object
    try:
        egpg = EasyGoPiGo3(use_mutex=True)
        myconfig.setParameters(egpg)
        egpg.reset_encoders()
        if DEBUG: print("egpg initialized")
    except Exception as e:
        print("Unable to instantiate my_easygopigo3.EasyGoPiGo3 object")
        print(e)
        exit(1)

    # Instantiate ToF Distance Sensor, add to egpg
    try:
        egpg.ds = egpg.init_distance_sensor(port=DSPORT)
        if DEBUG: print("egpg.ds initialized")
    except Exception as e:
        print("Unable to instantiate DI distance_sensor")
        print(e)
        exit(1)

    # Instantiate my_safe_inertial_measurement_unit.SafeIMUSensor for the DI IMU Sensor
    try:
        egpg.imu = SafeIMUSensor(port = IMUPORT, use_mutex=True, mode=IMUMODE)
        sleep(1.0)  # allow to settle
        if DEBUG: print("egpg.imu initialized")
    except Exception as e:
        print("Unable to instantiate my_safe_inertial_measurement_unit.SafeIMUSensor")
        print(e)
        exit(1)

    # Instantiate tilt-pan servos
    try:
        egpg.tp = tiltpan.TiltPan(egpg)
        egpg.tp.tiltpan_center()
        egpg.tp.off()  # turn off till we need
        if DEBUG: print("egpg.tp initialized")

    except Exception as e:
        print("Unable to instantiate tiltpan servos")
        print(e)
        exit(1)

    try:
        os.mkdir(timestr, 0o777)
    except OSError:
        print("Could not create {}/".format(timestr))
        exit(1)
    try:
        os.chdir(timestr)
        data_h = open("Data.txt", 'w')
        headerStr = "{}              {: >7}  {: >7}   {: >7}  {: >6}  {}".format('timestr','l_enc','r_enc','imu_hdg','pan_ang','ds_mm')
        if DEBUG: print("writing: ",headerStr)
        data_h.write(headerStr + '\n')
    except Exception as e:
        print("Could not open Data file")
        print(e)
        exit(1)

    # Initialize picamera as videostream
    try:
        if DEBUG: print("Initializing PiCamera VideoStream")
        vs = VideoStream(usePiCamera=True, resolution=(IMAGEWIDTH,IMAGEHEIGHT))
        vs.start()
        sleep(2)   # let camera warm up
        fourcc = cv2.VideoWriter_fourcc(*CODEC)
        #                            filename,      codec,  fps,    ( width, height ),      color
        video_h = cv2.VideoWriter(timestr + '.avi', fourcc, fps, (IMAGEWIDTH, IMAGEHEIGHT), True)
        if video_h == None:
            print("VideoWriter() init failure")
            exit(1)
    except Exception as e:
        print("Could not initialize video")
        print(e)
        exit(1)


    print("carlDataLogger.do_setup() complete")

def readSensors():
    global egpg,l_enc,r_enc,dl_enc,dr_enc,reading_dt,dReading_dt,imu_heading,pan_angle,ds_range_mm

    prior_l_enc = l_enc
    prior_r_enc = r_enc
    prior_reading_dt = reading_dt

    reading_dt = dt.datetime.now()

    l_enc, r_enc = egpg.read_encoders()
    imu_heading = egpg.imu.safe_read_euler()[0]
    ds_range_mm = myDistSensor.adjustReadingInMMForError(egpg.ds.read_mm())
    pan_angle = egpg.tp.get_pan_pos() - tiltpan.PAN_CENTER

    dl_enc = l_enc - prior_l_enc
    dr_enc = r_enc - prior_r_enc
    dReading_dt = reading_dt - prior_reading_dt

def captureFrame():
    global vs,video_h
    try:
        frame = vs.read()   # read the frame from videostream
        if DEBUG: print("captureFrame: frame (h,w)={}".format((frame.shape[:2])))
        video_h.write(frame)
        if DEBUG: print("wrote video frame")
        if display:
            cv2.imshow("Frame Saved", frame)
            cv2.waitKey(1)
    except Exception as e:
        print("captureFrame() Exception")
        print(e)


def do_teardown():
    global data_h,egpg,video_h,vs

    print("carlDataLogger: Begin do_teardown()")

    if (egpg != None): egpg.stop()
    sleep(1)

    # close data file
    data_h.close()

    # close any display windows
    cv2.destroyAllWindows()

    # close video file 
    vs.stop()
    video_h.release()
    sleep(1)


    print("carlDataLogger: Teardown complete")


def writeData():
    global data_h,l_enc,r_enc,dl_enc,dr_enc,reading_dt,dReading_dt,imu_heading,pan_angle,ds_range_mm

    timestr = reading_dt.strftime("%Y%m%d-%H%M%S.%f")[:-3]
    dataStr = "{}, {:> 7d}, {:> 7d}, {:> 7.1f}, {:> 6.1f}, {:> 7.0f}".format(timestr,l_enc,r_enc,imu_heading,pan_angle,ds_range_mm)
    if DEBUG: print("writing: ",dataStr)
    data_h.write(dataStr + '\n')

# MAIN

def main():

    runLog.logger.info("Started")
    do_setup()

    try:
        # Do Somthing in a Loop
        loopCount = 0
        keepLooping = True

        while keepLooping:
            loopCount += 1
            # do something
            readSensors()
            writeData()
            captureFrame()
            sleep(loopSleep)



    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
            print("\n*** Ctrl-C detected - Finishing up")

    finally:
        do_teardown()
        sleep(1)

    runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
