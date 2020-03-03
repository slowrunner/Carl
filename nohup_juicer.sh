#!/bin/bash
LOGFILE=/home/pi/Carl/juicer.out

if test -f "$LOGFILE"; then
    mv $LOGFILE $LOGFILE".bak"
fi

# nohup /home/pi/Carl/plib/juicer.py > $LOGFILE &
nohup /home/pi/Carl/Projects/Juicer/new_juicer.py > $LOGFILE &

