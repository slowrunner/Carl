#!/bin/bash

# stop GoPiGo3 antenna_wifi.service
sudo systemctl stop antenna_wifi

# Stop the GoPiGo3 antenna_wifi.service being loaded at boot 
sudo systemctl disable antenna_wifi

# turn off wifi_led
python -c "import gopigo3;GPG=gopigo3.GoPiGo3();GPG.set_led(GPG.LED_WIFI,0,0,0)"
# add notice to life.log
/home/pi/Carl/logMaintenance.py "WiFi LED (antenna_wifi service) turned off permenantly"
