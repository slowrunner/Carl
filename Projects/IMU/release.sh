#!/bin/bash

echo "Release locals to Carl/plib"

fn=my_safe_inertial_measurement_unit.py
echo "Copying "$fn
cp $fn ~/Carl/plib

fn=my_inertial_measurement_unit.py
echo "Copying "$fn
cp $fn ~/Carl/plib

fn=myBNO055.py
echo "Copying "$fn
cp $fn ~/Carl/plib

fn="imulog.py"
echo "Copying "$fn
cp $fn ~/Carl/plib

echo "Release local readIMU.py to systests/imu"
fn="readIMU.py"
cp $fn ~/Carl/systests/imu


echo "Done"
