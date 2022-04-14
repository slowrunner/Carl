#!/bin/bash

echo "Reboot Requested"
batt=`(/home/pi/Carl/plib/battery.py)`
/home/pi/Carl/logMaintenance.py "Reboot Requested"
/home/pi/Carl/logMaintenance.py "'$batt'"
sudo shutdown -r +1
