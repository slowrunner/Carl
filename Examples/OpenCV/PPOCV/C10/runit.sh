#!/bin/bash

infile="/home/pi/Carl/Examples/PPOCV/images/coins.png"

./sobel_and_laplacian.py -i $infile
./canny.py -i $infile
