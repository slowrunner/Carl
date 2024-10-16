#!/usr/bin/env python3
#
# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# File: noInitTest.py

# Usage:  Expand a console to be 192 chars wide (next line does not appear wrapped)
# 3456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012
#
# ./noInitTest.py  or python3 noInitTest.py
#
#
# Uses Alan's extended mutex protected SafeIMUSensor() class from my_safe_inertial_measurement_unit.py
# and my_inertial_measurement_unit.py and myBNO055.py
# to initialize the software object but does not alter the BNO055 hardware,
# and then print/overwrite a line of values 5 times a second.
#
# Note does not change the operation mode, regardless of value passed in.

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
READING_DELAY = 0.5




def main():
    IMUPORT = "AD1"   # Must be AD1 or AD2 only

    print("\nSafe Reads of DI IMU (BNO055 chip) WITHOUT INITIALIZING HARDWARE")
    print("Using mutex-protected, exception-tolerant SW I2C on GoPiGo3 port {}\n".format(IMUPORT))

    imu = SafeIMUSensor(port = IMUPORT, use_mutex = True, init=False, verbose = VERBOSITY)

    time.sleep(1.0)  # allow for all measurements to initialize

    exCnt = imu.getExceptionCount()

    try:
        imu.printCalStatus()
        # readAndPrint(imu,cnt=1,cr=True)

        op_mode_str = imu.safe_get_op_mode_str()

        print("Current Operation Mode: {}".format(op_mode_str))

        print("Not Resetting Chip")

        print("\nGet System Status (no self test): Fusion with no errors will return (5,None,0)")
        print("get_system_status:",imu.safe_get_system_status(run_self_test=False))

        print("\nReading every {} seconds".format(READING_DELAY))
        while True:
            imu.readAndPrint(cnt=1,delay=READING_DELAY,cr=False)
            if (imu.getExceptionCount() != exCnt):
                exCnt = imu.getExceptionCount()
                print("\n{}: Exception Count: {}".format(dt.now(),exCnt))
            if ((abs(imu.safe_read_gyroscope()[2]) > 0.5) or \
                (abs(imu.safe_read_linear_acceleration()[1]) > 0.5) ):
                print("\n                                              ** {} **\n".format(dt.now().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]))


    except KeyboardInterrupt:
        print("\nCntrl-C detected. Exiting..")


# Main loop
if __name__ == '__main__':
	main()

