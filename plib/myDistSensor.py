#!/usr/bin/python
#
# myDistSensor.py    DISTANCE SENSOR 
#
#
# Methods:
#     adjustForAveErrorInMM(reading)  returns corrected reading
#
# Constants:
#     ERROR_IN_MM  difference between readings and actual (positive means reading higher than average)
#
"""
```
# Usage:
import sys
sys.path.append('/home/pi/Carl/plib')
import myDistSensor

correctedDistanceInMM = myDistSensor.adjustForAveErrorInMM(ds.read_mm())
```
"""

# Readings error (positive if reading is greater than actual)
ERROR_IN_MM = 13

def adjustForAveErrorInMM(reading):
    return reading - ERROR_IN_MM
