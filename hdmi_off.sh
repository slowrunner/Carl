#!/bin/bash

# turn HDMI display circuit off to conserve ~25mA at 5v
sudo /usr/bin/tvservice -o

# add notice to life.log
/home/pi/Carl/logMaintenance.py "HDMI (tvservice) off"

