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

# from time import sleep
import easygopigo3 # import the EasyGoPiGo3 class
import easysensors # import Sensor() class
import numpy as np

# usage  egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)  # create a GoPiGo3 object
#        acs712 = currentSensor.ACS712(egpg)             # create the currentSensor
#  or    acs712 = currentSensor.ACS712(egpg, port="AD2", use_mutex=True)
#        print("Current Draw: {:.0f} mA".format( acs712.get_reading() ))
#
class ACS712(easysensors.AnalogSensor):
    def __init__(self, gpg,port="AD1", use_mutex=False):
        easysensors.AnalogSensor.__init__(self, port, "INPUT", gpg, gpg.use_mutex)
        easysensors.AnalogSensor.set_descriptor(self,"ACS712 +/-5A Current Sensor, outputs Analog Voltage 185mV/Amp around 2.5v")


    def get_reading(self, samples=10):
        mA_per_mV = 185.0
        zeroV = 2.50
        VREF = 5.0              # GoPiGo3 Analog Input is 0-5v
        A2D_RESOLUTION = 4096   # GoPiGo3 A2D is 12-bit resolution on 0-5v range

        vReadings = []
        for i in xrange(0,samples):
            vReadings += [(self.read() / A2D_RESOLUTION) * VREF]
        aveV = np.mean(vReadings)
        # print("aveV:",aveV)
        # print("Readings:",vReadings)
        mA = (aveV - zeroV) * 1000 / mA_per_mV
        return mA



def main():
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True) # Create an instance of the EasyGoPiGo3 class
    acs712 = ACS712(egpg)  # default port AD1

    print("Sensor Descriptor",acs712.descriptor)
    print("Single Current Reading:   {:.0f} mA".format(acs712.get_reading(samples=1)))
    print("Averaged Current Reading: {:.0f} mA".format(acs712.get_reading()))

if __name__ == "__main__":
	main()
