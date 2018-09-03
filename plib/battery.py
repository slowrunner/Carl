#!/usr/bin/python
#
# battery.py   BATTERY LIFE ESTIMATE
#

import myPyLib
import datetime
import sys
sys.path.append("/home/pi/Carl/plib")
import time
import os

# ########## HOURS OF LIFE REMAINING
# hoursOfLifeRemaining(Vbatt)
#
# Data points are adjusted to a shutdown point at 8.5v as a safe usage
#      based on run of batery_life.py using 4 times under 7.4v (0.925/cell shutdown)
#
#
# Historical:
#   Aug 2018  7.3h   (6xEnergizer 2300mAh AA and 2xAmazon 2000mAh AA)

#  (V , Time remaining)

lifePoints= (
 (11.0,  7.00),   # guess
 (10.71, 6.67),   # 6h 50m
 (9.56,  5.67),
 (9.25,  4.67),
 (9.14,  3.67),
 (9.01,  2.67),
 (8.96,  1.67),
 (8.76,  0.67),
 (8.50,  0.00),
 (8.25, -0.33),
 (7.40, -0.67),
 (0.00, -1.00)
 )

hoursOfLifeRemainingArray = myPyLib.InterpolatedArray(lifePoints)

def hoursOfLifeRemaining(Vbatt):
   return hoursOfLifeRemainingArray[Vbatt]

def printLifeTable():
  testVs = [ float(x)/10 for x in range(110,70, -5) ]
  print "Voltage Life Table"
  print "V   Hours Remaining"
  for v in testVs:
    print "%0.1f  %0.1f" % (v, hoursOfLifeRemaining(v))

SafeShutDown = 8.5  # 20% life

def batteryTooLow(vBatt):
  if (vBatt < SafeShutDown):
      return True
  else:
      return False


# ##### MAIN ######
def main():
      print "\n"
      printLifeTable()
      print "batteryTooLow(9.0): ",batteryTooLow(9.0)
      print "batteryTooLow(8.4): ",batteryTooLow(8.4)
      Vtest=9.0
      print "hoursOfLifeRemaining(%.1f):%.2fh"% (Vtest,hoursOfLifeRemaining(Vtest)) 

if __name__ == "__main__":
    main()



