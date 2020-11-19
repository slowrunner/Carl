#!/bin/bash

HWLOG="HW_I2C_during_SW_I2C_Stress.log"
SWLOG="SW_I2C_Stress.log"


if test -f "$HWLOG"; then
    mv $HWLOG $HWLOG".bak"
    echo "Created " $HWLOG".bak"
fi

if test -f "$SWLOG"; then
    mv $SWLOG $SWLOG".bak"
    echo "Created " $SWLOG".bak"
fi




echo "Starting to stress HW I2C by requesting a DI Distance Sensor reading roughly 10 times per second"
./HWDistanceSensor.py > $HWLOG &

echo "Adding SW I2C stress by requesting set of four DI IMU component readings roughly 10 times per second"
./SW_I2C_Stress_with_IMU.py > $SWLOG &

echo " "
echo "Now Run ./monitor_HW_and_SW_logs.sh to watch results"

echo "To end test, control-c out of the monitor_HW_and_SW_logs.sh process"
echo "and then run:"

echo '    ps -ef | grep -v grep | grep -E "SW_I2C_Stress_with_IMU|HWDistanceSensor"'
ps -ef | grep -v grep | grep -E "SW_I2C_Stress_with_IMU|HWDistanceSensor"

echo " "
echo "Note the process numbers, then kill the listed python3 processes with"
echo "    kill <left_most_PID>"
echo "    kill <left_most_PID>"


