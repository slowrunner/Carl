#!/bin/bash

while true; do tail status_during_SW_I2C_Stress.log; echo -e '\n======'; tail SW_I2C_Stress.log; echo -e '\n====='; grep -c Exception SW_I2C_Stress.log;echo -e "IMU (SW I2C) Exceptions \n=====";sleep 5; done;
