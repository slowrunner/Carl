#!/bin/bash

echo "TOP DISK SPACE FROM /"
sudo du -a / | sort -n -r | head -n 10
echo ""
echo "TOP DISK SPACE FROM /home/pi"
du -a /home/pi | sort -n -r | head -n 10
echo ""
df /


