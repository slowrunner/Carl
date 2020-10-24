#!/bin/bash

cp life.log life.log.backup
cp wheel.log wheel.log.backup
cp imu.log imu.log.backup
cp run.log run.log.backup
cp carlData.json carlData.json.backup
echo "backed up life, wheel, imu, run logs and carlData.json"
ls -al *.backup

