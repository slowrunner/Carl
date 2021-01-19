#!/bin/bash

cp life.log backups/life.log.backup
cp wheel.log backups/wheel.log.backup
cp imu.log backups/imu.log.backup
cp run.log backups/run.log.backup
cp carlData.json backups/carlData.json.backup
cp juicer.out backups/juicer.out.backup
echo "backed up life, wheel, imu, run, juicer logs and carlData.json"
ls -al backups/*.backup
echo " "
echo "Note: Does not backup google.cloud.cred.json"
echo "      Does not backup openweathermap.key"
echo "      Does not backup wunderground.key"
echo "      Does not backup nyumaya_engine_carl/models"

