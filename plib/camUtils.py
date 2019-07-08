#!/usr/bin/python3

# camUtils.py

# snapJPG()   Takes single full resolution image
#             after 5 sec delay to set exposure
#             writes image to /home/pi/Carl/images/capture_YYYYmmdd-HHMMSS.jpg

from picamera import PiCamera
from time import sleep
from datetime import datetime
import cv2
import numpy as np

CAM_TILT = 2.0  # 1.53

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

def captureOCV(x=640, y=480, lowlight=False):
    with PiCamera() as camera:
        camera.resolution = (x,y)
        camera.framerate = 24
        if lowlight:
            camera.brightness = 70  # default 50
            camera.contrast = 60    # default 0
        camera.sharpness = 75   # default 0
        camera.awb_mode = 'incandescent'
        sleep(2)
        image = np.empty((y * x * 3,), dtype=np.uint8)
        camera.capture(image, 'bgr')
        image = image.reshape((y, x, 3))
        camera.close()
    return image

def fixTilt(image):
    # Note: extra pixels will be black
    (h,w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, CAM_TILT, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def main():
    print("Testing snapJPG()")
    fname = snapJPG()
    print("snapJPG() wrote ", fname)

    print("Testing captureOCV() and fixTilt()")
    image = captureOCV()
    cv2.imshow("captureOCV() image",image)
    image2 = captureOCV(lowlight=True)
    cv2.imshow("captureOCV(lowlight=True) image",image2)
    print("image2 shape [y,x]", image2.shape[:2])
    image3 = fixTilt(image2)
    print("fixTilt() image shape [y,x]", image3.shape[:2])
    cv2.imshow("fixTilt() applied", image3)
    cv2.waitKey(0)

if (__name__ == "__main__"): main()

