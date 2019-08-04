#!/usr/bin/python3

# imports

import sys
sys.path.append("/home/pi/Carl/plib")

import camUtils
import time
import cv2

try:
    while True:
        print("Testing captureOCV() and fixTilt()")
        image = camUtils.captureOCV(lowlight=True)
        image = camUtils.fixTiltOCV(image)
        print("fixTilt() image shape [y,x]", image.shape[:2])
        cv2.imshow("fixTiltOCV() applied", image)
        cv2.waitKey(1)

except KeyboardInterrupt:
    print("\n*** ^C Detected - Finishing up")
    time.sleep(1)
