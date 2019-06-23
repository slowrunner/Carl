#!/usr/bin/env python
#
#  currentSensor.py   ACS712 Current Sensor Utilities for GoPiGo3
#
#  The sensor should be connected to AD1 of the GoPiGo3
#
#  object:
#    ACS712(egpg, port="AD1", use_mutex=False)
#  methods:
#    get_reading(samples=10)    # return current in mA
#                               # range -5000.0 to +5000.0 mA
#                               # 6.6mA resolution +/-1.5% error
#

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

# import sys
# sys.path.append('/home/pi/Carl/plib')

from time import sleep
import easygopigo3 # import the EasyGoPiGo3 class
import easysensors # import Sensor() class
import numpy as np


VREF  = 5.10            # GoPiGo3 supplied
zeroV = 0.5 * VREF
READING_BIAS = 10       # saw 2073 instead of 2048
A2D_RESOLUTION = 4096   # GoPiGo3 A2D is 12-bit resolution on 0-5v range
mV_per_Amp = 220        # spec 185.0


# usage  egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)  # create a GoPiGo3 object
#        acs712 = currentSensor.ACS712(egpg)             # create the currentSensor
#  or    acs712 = currentSensor.ACS712(egpg, port="AD2", use_mutex=True)
#        print("Current Draw: {:.0f} mA".format( acs712.get_reading() ))
#
class ACS712(easysensors.AnalogSensor):
    def __init__(self, gpg,port="AD1", use_mutex=False):
        easysensors.AnalogSensor.__init__(self, port, "INPUT", gpg, gpg.use_mutex)
        easysensors.AnalogSensor.set_descriptor(self,"ACS712 +/-5A Current Sensor, outputs Analog Voltage 185mV/Amp around 2.5v")

    def get_amps(self, vRef=VREF, samples=10):

        vReadings = []
        for i in xrange(0,samples):
            sleep(.005)
            vReadings += [self.read()]
        aveV = (np.mean(vReadings)-READING_BIAS) / A2D_RESOLUTION * vRef
        print("aveReading: {:.0f}:".format(np.mean(vReadings)))
        print("aveV: {:.2f} v".format(aveV))
        # print("Readings:",vReadings)
        zeroV = vRef * 0.5
        amps = (zeroV - aveV) * 1000 / mV_per_Amp
        return amps



def main():
    try:
      egpg = easygopigo3.EasyGoPiGo3(use_mutex=True) # Create an instance of the EasyGoPiGo3 class
      acs712 = ACS712(egpg)  # default port AD1
      acs2 = ACS712(egpg,"AD2")
      # acs2.set_pin(2)
      # acs712.set_pin(2)
      print("Sensor Description",acs712.__str__())
      print("Averaged Current Reading: {:.3f} A".format(acs712.get_amps()))
      sleep(5)
      while True:
        # print("Single Current Reading:   {:.2f} A".format(acs712.get_amps(samples=1)))
        print("Averaged Current Reading: {:.3f} A".format(acs712.get_amps(egpg.get_voltage_5v()) ))
        print("5v supply {:.2f} v".format(egpg.get_voltage_5v()))

        # print("Sensor Description",acs2.__str__())
        # print("Single Current Reading:   {:.0f} mA".format(acs2.get_amps(samples=1)))
        # print("Averaged Current Reading: {:.0f} mA".format(acs2.get_amps()))

        print("\n\n")
        sleep(1)
    except KeyboardInterrupt:
        print("\nGoodbye")

if __name__ == "__main__":
	main()
