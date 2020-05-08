#!/usr/bin/env python3
#
# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# File: resetIMU.py

# ./resetIMU.py  or python3 reestIMU.py
#
#
# Uses Alan's extended mutex protected SafeIMUSensor() class from my_safe_inertial_measurement_unit.py
# and my_inertial_measurement_unit.py that allows reseting the chip without changing mode.
#
# Note Does not alter operation mode

from __future__ import print_function
from __future__ import division

import time
from datetime import datetime as dt
from my_safe_inertial_measurement_unit import SafeIMUSensor
import myBNO055 as BNO055

VERBOSITY = True




def main():
    IMUPORT = "AD1"   # Must be AD1 or AD2 only

    print("\nReset DI IMU (BNO055 chip) without changing mode")
    print("Using mutex-protected, exception-tolerant SW I2C on GoPiGo3 port {}\n".format(IMUPORT))

    imu = SafeIMUSensor(port = IMUPORT, use_mutex = True, init=False, verbose = VERBOSITY)

    time.sleep(1.0)  # allow for all measurements to initialize

    exCnt = imu.getExceptionCount()

    try:
        imu.printCalStatus()
        # Reseting chip (Heading:0, Roll:0, Pitch:90)
        imu.safe_resetBNO055(verbose=VERBOSITY)
        # Remap for GoPiGo3: Point-Up, Chip-Toward Front
        imu.safe_axis_remap(verbose=VERBOSITY)

        imu.printCalStatus()

        print("\n")
        imu.readAndPrint(cr=True)
        print("\nExiting resetIMU.py")

    except KeyboardInterrupt:
        print("\nCntrl-C detected. Exiting..")


# Main loop
if __name__ == '__main__':
	main()

