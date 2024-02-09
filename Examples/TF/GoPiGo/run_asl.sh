#!/bin/bash

python3 gpg_asl_picamera.py  \
 --model /home/pi/Carl/Examples/TF/models/ASL.tflite \
 --labels /home/pi/Carl/Examples/TF/models/labels_ASL.txt \
 --preview n \
 --confidence 0.6 \
 --save y




