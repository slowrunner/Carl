#!/usr/bin/env python3

# FILE: check_quiet_time.py

# PURPOSE: Check if current time is considered "quiet time"
#          (quiet time is between 11pm and 10am )

import sys
sys.path.insert(1,"/home/pi/Carl/plib")
import speak
import datetime as dt

dtNow=dt.datetime.now().strftime("%H:%M:%S")

if speak.quietTime():
	print("{} is Quiet Time".format(dtNow))
else:
	print("{} is not Quiet Time".format(dtNow))

