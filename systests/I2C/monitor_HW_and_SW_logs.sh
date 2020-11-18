#!/bin/bash

while true; do tail HW_I2C_during_SW_I2C_Stress.log; echo -e '\n======'; tail SW_I2C_Stress2.log; echo -e '\n====='; grep -c Exception SW_I2C_Stress2.log;echo -e "IMU (SW I2C) Exceptions \n=====";sleep 5; done;
