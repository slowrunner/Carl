#!/bin/bash
PYTHONUNBUFFERED=1
export PYTHONUNBUFFERED
LOGFILE=imu.out

if test -f /home/pi/Carl/$LOGFILE; then
    mv /home/pi/Carl/$LOGFILE /home/pi/Carl/tmp/$LOGFILE.bak
fi

nohup /home/pi/Carl/plib/imulog.py  >/home/pi/Carl/$LOGFILE &

