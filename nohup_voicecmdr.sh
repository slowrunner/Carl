#!/bin/bash
LOGFILE=/home/pi/Carl/voicecmdr.out

if test -f "$LOGFILE"; then
    mv $LOGFILE $LOGFILE".bak"
fi

nohup /home/pi/Carl/plib/voicecmdr.py > $LOGFILE &
# nohup /home/pi/Carl/plib/voicecmdr.py  >/dev/null 2>&1 &

