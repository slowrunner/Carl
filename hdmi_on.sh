#!/bin/bash

# turn HDMI display circuit back on, adds ~25mA at 5v
sudo /usr/bin/tvservice -p

# add notice to life.log
/home/pi/Carl/logMaintenance.py "HDMI (tvservice) on"

