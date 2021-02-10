#!/bin/bash

sudo nohup python3 -u /home/pi/Carl/systests/WiFi/test_wifi.py > /home/pi/Carl/systests/WiFi/wifi.out &
echo "test_wifi.py logging to ~/Carl/systests/WiFi/wifi.out"


