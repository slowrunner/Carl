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
# Data points are adjusted to a recharge point of 8.5v as a safe usage
#      based on run of batery_life.py using 4 times under 7.4v (0.925/cell shutdown)
#
# Supposedly Toyota Prius uses 80% of battery capacity as safe limit to maximize 
#      number of recharge cycles.
#
# Historical:
#   Apr 2019  Auto docking off at trickle, on at 8.5v mean
#   Apr 2019  7h49m to 8.5v, +30m to 8.1, +15m to 7.5v, +1m to 7.1v h/w shutdown
#   Jan 2018  8h07m
#   Sep 2018  9h21m   (8x EBL 2800mAh AA cells, around 2550 mAh on BC-3000 test)
#   Aug 2018  7h20m   (6xEnergizer 2300mAh AA and 2xAmazon 2000mAh AA)
#   Mar 2019  1h30m   and 16.45v charging seen

#  (V , Time remaining)

lifePoints= (
 (18.000, 8.00),   # charging
 (11.025, 7.82),   # 
 (9.688,  6.82),   # 8h 48m to 8.5v
 (9.483,  5.82),
 (9.346,  4.82),
 (9.286,  3.82),
 (9.200,  2.82),
 (9.046,  1.82),
 (8.806,  0.82),
 (8.500,  0.00),   # 45m to 7.5v shutdown, recharge now
 (8.100,  -0.50),   # 15m to 7.5v shutdown
 (7.500,  -0.53),   # 1-2 min to total die
 (0.000,  -99.00)
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



