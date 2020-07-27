#!/bin/bash

# turn HDMI display circuit back on, adds ~25mA at 5v
sudo /usr/bin/tvservice -p
echo "HDMI (tvservice) on"

