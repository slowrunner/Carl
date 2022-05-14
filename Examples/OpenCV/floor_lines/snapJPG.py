#!/usr/bin/python

# snapJPG.py  Takes single 320x240 resolution image
#             after 5 sec delay to set exposure
#             if argument - writes image to ./images/<arg>
#             otherwise writes image to ./images/capture_YYYYmmdd-HHMMSS.jpg

from picamera import PiCamera
from time import sleep
from datetime import datetime
import os
import sys

camera = PiCamera()
# camera.resolution = (2592, 1944)
camera.resolution = (320, 240)


sleep(5) # 0.25 good light, 5.0 when dark - allow picam to adjust exposure
args = sys.argv[1:]

if ( len(args) > 0 ):
    fname = "images/"+args[0]
else:
    fname = "images/capture_"+datetime.now().strftime("%Y%m%d-%H%M%S")+".jpg"

if not os.path.exists('images'):
    os.makedirs('images')

fn = camera.capture(fname)

print("Wrote image to {}".format(fname))

# if using HDMI monitor preview
# sleep(30)
# camera.stop_preview()

