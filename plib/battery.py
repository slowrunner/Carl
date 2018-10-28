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

SafeShutDown = 8.75  # (1.09375v/cell yields 8h "fun time", 14% life remaining 1h18m)

# ########## HOURS OF LIFE REMAINING
# hoursOfLifeRemaining(Vbatt)
#
# Data points are adjusted to a shutdown point at 8.75v as a safe usage
#      based on run of batery_life.py using 4 times under 7.4v (0.925/cell shutdown)
#
# Supposedly Toyota Prius uses 80% of battery capacity as safe limit to maximize 
#      number of recharge cycles.
#
# Historical:
#   Sep 2018  9h21m   (8x EBL 2800mAh AA cells, around 2550 mAh on BC-3000 test)
#   Aug 2018  7h20m   (6xEnergizer 2300mAh AA and 2xAmazon 2000mAh AA)

#  (V , Time remaining)

lifePoints= (
 (14.0,  8.30),   # charging
 (11.0,  8.25),   # guess
 (10.23, 7.95),   # 7h 57m to 8.75, 9h21m to 7.4v
 (9.56,  6.95),
 (9.40,  5.95),
 (9.33,  4.95),
 (9.28,  3.95),
 (9.22,  1.95),
 (8.95,  0.95),
 (8.75,  0.00),
 (7.99, -1.30),
 (7.40, -1.38),
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



