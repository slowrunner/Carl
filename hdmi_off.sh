#!/bin/bash

# turn HDMI display circuit off to conserve ~25mA at 5v
sudo /usr/bin/tvservice -o
echo "HDMI (tvservice) off"

