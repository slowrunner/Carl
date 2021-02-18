#!/usr/bin/python3
#
# tiltpan.py    Tilt and Pan Servo Management Class
#
# Pan Servo:  PAN_LEFT_LIMIT  = 0, PAN_CENTER  = 90, PAN_RIGHT_LIMIT = 180   (for GoPiGo3 servo compatibility)
# Tilt Servo: TILT_DOWN_LIMIT = -90, TILT_CENTER = 0, TILT_UP_LIMIT   = 90
#
# Methods:
#  TiltPan(egpg)          # creates class object
#  tilt(pos = tilt_pos)
#  pan(pos = pan_pos)
#  tiltpan_center()       # convenience tilt(TILT_CENTER), pan(PAN_CENTER)
#  center()               # same as tiltpan_center()
#  off()                  # turn both servos off / non-holding position (sets pos to UNKNOWN)
#  nod_yes(spd=0.03)
#  nod_no(spd=0.02)
#  nod_IDK(spd=0.02)
#  get_tilt_pos()
#  get_pan_pos()
#
#
"""
```
# Usage:

import tiltpan
import easygopigo3
import myconfig

egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
myconfig.setParameters(egpg)

tp = tiltpan.TiltPan(egpg)

tp.tiltpan_center()
tp.tilt(tiltpan.TILT_CENTER)  # -90 to +90
tp.pan(tiltpan.PAN_CENTER)
print tp.get_pan_pos(), tp.get_tilt_pos()
tp.tiltpan.off()

```
"""

#
from __future__ import print_function
from __future__ import division

# import the modules

import sys
sys.path
sys.path.append('/home/pi/Carl/plib')
import runLog

from time import sleep
import signal
import os
import myPyLib
import speak
from datetime import datetime
from math import sin,cos,radians
import myconfig
import easygopigo3

TILT_PORT = "SERVO2"
PAN_PORT  = "SERVO1"

PAN_LEFT_LIMIT = 0
PAN_RIGHT_LIMIT = 180
PAN_CENTER = 90

TILT_DOWN_LIMIT = -65
TILT_CENTER = 0
TILT_UP_LIMIT = 65

UNKNOWN = 999

class TiltPan():
    tilt_position = TILT_CENTER
    pan_position  = PAN_CENTER
    ts = None
    ps = None
    def __init__(self, egpg):
        TiltPan.ts = egpg.init_servo(TILT_PORT)
        TiltPan.ps = egpg.init_servo(PAN_PORT)

    def get_tilt_pos(self):
        return TiltPan.tilt_position

    def get_pan_pos(self):
       return TiltPan.pan_position

    def tiltpan_center(self):
      TiltPan.tilt_position = TILT_CENTER
      TiltPan.pan_position = PAN_CENTER
      self.tilt()
      sleep(0.25)  # delay to limit current draw, SG90 spec: 0.12 sec/60deg
      self.pan()
      sleep(0.25)  # delay to ensure action incase next method is off()

    def center(self):
      self.tiltpan_center()

    def off(self):          # turn both servo PWM freq to 0 to stop holding position
      TiltPan.ps.gpg.set_servo(TiltPan.ps.portID, 0)
      TiltPan.ts.gpg.set_servo(TiltPan.ts.portID, 0)
      # With the servos off, the position may change without command
      # TiltPan.tilt_position = UNKNOWN
      # TiltPan.pan_position = UNKNOWN

    def tilt(self,tgt=None):
      if tgt != None: TiltPan.tilt_position = tgt
      if (TiltPan.tilt_position > TILT_UP_LIMIT):
          TiltPan.tilt_position = TILT_UP_LIMIT
          print("tilt(tgt) > TILT_UP_LIMIT")
      if (TiltPan.tilt_position < TILT_DOWN_LIMIT):
          TiltPan.tilt_position = TILT_DOWN_LIMIT
          print("tilt(tgt) < TILT_DOWN_LIMIT")
      TiltPan.ts.rotate_servo(-TiltPan.tilt_position+90)


    def pan(self,tgt=None):
      if tgt != None: TiltPan.pan_position = tgt
      if (TiltPan.pan_position > PAN_RIGHT_LIMIT):
         TiltPan.pan_position = PAN_RIGHT_LIMIT
         print("pan(tgt) > PAN_RIGHT_LIMIT")
      if (TiltPan.pan_position < PAN_LEFT_LIMIT):
         TiltPan.pan_position = PAN_LEFT_LIMIT
         print("pan(tgt) < PAN_LEFT_LIMIT")
      TiltPan.ps.rotate_servo(180-TiltPan.pan_position)

    def nod_yes(self,spd=0.03):
        NOD_UP_LIMIT = 20
        NOD_DN_LIMIT = -20
        TIMES_TO_NOD = 2
        for i in range(0,TIMES_TO_NOD):
            for angle in range(TILT_CENTER, NOD_UP_LIMIT+1, 5):
                    self.tilt(angle)
                    sleep(spd)
            for angle in range(NOD_UP_LIMIT, NOD_DN_LIMIT-1, -5):
                    self.tilt(angle)
                    sleep(spd)
            for angle in range(NOD_DN_LIMIT, TILT_CENTER+1, 5):
                    self.tilt(angle)
                    sleep(spd)
        self.tiltpan_center()

    def nod_no(self,spd=0.02):
        NOD_LEFT_LIMIT = 70
        NOD_RIGHT_LIMIT = 110
        TIMES_TO_NOD = 2
        self.tiltpan_center()
        for i in range(0,TIMES_TO_NOD):
            for angle in range(PAN_CENTER, NOD_LEFT_LIMIT-1, -5):
                    self.pan(angle)
                    sleep(spd)
            for angle in range(NOD_LEFT_LIMIT, NOD_RIGHT_LIMIT+1, 5):
                    self.pan(angle)
                    sleep(spd)
            for angle in range(NOD_RIGHT_LIMIT, PAN_CENTER-1, -5):
                    self.pan(angle)
                    sleep(spd)
        self.tiltpan_center()

    def nod_IDK(self,spd=0.02):
        for radius in range(30,60+1,30):
            for angle in range(0,360+1,2):
                tiltp =  int( radius * sin( radians(angle) ))
                panp  =  int( radius * cos( radians(angle) )) + 90
                self.tilt(tiltp)
                self.pan(panp)
                sleep(spd)
        self.tiltpan_center()



# ##### MAIN ######

def handle_ctlc():
  global tp
  tp.tiltpan_center()
  print("tiltpan.py: handle_ctlc() executed")

@runLog.logRun
def main():
  global tp
  try:
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    tp = TiltPan(egpg)
    # #### SET CNTL-C HANDLER
    myPyLib.set_cntl_c_handler(handle_ctlc)

    while True:
        print("tiltpan centered")
        tp.tiltpan_center()
        sleep(5)
        print("pan(45)")
        tp.pan(45)
        sleep(5)
        print("pan(135)")
        tp.pan(135)
        sleep(5)
        print("pan(PAN_CENTER)")
        tp.pan(PAN_CENTER)
        print("tilt(45)")
        tp.tilt(45)
        sleep(5)
        print("tilt(-45)")
        tp.tilt(-45)
        sleep(5)
        print("tilt(TILT_CENTER)")
        tp.tilt(TILT_CENTER)

        tp.tiltpan_center()
        print("pan_position:",tp.get_pan_pos() )
        print('UP too far')
        tp.tilt(90)
        print("tilt_position:",tp.get_tilt_pos() )
        sleep(5)
        print('DOWN too far')
        tp.tilt(-90)
        print("tilt_position:",tp.get_tilt_pos() )
        sleep(5)
        print("YES")
        tp.nod_yes()
        sleep(2)
        print("NO")
        tp.nod_no()
        sleep(2)
        print("IDK")
        tp.nod_IDK()
        sleep(2)
        print("Turning tiltpan servos off")
        tp.off()
        sleep(5)
        print("tilt_position(999=UNKNOWN):",tp.get_tilt_pos() )
        print("pan_position (999=UNKNOWN):",tp.get_pan_pos() )
    #end while
  except SystemExit:
    print("tiltpan.py: exiting")

if __name__ == "__main__":
    main()

