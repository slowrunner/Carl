#!/bin/bash

# stop GoPiGo3 antenna_wifi.service
sudo systemctl stop antenna_wifi
# turn off wifi_led
python -c "import gopigo3;GPG=gopigo3.GoPiGo3();GPG.set_led(GPG.LED_WIFI,0,0,0)"

