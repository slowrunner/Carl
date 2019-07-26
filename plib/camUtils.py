#!/usr/bin/python3

# camUtils.py

# snapJPG()   Takes single full resolution image
#             after 5 sec delay to set exposure
#             writes image to /home/pi/Carl/images/capture_YYYYmmdd-HHMMSS.jpg

# captureOCV(x=640, y=480, lowlight=False)
#             Captures an OpenCV compatible (BGR) image to numpy array (y,x,3)
#             If lowlight is True, captures with increased brightness and contrast

# fixTiltOCV(image)
#             retuns an OpenCV image array rotated to correct camera mount error from horizontal

# hAngle(targetPixel, hRes, hFOV=DEFAULT_H_FOV)
#             returns horizontal angle off center in degrees

from picamera import PiCamera
from time import sleep
from datetime import datetime
import cv2
import numpy as np

CAM_TILT = 2.0  # 1.53
IMAGES_DIR = "/home/pi/Carl/images/"
DEFAULT_FNAME = "capture_YYYYMMDD-HHMMSS.jpg"
DEFAULT_H_FOV = 55.5

# snapJPG()   Takes single full resolution image
#             after 5 sec delay to set exposure
#             writes image to /home/pi/Carl/images/capture_YYYYmmdd-HHMMSS.jpg

def snapJPG(fpath=IMAGES_DIR,fname=DEFAULT_FNAME, preview=False, lowlight=False):
    camera = PiCamera()
    camera.resolution = (2592, 1944)
    if lowlight:
        camera.brightness = 70  # default 50
        camera.contrast = 60    # default 0
    camera.sharpness = 75       # default 0
    camera.awb_mode = 'incandescent'

    # if have HDMI monitor hooked up
    if preview: camera.start_preview()

    sleep(5) # 0.25 good light, 5.0 when dark - allow picam to adjust exposure
    if fname == DEFAULT_FNAME:
        fname = "capture_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
    fullPath = IMAGES_DIR + fname
    fn = camera.capture(fullPath)

    # if using HDMI monitor preview
    if preview:
        sleep(30)
        camera.stop_preview()
    camera.close()
    return fullPath

# captureOCV(x=640, y=480, lowlight=False)
#             Captures an OpenCV compatible (BGR) image to numpy array (y,x,3)
#             If lowlight is True, captures with increased brightness and contrast

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

# fixTiltOCV(image)
#             retuns an OpenCV image array rotated to correct camera mount error from horizontal

def fixTiltOCV(image):
    # Note: extra pixels will be black
    (h,w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, CAM_TILT, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

# hAngle(targetPixel, hRes, hFOV=DEFAULT_H_FOV)
#             returns horizontal angle off center in degrees
def hAngle(targetPixel, hRes, hFOV=DEFAULT_H_FOV):
    Base = (hRes/2) / np.tan( np.deg2rad( hFOV/2 ))
    dCtr = targetPixel - (hRes // 2)
    leftRight = np.sign(dCtr)    # negative = left, positive = right of center
    xAngle = np.rad2deg( np.arctan( abs(dCtr) / Base ))
    return (leftRight * xAngle)

def main():

    print("Testing hAngle(targetPixel=480, hRes=640, hFOV=DEFAULT_H_FOV)")
    degOffCtr = hAngle(480,640,DEFAULT_H_FOV)
    print("result: {:.1f}".format(degOffCtr))

    print("Testing hAngle(targetPixel=0, hRes=640, hFOV=DEFAULT_H_FOV)")
    degOffCtr = hAngle(0,640,DEFAULT_H_FOV)
    print("result: {:.1f}".format(degOffCtr))

    print("Testing hAngle(targetPixel=320, hRes=640, hFOV=DEFAULT_H_FOV)")
    degOffCtr = hAngle(320,640,DEFAULT_H_FOV)
    print("result: {:.1f}".format(degOffCtr))


    print("Testing snapJPG()")
    fname = snapJPG()
    print("snapJPG() wrote ", fname)

    lowlightFname = "lowlight_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
    print("Testing snapJPG(lowlight=True)")
    fpath = snapJPG(fname=lowlightFname,lowlight=True)
    print("snapJPG() wrote ", fpath)


    print("Testing captureOCV() and fixTilt()")
    image = captureOCV()
    cv2.imshow("captureOCV() image",image)

    image2 = captureOCV(lowlight=True)
    cv2.imshow("captureOCV(lowlight=True) image",image2)
    print("image2 shape [y,x]", image2.shape[:2])

    image3 = fixTiltOCV(image2)
    print("fixTilt() image shape [y,x]", image3.shape[:2])
    cv2.imshow("fixTiltOCV() applied", image3)

    cv2.waitKey(0)


if (__name__ == "__main__"): main()

