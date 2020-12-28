#!/bin/bash

mkdir EasyPiCamSensor
cp *.py EasyPiCamSensor
cp README.md EasyPiCamSensor
cp Target_Colors.pdf EasyPiCamSensor
tar -zcvf EasyPiCamSensor.tgz EasyPiCamSensor
rm -r EasyPiCamSensor
echo "done"
