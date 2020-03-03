#!/bin/bash


infile="/home/pi/Carl/Examples/OpenCV/PPOCV/images/coins_03.png"
infile1="/home/pi/Carl/Examples/OpenCV/PPOCV/images/coins.png"
infile2="/home/pi/Carl/Examples/OpenCV/PPOCV/images/skateboard_decks.png"
infile4="/home/pi/Carl/Examples/OpenCV/PPOCV/images/coins_02.png"
infile5="/home/pi/Carl/Examples/OpenCV/PPOCV/images/coins_02.png"
infile6="/home/pi/Carl/Examples/OpenCV/PPOCV/images/pills_01.png"
infile7="/home/pi/Carl/Examples/OpenCV/PPOCV/images/pills_02.png"
./contour_only.py -i $infile
./adaptive_threshold.py -i $infile1
./otsu_and_riddler.py -i $infile1
./threshold.py --image $infile2 --threshold 245
./watershed.py -i $infile4
./watershed.py -i $infile5
./watershed.py -i $infile6
./watershed.py -i $infile7
