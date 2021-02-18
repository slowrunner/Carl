#!/bin/bash

echo "checkI2C.sh"
echo " "
echo "I2C Device Detect"
i2cdetect -y 1
echo " "
echo "~/Carl/plib/readDistOnce.py"
~/Carl/plib/readDistOnce.py
echo " "
echo "I2C issue exists if Distance is 0"
