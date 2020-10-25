#!/bin/bash

# Set the GoPiGo3 antenna_wifi.service to start at boot
sudo systemctl enable antenna_wifi


# start GoPiGo3 antenna_wifi.service now
sudo systemctl start antenna_wifi

# add notice to life.log
/home/pi/Carl/logMaintenance.py "WiFi LED (antenna_wifi service) turned on permenantly"


