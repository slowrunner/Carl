#!/usr/bin/python
#
# tiltpan.py    Tilt and Pan Servo Management
#
# Pan Servo:  PAN_LEFT_LIMIT  = 0, PAN_CENTER  = 90, PAN_RIGHT_LIMIT = 180
# Tilt Servo: TILT_DOWN_LIMIT = 0, TILT_CENTER = 90, TILT_UP_LIMIT   = 180
#
# Methods:
#  tilt(pos = tilt_pos)
#  pan(pos = pan_pos)
#  tiltpan_center()       # convenience tilt(TILT_CENTER), pan(PAN_CENTER)

```
# Usage:
import easygopigo
import tiltpan

egpg = EasyGoPiGo3(mutex=True)  # protect so others can use also
ts = egpg.init_servo(TILT_PORT, use_mutex=True)
ps = egpg.init_servo(PAN_PORT, use_mutex=True)

tiltpan_center()
```

#
# from __future__ import print_function
from __future__ import division

# import the modules

import sys
sys.path
sys.path.append('/home/pi/Carl/plib')

import time
import signal
import os
import myPyLib
import speak
from datetime import datetime
import easygopigo3

TILT_PORT = "SERVO2"
PAN_PORT  = "SERVO1"

PAN_LEFT_LIMIT = 0
PAN_RIGHT_LIMIT = 180
PAN_CENTER = 90
TILT_DOWN_LIMIT = 0
TILT_CENTER = 90
TILT_UP_LIMIT = 180

tilt_position = TILT_CENTER
pan_position  = PAN_CENTER

# #### Create a mutex protected instance of EasyGoPiGo3 base class 
egpg = easygopigo3.EasyGoPiGo3(mutex=True)

ts = egpg.init_servo(TILT_PORT, use_mutex=True)
ps = egpg.init_servo(PAN_PORT, use_mutex=True)

tiltpan_center()

def tilt(tgt=tilt_position):
  global ts

  tilt_position = tgt
  ts.rotate_servo(tilt_position)


def pan(tgt=pan_position):
  global ps

  pan_position = tgt
  ps.rotate_servo(pan_position)

# ##### MAIN ######

def handle_ctlc():
  print "tiltpan.py: handle_ctlc() executed"

def main():

  # #### SET CNTL-C HANDLER 
  myPyLib.set_cntl_c_handler(handle_ctlc)


  try:
    while True:
        tiltpan_center()
        for angle in range(TILT_DOWN_LIMIT, TILT_UP_LIMIT+1, 5):
                tilt(angle)
                time.sleep(0.2)
        tiltpan_center()
        for angle in range(PAN_LEFT_LIMIT, PAN_RIGHT_LIMIT+1, 5):
                pan(angle)
                time.sleep(0.2)
        tiltpan_center()
        for radius in range(20,60+1,20):
            for angle in range(0,360+1,5):
                tilt_position =  range * sin( radians(angle) ) + 90
                pan_position  =  range * cos( radians(angle) ) + 90
                tilt()
                pan()
                time.sleep(0.2)
    #end while
  except SystemExit:
    print "tiltpan.py: exiting"

if __name__ == "__main__":
    main()

