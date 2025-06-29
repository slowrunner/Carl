#!/bin/bash

python3 gpg_classify_picamera.py  \
 --model /home/pi/Carl/Examples/TF/models/mobilenet_v1_1.0_224_quant.tflite \
 --labels /home/pi/Carl/Examples/TF/models//labels_mobilenet_quant_v1_224.txt \
 --preview y \
 --confidence 0.6 \
 --save n




