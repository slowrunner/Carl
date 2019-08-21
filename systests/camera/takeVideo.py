#!/usr/bin/python

# snapJPG.py  Takes single full resolution image
#             after 5 sec delay to set exposure
#             writes image to ./images/capture_YYYYmmdd-HHMMSS.jpg

from picamera import PiCamera
from time import sleep
from datetime import datetime

VIDEO_LENGTH = 10 # seconds
HRES = 640
VRES = 480
WAIT_TIME = 5

camera = PiCamera()
camera.resolution = (HRES, VRES)

print("Waiting {}s for camera to settle".format(WAIT_TIME))
sleep(WAIT_TIME) # 0.25 good light, 5.0 when dark - allow picam to adjust exposure
fname = "videos/video_"+datetime.now().strftime("%Y%m%d-%H%M%S")+".h264"
fn = camera.start_recording(fname)
camera.wait_recording(VIDEO_LENGTH)
camera.stop_recording
print("{}s {}x{} video saved to {}".format(VIDEO_LENGTH, HRES, VRES, fname))

