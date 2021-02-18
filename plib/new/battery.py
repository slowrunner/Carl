#!/usr/bin/python3
#
# battery.py   BATTERY LIFE ESTIMATE
#

import myPyLib
import datetime
import sys
sys.path.append("/home/pi/Carl/plib")
import time
import os

#  8 * 1.0125v/cell = 8.1v - 0.6v GoPiGo3 reverse polarity protection diode to get volt() reading
SafeShutDown = 7.5  # (1.0125v/cell yields 6.7hr "fun time", 2% life 8m remaining)

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
#   Jul 2019  7h to death, 6h15m to 8.1v playtime (8x Powerowl 2800mAh 2250 on BC-3000 test)
#   Apr 2019  Auto docking off at trickle, on at 8.5v mean (new EBLs)
#   Apr 2019  7h49m to 8.5v, +30m to 8.1, +15m to 7.5v, +1m to 7.1v h/w shutdown
#   Jan 2018  8h07m
#   Sep 2018  9h21m   (8x EBL 2800mAh AA cells, around 2550 mAh on BC-3000 test)
#   Aug 2018  7h20m   (8x EBL 2800mAh))


#  (V , Time remaining)
lifePoints= (
 (18.00,  7.02),   # charging
 (11.00,  7.01),   #
 (10.70,  7.00),   # 7h to total die
 (9.580,  6.00),
 (9.400,  5.00),
 (9.310,  4.00),
 (9.250,  3.00),
 (9.140,  2.00),
 (8.810,  1.00),
 (8.100,  0.45),   # 27m or 20m to 7.5v shutdown - normal playtime limit
 (7.700,  0.22),   # 13m or 5m to 7.5v shutdown - conditioning limit
 (7.500,  0.13),   # 8 min estimated to total die
 (7.200,  0.00),
 (0.000,  -999.00)
 )

hoursOfLifeRemainingArray = myPyLib.InterpolatedArray(lifePoints)

def hoursOfLifeRemaining(Vbatt):
   return hoursOfLifeRemainingArray[Vbatt]

def printLifeTable():
  testVs = [ float(x)/10 for x in range(110,70, -5) ]
  print ("Voltage Life Table")
  print ("V   Hours Remaining")
  for v in testVs:
    print ("%0.1f  %0.1f" % (v, hoursOfLifeRemaining(v)))

def batteryTooLow(vBatt):
  if (vBatt < SafeShutDown):
      return True
  else:
      return False


# ##### MAIN ######
def main():
      print ("\n")
      printLifeTable()
      print ("Safety Shutdown:",SafeShutDown,"v")
      print ("batteryTooLow(8.5): ",batteryTooLow(8.5))
      print ("batteryTooLow(7.4): ",batteryTooLow(7.4))
      Vtest=10.7
      print ("hoursOfLifeRemaining(%.1f): %.2fh"% (Vtest,hoursOfLifeRemaining(Vtest)) )

if __name__ == "__main__":
    main()



