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

#  8*1.09v = 8.72v - 0.6v GoPiGo3 reverse polarity protection diode to get volt() reading
SafeShutDown = 8.1  # (1.09v/cell yields 6.5hr "fun time", 15-20% life remaining)

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
#   Jan 2018  8h07m
#   Sep 2018  9h21m   (8x EBL 2800mAh AA cells, around 2550 mAh on BC-3000 test)
#   Aug 2018  7h20m   (6xEnergizer 2300mAh AA and 2xAmazon 2000mAh AA)

#  (V , Time remaining)

lifePoints= (
 (16.0,  8.50),   # charging
 (11.0,  8.25),   # 
 (10.23, 8.12),   # 8h 07m to 7.04v
 (9.17,  7.12),
 (8.75,  6.12),
 (8.54,  5.12),
 (8.42,  4.12),
 (8.33,  3.12),
 (8.19,  2.12),
 (7.94,  1.12),
 (7.04,  0.12),
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
      print "batteryTooLow(8.0): ",batteryTooLow(8.0)
      Vtest=10.25
      print "hoursOfLifeRemaining(%.1f):%.2fh"% (Vtest,hoursOfLifeRemaining(Vtest)) 

if __name__ == "__main__":
    main()



