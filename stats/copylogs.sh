#!/bin/bash

# Copies the active logs to stats directory with .year.n extension

year=7

# ../imu.log  ../life.log  ../run.log  ../speak.log  ../voice.log  ../wheel.log
../totallife.sh
cp ../life.log life.log.year.$year
# cp ../imu.log imu.log.year.$year
cp ../run.log run.log.year.$year
cp ../speak.log speak.log.year.$year
cp ../voice.log voice.log.year.$year
cp ../wheel.log wheel.log.year.$year
