#!/bin/bash
LOGFILE=voicecmdr.out

if test -f /home/pi/Carl/$LOGFILE; then
    mv /home/pi/Carl/$LOGFILE /home/pi/Carl/tmp/$LOGFILE.bak
fi

nohup /home/pi/Carl/plib/voicecmdr.py > /home/pi/Carl/$LOGFILE &
# nohup /home/pi/Carl/plib/voicecmdr.py  >/dev/null 2>&1 &

