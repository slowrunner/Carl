#!/bin/bash

cp life.log life.log.backup
cp wheel.log wheel.log.backup
cp imu.log imu.log.backup
cp run.log run.log.backup
echo "backed up life, wheel, imu, and run logs"
ls -al *.backup

