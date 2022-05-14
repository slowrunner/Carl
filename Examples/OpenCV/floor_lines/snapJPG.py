#!/usr/bin/python

# snapJPG.py  Takes single full resolution image
#             after 5 sec delay to set exposure
#             writes image to ./images/capture_YYYYmmdd-HHMMSS.jpg

from picamera import PiCamera
from time import sleep
from datetime import datetime
import os


camera = PiCamera()
# camera.resolution = (2592, 1944)
camera.resolution = (320, 240)


sleep(5) # 0.25 good light, 5.0 when dark - allow picam to adjust exposure
fname = "images/capture_"+datetime.now().strftime("%Y%m%d-%H%M%S")+".jpg"

if not os.path.exists('images'):
    os.makedirs('images')

fn = camera.capture(fname)

# if using HDMI monitor preview
# sleep(30)
# camera.stop_preview()

