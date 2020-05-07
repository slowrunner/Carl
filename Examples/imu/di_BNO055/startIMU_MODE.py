#!/usr/bin/env python3
#
# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# File: startIMU_MODE.py

# ./startIMU_MODE.py  or python3 startIMU_MODE.py
#
#
# Uses Alan's extended mutex protected SafeIMUSensor() class from my_safe_inertial_measurement_unit.py
# and my_inertial_measurement_unit.py that allows passing/setting BNO055.OPERATION_MODE_IMUPLUS
# (Fusion using accelerometers and gyros only, no magnemometers)
# to start the BNO055, (sets heading, roll, pitch to 0,0,90)
#
# Note puts chip in IMUPLUS operation mode
# (Fusion uses Only Gyros and Accels, no mags)

from __future__ import print_function
from __future__ import division

import time
from datetime import datetime as dt
# from di_sensors.easy_inertial_measurement_unit import EasyIMUSensor
from my_safe_inertial_measurement_unit import SafeIMUSensor
# from di_sensors import BNO055
import myBNO055 as BNO055

# import numpy as np

VERBOSITY = True

def printHeading(imu,cr = True):
        euler = imu.safe_read_euler()

        string_to_print = "Heading: {:>5.1f} ".format(round(euler[0],1))
        if cr:
            print(string_to_print)
        else:
            print(string_to_print, end='\r')


def main():
    IMUPORT = "AD1"   # Must be AD1 or AD2 only

    print("\nReset DI IMU (BNO055 chip) in IMUPLUS mode")
    print("(Fusion based on Gyros, and Accels - no mags)")
    print("Using mutex-protected, exception-tolerant SW I2C on GoPiGo3 port {}\n".format(IMUPORT))

    imu = SafeIMUSensor(port = IMUPORT, use_mutex = True, mode = BNO055.OPERATION_MODE_IMUPLUS, init=True, verbose = VERBOSITY)

    time.sleep(1.0)  # allow for all measurements to initialize

    exCnt = imu.getExceptionCount()

    try:
        # Reseting chip to Heading:0, Roll:0, Pitch:90
        # imu.resetBNO055(verbose=VERBOSITY)
        printHeading(imu)
        print("\nExiting resetIMU_MODE.py")

    except KeyboardInterrupt:
        print("\nCntrl-C detected. Exiting..")


# Main loop
if __name__ == '__main__':
	main()

