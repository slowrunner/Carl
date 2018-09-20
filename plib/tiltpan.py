#!/usr/bin/python
#
# tiltpan.py    Tilt and Pan Servo Management
#
# Pan Servo:  PAN_LEFT_LIMIT  = 0, PAN_CENTER  = 90, PAN_RIGHT_LIMIT = 180   (for GoPiGo3 servo compatibility)
# Tilt Servo: TILT_DOWN_LIMIT = -90, TILT_CENTER = 0, TILT_UP_LIMIT   = 90
#
# Methods:
#  tilt(pos = tilt_pos)
#  pan(pos = pan_pos)
#  tiltpan_center()       # convenience tilt(TILT_CENTER), pan(PAN_CENTER)
#  off()                  # turn both servos off / non-holding position
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
import easygopigo
import tiltpan

egpg = EasyGoPiGo3(use_mutex=True)  # protect so others can use also
ts = egpg.init_servo(TILT_PORT)
ps = egpg.init_servo(PAN_PORT)

tiltpan.tiltpan_center()
tiltpan.tilt(tiltpan.TILT_CENTER)  # -90 to +90
tiltpan.pan(tiltpan.PAN_CENTER)
print tiltpan.get_pan_pos(), tiltpan.get_tilt_pos()

```
"""

#
from __future__ import print_function
from __future__ import division

# import the modules

import sys
sys.path
sys.path.append('/home/pi/Carl/plib')

from time import sleep
import signal
import os
import myPyLib
import speak
from datetime import datetime
from math import sin,cos,radians

import easygopigo3

TILT_PORT = "SERVO2"
PAN_PORT  = "SERVO1"

PAN_LEFT_LIMIT = 0
PAN_RIGHT_LIMIT = 180
PAN_CENTER = 90

TILT_DOWN_LIMIT = -65
TILT_CENTER = 0
TILT_UP_LIMIT = 65

tilt_position = TILT_CENTER
pan_position  = PAN_CENTER

# #### Create a mutex protected instance of EasyGoPiGo3 base class
egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)

ts = egpg.init_servo(TILT_PORT)
ps = egpg.init_servo(PAN_PORT)

def get_tilt_pos():
   return tilt_position

def get_pan_pos():
   return pan_position

def tiltpan_center():
  global tilt_position,pan_position
  tilt_position = TILT_CENTER
  pan_position = PAN_CENTER
  tilt()
  sleep(0.5)  # delay to limit current draw, SG90 spec: 0.12 sec/60deg
  pan()

def off():          # turn both servo PWM freq to 0 to stop holding position
  global ts, ps
  ps.gpg.set_servo(ps.portID, 0)
  ts.gpg.set_servo(ts.portID, 0)

def tilt(tgt=tilt_position):
  global ts,tilt_position

  tilt_position = tgt
  if (tilt_position > TILT_UP_LIMIT):
      tilt_position = TILT_UP_LIMIT
      print("tilt(tgt) > TILT_UP_LIMIT")
  if (tilt_position < TILT_DOWN_LIMIT):
      tilt_position = TILT_DOWN_LIMIT
      print("tilt(tgt) < TILT_DOWN_LIMIT")
  ts.rotate_servo(-tilt_position+90)


def pan(tgt=pan_position):
  global ps,pan_position

  pan_position = tgt
  if (pan_position > PAN_RIGHT_LIMIT):
     pan_position = PAN_RIGHT_LIMIT
     print("pan(tgt) > PAN_RIGHT_LIMIT")
  if (pan_position < PAN_LEFT_LIMIT):
     pan_position = PAN_LEFT_LIMIT
     print("pan(tgt) < PAN_LEFT_LIMIT")
  ps.rotate_servo(180-pan_position)

def nod_yes(spd=0.03):
    NOD_UP_LIMIT = 20
    NOD_DN_LIMIT = -20
    TIMES_TO_NOD = 2
    for i in range(0,TIMES_TO_NOD):
        for angle in range(TILT_CENTER, NOD_UP_LIMIT+1, 5):
                tilt(angle)
                sleep(spd)
        for angle in range(NOD_UP_LIMIT, NOD_DN_LIMIT-1, -5):
                tilt(angle)
                sleep(spd)
        for angle in range(NOD_DN_LIMIT, TILT_CENTER+1, 5):
                tilt(angle)
                sleep(spd)
    tiltpan_center()

def nod_no(spd=0.02):
    NOD_LEFT_LIMIT = 70
    NOD_RIGHT_LIMIT = 110
    TIMES_TO_NOD = 2
    tiltpan_center()
    for i in range(0,TIMES_TO_NOD):
        for angle in range(PAN_CENTER, NOD_LEFT_LIMIT-1, -5):
                pan(angle)
                sleep(spd)
        for angle in range(NOD_LEFT_LIMIT, NOD_RIGHT_LIMIT+1, 5):
                pan(angle)
                sleep(spd)
        for angle in range(NOD_RIGHT_LIMIT, PAN_CENTER-1, -5):
                pan(angle)
                sleep(spd)
    tiltpan_center()

def nod_IDK(spd=0.02):
    for radius in range(30,60+1,30):
        for angle in range(0,360+1,2):
            tiltp =  int( radius * sin( radians(angle) ))
            panp  =  int( radius * cos( radians(angle) )) + 90
            tilt(tiltp)
            pan(panp)
            sleep(spd)
    tiltpan_center()

# ##### MAIN ######

def handle_ctlc():
  tiltpan_center()
  print("tiltpan.py: handle_ctlc() executed")

def main():
  global tilt_position, pan_position

  # #### SET CNTL-C HANDLER
  myPyLib.set_cntl_c_handler(handle_ctlc)


  try:
    while True:
        print("tiltpan centered")
        tiltpan_center()
        sleep(5)
        print("pan(45)")
        pan(45)
        sleep(5)
        print("pan(135)")
        pan(135)
        sleep(5)
        print("pan(PAN_CENTER)")
        pan(PAN_CENTER)
        print("tilt(45)")
        tilt(45)
        sleep(5)
        print("tilt(-45)")
        tilt(-45)
        sleep(5)
        print("tilt(TILT_CENTER)")
        tilt(TILT_CENTER)

        tiltpan_center()
        print("pan_position:",get_pan_pos() )
        print('UP too far')
        tilt(90)
        print("tilt_position:",get_tilt_pos() )
        sleep(5)
        print('DOWN too far')
        tilt(-90)
        print("tilt_position:",get_tilt_pos() )
        sleep(5)
        print("YES")
        nod_yes()
        sleep(2)
        print("NO")
        nod_no()
        sleep(2)
        print("IDK")
        nod_IDK()
        sleep(2)
        print("Turning tiltpan servos off")
        off()
        sleep(5)
    #end while
  except SystemExit:
    print("tiltpan.py: exiting")

if __name__ == "__main__":
    main()

