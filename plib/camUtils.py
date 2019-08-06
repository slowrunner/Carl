#!/usr/bin/python3

# camUtils.py

# snapJPG(fpath,fname,preview=False, lowlight=False, longexp=False)
#     Takes single full resolution image, 
#     after delay to set exposure (2s auto or 5s lowlight, 30s longexp)
#     defaults write image to /home/pi/Carl/images/capture_YYYYmmdd-HHMMSS.jpg

# captureOCV(x=640, y=480, lowlight=False)
#             Captures an OpenCV compatible (BGR) image to numpy array (y,x,3)
#             If lowlight is True, captures with increased brightness and contrast

# longExpOCV(x=640,y=480)
#     Captures a long exposure,  OpenCV compatible (BGR) image to a numpy array(y,x,3)
#     Forces sensor mode 3 (long exposure mode), framerate 1/6fps, shutterspeed 6s
#     ISO 800 (for max gain)

# fixTiltOCV(image)
#             retuns an OpenCV image array rotated to correct camera mount error from horizontal

# hAngle(targetPixel, hRes, hFOV=DEFAULT_H_FOV)
#             returns horizontal angle off center in degrees

# Full Resolution is per V1.3 camera board

# PiCamera v1.13 at present
from picamera import PiCamera
from time import sleep
from datetime import datetime
import cv2
import numpy as np
from fractions import Fraction
import sys
sys.path.append("/home/pi/Carl/plib")
import myimutils

CAM_TILT = 2.0  # 1.53
IMAGES_DIR = "/home/pi/Carl/images/"
DEFAULT_FNAME = "capture_YYYYMMDD-HHMMSS.jpg"
DEFAULT_H_FOV = 55.5

# Camera takes 200 frames to compute exposure, 
# office auto=1/15s exposure so 2-3s to settle
# longexp uses 1/6s framerate so 30s
LONGEXP_DELAY = 30  # let camera settle for good long time
LOWLIGHT_DELAY = 5
GOODLIGHT_DELAY = 2

# snapJPG(fpath,fname,preview=False, lowlight=False, longexp=False)
#     Takes single full resolution image,
#     after 5 sec delay to set exposure, (or 30s longexp)
#     defaults write image to /home/pi/Carl/images/capture_YYYYmmdd-HHMMSS.jpg
#     longexp takes 6s capture at ISO 800

def snapJPG(fpath=IMAGES_DIR,fname=DEFAULT_FNAME, preview=False, lowlight=False, longexp=False):
    if longexp:
        camera = PiCamera(
            resolution=(2592, 1944),
            framerate=Fraction(1, 6),
            sensor_mode=3)
        camera.shutter_speed = 6 * 1000000  # micro seconds
        camera.iso = 800
        camera.awb_mode = 'incandescent'
        print("snapJPG(longexp) {}s settling delay".format(LONGEXP_DELAY))
        sleep(LONGEXP_DELAY)
        camera.exposure_mode = 'off'
    else:
        camera = PiCamera()
        camera.resolution = (2592, 1944)
        if lowlight:
            camera.brightness = 70  # default 50
            camera.contrast = 60    # default 0
        camera.sharpness = 75       # default 0
        camera.awb_mode = 'incandescent'
        if lowlight:
            sleep(LOWLIGHT_DELAY) # 0.25 good light, 5.0 when dark - allow picam to adjust exposure
        else: sleep(GOODLIGHT_DELAY)

    # if have HDMI monitor hooked up
    if preview: camera.start_preview()
    if fname == DEFAULT_FNAME:
        fname = "capture_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
    fullPath = IMAGES_DIR + fname
    print("snapJPG: capturing image now")
    fn = camera.capture(fullPath)
    print("snapJPG: capture done")

    # if using HDMI monitor preview
    if preview:
        sleep(30)
        camera.stop_preview()
    # bug in picamera https://github.com/waveform80/picamera/issues/528
    if longexp:
        camera.framerate = 1  # workaround
        sleep(2)
    camera.close()
    if longexp: print("snapJPB(): long exposure camera.close() succeeded")
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
        if lowlight: 
            sleep(LOWLIGHT_DELAY)
        else:
            sleep(GOODLIGHT_DELAY)
        image = np.empty((y * x * 3,), dtype=np.uint8)
        camera.capture(image, 'bgr')
        image = image.reshape((y, x, 3))
        camera.close()     # theorhetically not needed for "with PiCamera()" construct
    return image

# longExpOCV(x=640, y=480)
#     Captures a long exposure,  OpenCV compatible (BGR) image to a numpy array(y,x,3)
#     Forces sensor mode 3 (long exposure mode), framerate 1/6fps, shutterspeed 6s
#     ISO 800 (for max gain)

def longExpOCV(x=640,y=480):
    camera = PiCamera(
        resolution=(x,y),
        framerate=Fraction(1, 6),
        sensor_mode=3)
    camera.shutter_speed = 6000000
    camera.iso = 800
    camera.awb_mode = 'incandescent'

    # Give the camera a good long time to set gains
    print("longExpOCV: delay {}s for camera to settle".format(LONGEXP_DELAY))
    sleep(LONGEXP_DELAY)
    camera.exposure_mode = 'off'
    # Now capture an image with a 6s exposure. (takes longer than 6s)
    print("Capturing Long Exposure Still Image Now")
    image = np.empty((y * x * 3,), dtype=np.uint8)
    camera.capture(image, 'bgr')
    image = image.reshape((y, x, 3))
    # bug in picamera https://github.com/waveform80/picamera/issues/528
    camera.framerate = 1    # workaround
    sleep(2)
    camera.close()
    print("longExpOCV(): camera.close() succeeded")
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

    longExpFname = "longExp_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
    print("Testing snapJPG(longexp=True)")
    fpath = snapJPG(fname=longExpFname,longexp=True)
    print("snapJPG() wrote ", fpath)

    print("Testing captureOCV() and fixTilt()")
    image = captureOCV()
    cv2.imshow("captureOCV() image",image)

    image2 = captureOCV(lowlight=True)
    cv2.imshow("captureOCV(lowlight=True) image",image2)
    print("image2 shape [y,x]", image2.shape[:2])
    sleep(2)

    image3 = fixTiltOCV(image2)
    print("fixTilt() image shape [y,x]", image3.shape[:2])
    cv2.imshow("fixTiltOCV() applied", image3)


    print("Testing longExpOCV()")
    image4 = longExpOCV()
    # myimutils.display("longExpOCV() image",image4,scale_percent=50)
    cv2.imshow("longExpOCV() image",image4)


    cv2.waitKey(0)


if (__name__ == "__main__"): main()

