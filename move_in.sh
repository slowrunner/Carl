#!/bin/bash

cp life.log.backup life.log
cp juicer.backup juicer.out
cp wheel.log.backup wheel.log
cp imu.log.backup imu.log
cp run.log.backup run.log
chmod 666 *.log
cp carlData.json.backup carlData.json
sudo cp configs/etc.asound.conf.PiOS /etc/asound.conf
sudo cp /usr/share/alsa/alsa.conf /usr/share/alsa/alsa.conf.bak
sudo cp configs/usr.share.alsa.alsa.conf /usr/share/alsa/alsa.conf
cp configs/home.pi.dot.asoundrc.PiOS /home/pi/.asoundrc