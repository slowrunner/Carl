#!/bin/bash
LOGFILE=juicer.out

if test -f /home/pi/Carl/$LOGFILE; then
    mv /home/pi/Carl/$LOGFILE /home/pi/Carl/tmp/$LOGFILE.bak
fi

nohup /home/pi/Carl/plib/juicer.py > /home/pi/Carl/$LOGFILE &

