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

SafeShutDown = 8.75  # 20% life

# ########## HOURS OF LIFE REMAINING
# hoursOfLifeRemaining(Vbatt)
#
# Data points are adjusted to a shutdown point at 8.75v as a safe usage
#      based on run of batery_life.py using 4 times under 7.4v (0.925/cell shutdown)
#
#
# Historical:
#   Sep 2018  9.4h   (8x EBL 2800mAh AA cells, around 2550 mAh on BC-3000 test)
#   Aug 2018  7.3h   (6xEnergizer 2300mAh AA and 2xAmazon 2000mAh AA)

#  (V , Time remaining)

lifePoints= (
 (11.0,  8.25),   # guess
 (10.13, 7.75),   # 7h 45m to 8.75, 9h24m to 7.4v
 (9.54,  6.75),
 (9.42,  5.75),
 (9.36,  4.75),
 (9.30,  3.75),
 (9.10,  1.75),
 (8.91,  0.75),
 (8.75,  0.00),
 (8.70, -0.25),
 (7.40, -1.65),
 (0.00, -2.00)
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
      print "batteryTooLow(8.74): ",batteryTooLow(8.74)
      Vtest=10.25
      print "hoursOfLifeRemaining(%.1f):%.2fh"% (Vtest,hoursOfLifeRemaining(Vtest)) 

if __name__ == "__main__":
    main()



