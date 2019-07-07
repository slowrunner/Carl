#!/usr/bin/python3

# camUtils.py

# snapJPG()   Takes single full resolution image
#             after 5 sec delay to set exposure
#             writes image to /home/pi/Carl/images/capture_YYYYmmdd-HHMMSS.jpg

from picamera import PiCamera
from time import sleep
from datetime import datetime


def snapJPG():
    camera = PiCamera()
    camera.resolution = (2592, 1944)

    # if have HDMI monitor hooked up
    # camera.start_preview()

    sleep(5) # 0.25 good light, 5.0 when dark - allow picam to adjust exposure
    fname = "/home/pi/Carl/images/capture_"+datetime.now().strftime("%Y%m%d-%H%M%S")+".jpg"
    fn = camera.capture(fname)

    # if using HDMI monitor preview
    # sleep(30)
    # camera.stop_preview()
    camera.close()
    return fname

def main():
    print("Testing snapJPG()")
    fname = snapJPG()
    print("snapJPG() wrote ", fname)

if (__name__ == "__main__"): main()

