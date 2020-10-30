#!/bin/bash

cp life.log.backup life.log
cp wheel.log.backup wheel.log
cp imu.log.backup imu.log
cp run.log.backup run.log
cp carlData.json.backup carlData.json
echo "restored from backups: life, wheel, imu, run logs and carlData.json"
ls -al  life* wheel* imu* run* carlData*

