#!/bin/bash

echo "Routine Shutdown Requested"
batt=`(/home/pi/Carl/plib/battery.py)`
/home/pi/Carl/logMaintenance.py "Routine Shutdown"
/home/pi/Carl/logMaintenance.py "'$batt'"
sudo shutdown -h +2
