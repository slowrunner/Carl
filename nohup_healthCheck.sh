#!/bin/bash
LOGFILE=healthCheck.out

if test -f /home/pi/Carl/$LOGFILE; then
    mv /home/pi/Carl/$LOGFILE /home/pi/Carl/tmp/$LOGFILE.bak
fi

nohup /home/pi/Carl/plib/healthCheck.py > /home/pi/Carl/$LOGFILE &

