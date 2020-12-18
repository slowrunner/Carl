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

# ARGUMENT PARSER
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
args = vars(ap.parse_args())
# print("Started with args:",args)


# CONSTANTS
cv2_data = cv2.data
print("Using OpenCV Data from ",cv2_data)

# VARIABLES


# METHODS

def detect_faces(image_in):
    image_copy = image_in.copy()
    image_gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2_data+"haarcascades/haarcascade_frontalface_default.xml")
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
        image_orig = cv2.imread(args["image"], 1)

        # test effect of smaller images (detect takes 3s on fullsize, <1s for 640x480)
        import imutils
        image = imutils.resize(image_orig,640,480)

        myimutils.display("input",image)
        cv2.waitKey(0)

        print(cv2.data.haarcascades)  # but the data files are missing


        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Load a cascade file for detecting faces

        # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        # face_cascade = cv2.CascadeClassifier()
        # face_cascade.load('haarcascade_frontalface_default.xml')

        # full size: face1,3,4 good, face2 finds face and false face in floor
        # 640x480: face1,3,4 good, face2.jpg finds face and false face in floor
        face_cascade = cv2.CascadeClassifier("/home/pi/Carl/Examples/OpenCV/opencv-3.4.4/data/haarcascades/haarcascade_frontalface_default.xml")

        # 640x480: finds in face1 and face2.jpg, fails face3 and face4
        # fullsize:fails face1, ok in face2.jpg,face3 and 4
        # face_cascade = cv2.CascadeClassifier("/home/pi/Carl/Examples/OpenCV/opencv-3.4.4/data/lbpcascades/lbpcascade_frontalface.xml")

        # full size: finds face in face1, 2, 3, and 4
        # 640x480: finds face1, fails face2, 3, 4
        # face_cascade = cv2.CascadeClassifier("/home/pi/Carl/Examples/OpenCV/opencv-3.4.4/data/lbpcascades/lbpcascade_frontalface_improved.xml")

        # Look for faces in the image using the loaded cascade file
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        print("Found " + str(len(faces)) + " face(s) in resized image")

        # make a copy to draw on
        found = image
        # Draw a rectangle around every face found
        for (x,y,w,h) in faces:
             cv2.rectangle(found,(x,y),(x+w,y+h),(255,0,0),2)

        # Save the result image
        # cv2.imwrite('faces_in_image_output.jpg',found)

        myimutils.display("faces", found)

        face_set = detect_faces(image_orig)
        myimutils.display("faces()", face_set[0] )
        print("faces() found {} faces".format(len(face_set[1])))
        for (x, y, w, h) in face_set[1]:
            print("    {}x{} face at ({},{})".format(h,w,x,y))

        k = cv2.waitKey(0)
        if k == 27:    # Esc to kill everything
            cv2.destroyAllWindows()



    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: lifeLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
