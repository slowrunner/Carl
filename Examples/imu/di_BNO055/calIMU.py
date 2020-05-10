#!/usr/bin/env python3
#
# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# File: calIMU.py

# ./calIMU.py  or python3 calIMU.py
#
# Assists user to perform calibration for NDOF mode
#
# Uses Alan's extended mutex protected SafeIMUSensor() class from my_safe_inertial_measurement_unit.py
# and my_inertial_measurement_unit.py.
#
# Note Does not alter operation mode

from __future__ import print_function
from __future__ import division

import time
from datetime import datetime as dt
from my_safe_inertial_measurement_unit import SafeIMUSensor
import myBNO055 as BNO055
from easygopigo3 import EasyGoPiGo3
from math import pi

CAL_SPEED = 150
VERBOSITY = True
WHEEL_DIAMETER    = 64.0
WHEEL_BASE_WIDTH  = 114.05  # for Monk Makes speaker.  (115.1 with HP speaker)

def main():
    IMUPORT = "AD1"   # Must be AD1 or AD2 only

    print("\nCalibrate DI IMU (BNO055 chip) without changing mode")
    print("Using mutex-protected, exception-tolerant SW I2C on GoPiGo3 port {}\n".format(IMUPORT))

    imu = SafeIMUSensor(port = IMUPORT, use_mutex = True, init=False, verbose = VERBOSITY)
    time.sleep(1.0)  # allow for all measurements to initialize


    op_mode_str = imu.safe_get_op_mode_str()
    print("Chip operating in {} mode".format(op_mode_str))

    try:
        print("\nCurrent Calibration Status:")
        imu.printCalStatus()

        # Reseting chip (Heading:0, Roll:0, Pitch:90)
        #imu.safe_resetBNO055(verbose=VERBOSITY)
        # Remap for GoPiGo3: Point-Up, Chip-Toward Front
        #imu.safe_axis_remap(verbose=VERBOSITY)

        if op_mode_str == "NDOF":
            print("\nIf Cal Status not [3,3,0,3], Rotate GoPiGo3 in rocking figure-8 pattern")
            imu.my_safe_calibrate(verbose=True)
            imu.printCalStatus()
        elif op_mode_str == "IMUPLUS":
            print("\nIMU will perform calibration automatically")
            print("No special motion is required")

        print("\n ************* Waiting 15s: Please set GoPiGo on floor, in reference direction ******************")
        time.sleep(15)

        imu.readAndPrint(cr=True)

        print("\nChecking Calibration Status for 1 minute")
        for i in range(0,10):
            imu.printCalStatus(cr=False)
            time.sleep(6)

        print("\n")
        imu.readAndPrint(cr=True)

        print("\nExiting calIMU.py")

    except KeyboardInterrupt:
        print("\nCntrl-C detected. Exiting..")


# Main loop
if __name__ == '__main__':
	main()

