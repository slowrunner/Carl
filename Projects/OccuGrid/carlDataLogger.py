#!/usr/bin/env python3
#
# carlDataLogger.py

"""
Documentation:

    Records Camera at 320x240 at [-fps 4] to start_datetime_str/start_datetime_str.avi
    Records datetime_str, l_enc, r_enc, imu_heading, servo angle, range for each frame to Data.txt
    Uses kbd_easygopigo3.GoPiGo3WithKeyboard class to control the bot and pan servo mounted range sensor
    Quits when Esc key pressed

    USAGE:  ./carlDataLogger.py [-fps 4] [-d or --display] [--help]

    Note: On RPi 3B, 4 fps is maximum for accurate interval data and video
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
    # from my_easygopigo3 import EasyGoPiGo3
    from kbd_easygopigo3 import GoPiGo3WithKeyboard
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
import signal
# module for capturing keyboard input events
from curtsies import Input


# ARGUMENT PARSER
ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--file", required=True, help="path to input file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
# ap.add_argument("-l", "--loop", default=False, action='store_true', help="optional loop mode")
ap.add_argument("-fps", "--fps", type=int, default=4, help="video [4] frames with data capture per second")
ap.add_argument("-d", "--display", default=False, action='store_true', help="optional display video")
args = vars(ap.parse_args())
print("carlDataLogger.py Started with args:",args)
# filename = args['file']
# loopFlag = args['loop']
fps = args['fps']
display = args['display']

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
# egpg = None          # EasyGoPiGo3 object with bound sensor objects ds,imu,tp (TiltPan) (via "monkey-patching")
kegpg = None         # GoPiGo3WithKeyboard object with bound sensor objects ds,imu,tp (TiltPan) (via "monkey-patching")
video_h = None
vs = None
rw_timing = 0.05 # initial guess for time to read sensors and write to Data.txt file
kbdWaitTime = .001  # 
# set loopSleep to make loop as close to the requested fps as possible
loopSleep = ((1.0/fps)-rw_timing-kbdWaitTime) if ((1.0/fps) > (rw_timing+kbdWaitTime)) else 0.001


# METHODS

def do_setup():
    global kegpg, data_h, video_h, vs

    timestr = start_dt.strftime("%Y%m%d-%H%M%S")
    print("carlDataLogger started at {}".format(timestr))

    # Instantiate my_easygopigo3.EasyGoPiGo3 object
    try:
        # egpg = EasyGoPiGo3(use_mutex=True)
        kegpg = GoPiGo3WithKeyboard(use_mutex=True)
        # myconfig.setParameters(egpg)
        myconfig.setParameters(kegpg.gopigo3)
        # egpg.reset_encoders()
        kegpg.gopigo3.reset_encoders()
        if DEBUG: print("kegpg initialized")
    except Exception as e:
        # print("Unable to instantiate my_easygopigo3.EasyGoPiGo3 object")
        print("Unable to instantiate kbd_easygopigo3.GoPiGo3WithKeyboard object")
        print(e)
        exit(1)

    # Instantiate ToF Distance Sensor, add to kegpg
    try:
        # egpg.ds = egpg.init_distance_sensor(port=DSPORT)
        kegpg.ds = kegpg.gopigo3.init_distance_sensor(port=DSPORT, use_mutex=True)
        if DEBUG: print("kegpg.ds initialized")
    except Exception as e:
        print("Unable to instantiate DI distance_sensor")
        print(e)
        exit(1)

    # Instantiate my_safe_inertial_measurement_unit.SafeIMUSensor for the DI IMU Sensor
    try:
        # egpg.imu = SafeIMUSensor(port = IMUPORT, use_mutex=True, mode=IMUMODE)
        kegpg.imu = SafeIMUSensor(port = IMUPORT, use_mutex=True, mode=IMUMODE)
        sleep(1.0)  # allow to settle
        if DEBUG: print("kegpg.imu initialized")
    except Exception as e:
        print("Unable to instantiate my_safe_inertial_measurement_unit.SafeIMUSensor")
        print(e)
        exit(1)

    # Instantiate tilt-pan servos
    """  (Initialized by kbd_easygopigo3 as kegpg.tp)
    try:
        egpg.tp = tiltpan.TiltPan(egpg)
        egpg.tp.tiltpan_center()
        egpg.tp.off()  # turn off till we need
        if DEBUG: print("egpg.tp initialized")

    except Exception as e:
        print("Unable to instantiate tiltpan servos")
        print(e)
        exit(1)
    """
    # initialize new folder and data file
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


    # write logo and key commands menu
    kegpg.drawLogo()
    kegpg.drawDescription()
    kegpg.drawMenu()
    kegpg.result = "nothing"  # hold the last command result string
    #     result will be one of "nothing", "moving", "path", "static", "exit"

    # if manual_mode is set to true, then the robot
    # moves for as long as the coresponding keys are pressed
    # if manual_mode is set to False, then a key needs
    # to be pressed once in order for the robot to start moving
    kegpg.manual_mode = False

    # set up a handler for ignoring the Ctrl+Z commands
    signal.signal(signal.SIGTSTP, lambda signum, frame : print("Press <ESC> to quit"))

    print("carlDataLogger.do_setup() complete")

def checkKbdForCmd(waitTime):
    global kegpg

    # if nothing captured in waitTime seconds returns None
    key = kegpg.input_generator.send(waitTime)

    # if key event captured, execute it
    if key is not None:
        kegpg.result = kegpg.executeKeyboardJob(key)
        if kegpg.result == "exit":
            raise KeyboardInterrupt
    elif kegpg.manual_mode is True and kegpg.result == "moving":
        kegpg.executeKeyboardJob("x")

def readSensors():
    global egpg,l_enc,r_enc,dl_enc,dr_enc,reading_dt,dReading_dt,imu_heading,pan_angle,ds_range_mm,kegpg

    prior_l_enc = l_enc
    prior_r_enc = r_enc
    prior_reading_dt = reading_dt

    reading_dt = dt.datetime.now()

    l_enc, r_enc = kegpg.gopigo3.read_encoders()
    imu_heading = kegpg.imu.safe_read_euler()[0]
    ds_range_mm = myDistSensor.adjustReadingInMMForError(kegpg.ds.read_mm())
    pan_angle = kegpg.tp.get_pan_pos() - tiltpan.PAN_CENTER

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
    global data_h,kegpg,video_h,vs

    print("carlDataLogger: Begin do_teardown()")

    if (kegpg != None): kegpg.gopigo3.stop()
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

def handleSIGTERM(*argv):
    raise SystemExit()
    return



def remoteControl():
   return 0


# MAIN

def main():
    global kbdWaitTime, loopSleep, rw_timing

    runLog.logger.info("Started")
    do_setup()
    # signal.signal(signal.SIGTERM,handleSIGTERM)

    try:
        loopCount = 0
        keepLooping = True
        with Input(keynames = "curtsies", sigint_event = True) as input_generator:
            kegpg.input_generator = input_generator
            while keepLooping:
                dtRWStart = dt.datetime.now()
                loopCount += 1
                readSensors()
                writeData()
                captureFrame()
                rw_timing = (dt.datetime.now() - dtRWStart).total_seconds()
                if DEBUG: print("rw_timing: {:5.3f}".format(rw_timing))
                dtKbdStart = dt.datetime.now()
                checkKbdForCmd(kbdWaitTime)
                kbd_timing = (dt.datetime.now() - dtKbdStart).total_seconds()
                if DEBUG: print("kbd_timing: {:5.3f}".format(kbd_timing))
                if kegpg.result == "exit":
                    print("kegpg.result == exit")
                    break
                # set loopSleep to make loop as close to the requested fps as possible
                loopSleep = ((1.0/fps)-rw_timing-kbdWaitTime) if ((1.0/fps) > (rw_timing+kbdWaitTime)) else 0.001
                if DEBUG: print("loopSleep: {:5.3}".format(loopSleep))
                sleep(loopSleep)



    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
            print("\n*** Ctrl-C detected - Finishing up")

    #except SystemExit:
    #        print("\n*** SIGTERM detected - Finishing up")

    finally:
        do_teardown()
        sleep(1)

    runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
