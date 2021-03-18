#!/bin/bash
PYTHONUNBUFFERED=1
export PYTHONUNBUFFERED

LOGFILE=/home/pi/Carl/juicer.out

if test -f "$LOGFILE"; then
    mv $LOGFILE $LOGFILE".bak"
fi

nohup /home/pi/Carl/Projects/Juicer/juicer.py > $LOGFILE &

