#!/bin/bash

diskused=`df | grep mmcblk0p2` ; \

while true; \
do echo -e "\n********** GoPiGo3 CARL MONITOR ******************************"; \
echo -n `date +"%A %D"`; \
echo ""; \
uptime; \
vcgencmd measure_temp && vcgencmd measure_clock arm && vcgencmd get_throttled; \
# python3 /home/ubuntu/KiltedDave/plib/battery.py; 
python3 /home/pi/Carl/plib/battery.py; 
echo "Disk Usage: "${diskused: -6:4}; \
echo ""; \
free -h; \
diskused=`df | grep mmcblk0p2` ; \
sleep 10; \
echo " "; \
done

