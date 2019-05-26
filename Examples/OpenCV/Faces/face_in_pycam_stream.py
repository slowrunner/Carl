#!/usr/bin/env python3
#
# face_in_image.py

"""
Documentation:
    Based on rpi.blogspot.com/2015/03/face-detection-with-raspberry-pi.html

    To get opencv/data/ files:
        cd ~/Carl/Examples/OpenCV/
        wget https://github.com/opencv/opencv/archive/3.4.4.zip
        unzip *.zip

    data is in ~/Carl/Examples/OpenCV/opencv-3.4.4/data

    loop time about 1 to 1.5 seconds at 320x240 or 640x480 

"""

# from __future__ import print_function # use python 3 syntax but make it compatible with python 2
# from __future__ import division       #                           ''

import sys
try:
    sys.path.append('/home/pi/Carl/plib')
    import speak
    import tiltpan
    import status
    import battery
    import myDistSensor
    import lifeLog
    import myconfig
    import myimutils   # display(windowname, image, scale_percent=30)
    Carl = True
except:
    Carl = False
import easygopigo3 # import the EasyGoPiGo3 class
import numpy as np
import datetime as dt
import argparse
from time import sleep

import cv2
import picamera
import io
import datetime
# ARGUMENT PARSER
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True, help="path to input file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
#args = vars(ap.parse_args())
# print("Started with args:",args)


# CONSTANTS


# VARIABLES


# METHODS

def detect_faces(image_in):
    image_copy = image_in.copy()
    image_gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier("/home/pi/Carl/Examples/OpenCV/opencv-3.4.4/data/haarcascades/haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in faces:
        cv2.rectangle(image_copy, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return image_copy,faces


# MAIN

def main():
    if Carl: lifeLog.logger.info("Started")
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    if Carl:
        myconfig.setParameters(egpg)
        tiltpan.tiltpan_center()
        sleep(0.5)
        tiltpan.off()

    try:

        keepLooping = True
        while keepLooping:
            # Create memory stream 
            stream = io.BytesIO()


            # capture a frame from camera to the streem
            with picamera.PiCamera() as camera:
                # camera.resolution = (320, 240)
                camera.resolution = (640, 480)
                camera.capture(stream, format='jpeg')

            frame_time = datetime.datetime.now().strftime("%H:%M:%S.%f")[:12]

            # convert pic into numpy array
            buff = np.fromstring(stream.getvalue(), dtype=np.uint8)

            # create an OpenCV image
            image = cv2.imdecode(buff, 1)

            #myimutils.display("input",image)
            #cv2.waitKey(0)

            face_set = detect_faces(image)
            # myimutils.display("faces()", face_set[0],50 )  # 640x480 images
            cv2.imshow("faces()", face_set[0])
            print("{}: faces() found {} faces".format(frame_time,len(face_set[1])))
            for (x, y, w, h) in face_set[1]:
                print("    {}x{} face at ({},{})".format(h,w,x,y))

            # wait time in ms: 500 to limit load, 1 to go as fast as possible (1 detect / sec)
            k = cv2.waitKey(1)
            if (k == 27):
                keepLooping = False
                cv2.destroyAllWindows()


    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: lifeLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
