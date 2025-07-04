#!/usr/bin/env python3
#
# myrobot.py

"""
Documentation:

Test if class vars are per process or not (hint:  per process)

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

#import cv2

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


# VARIABLES


# METHODS

# CLASSES

class RobotBaseClass():

    ROBOTBASECLASS_VAR = 123

    def __init__(self):
        print("RobotBaseClass.init() executed")

    def robotBaseClassMethod(self):
        print("robotBaseClassMethod() executed")

    def getRobotBaseClassVar(self):
        print("{}.getRobotBaseClassVar() executed".format(self.instanceName))
        return RobotBaseClass.ROBOTBASECLASS_VAR

    def setRobotBaseClassVar(self, value):
        print("{}.setRobotBaseClassVar({}) executed".format(self.instanceName,value))
        RobotBaseClass.ROBOTBASECLASS_VAR = value

class MyRobot(RobotBaseClass):
    classVar1 = -999

    def __init__(self,instance="default"):
        print("MyRobot.init({}) executed".format(instance))
        self.instanceName = instance

    def myRobotMethod(self):
        print("{}.myRobotMethod() executed".format(self.instanceName))

    def setClassVar1(self,value):
        MyRobot.classVar1 = value
        print("{}.setClassVar1({}) executed".format(self.instanceName,value))

    def getClassVar1(self):
        print("{}.getClassVar1() executed".format(self.instanceName))
        return MyRobot.classVar1


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
        # Do Somthing in a Loop
        loopSleep = 1 # second
        loopCount = 0
        keepLooping = False
        while keepLooping:
            loopCount += 1
            # do something
            sleep(loopSleep)

        # Do Something Once
        myrobot1 = MyRobot("myrobot1")
        myrobot2 = MyRobot("myrobot2")
        print("myrobot1.instanceName:",myrobot1.instanceName)
        print("myrobot2.instanceName:",myrobot2.instanceName)

        print("myrobot1.getClassVar1():",myrobot1.getClassVar1())
        print("myrobot2.getClassVar1():",myrobot2.getClassVar1())
        myrobot1.setClassVar1(1000)
        print("myrobot1.getClassVar1():",myrobot1.getClassVar1())
        print("myrobot2.getClassVar1():",myrobot2.getClassVar1())

        print("myrobot1.getRobotBaseClassVar():",myrobot1.getRobotBaseClassVar())
        print("myrobot2.getRobotBaseClassVar():",myrobot2.getRobotBaseClassVar())
        myrobot2.setRobotBaseClassVar(456)
        print("myrobot1.getRobotBaseClassVar():",myrobot1.getRobotBaseClassVar())
        print("myrobot2.getRobotBaseClassVar():",myrobot2.getRobotBaseClassVar())

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
