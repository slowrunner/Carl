#!/usr/bin/env python3
#
# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# File: safeRead.py

# Usage:  Expand a console to be 192 chars wide (next line does not appear wrapped)
# 3456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012
#
# ./safeRead.py  or python3 safeRead.py
#
#
# Uses Alan's extended mutex protected SafeIMUSensor() class from my_safe_inertial_measurement_unit.py
# and my_inertial_measurement_unit.py that allows a software object only instantiation
# and then print/overwrite a line of values 5 times a second.
#
# Note Does not alter operation mode

from __future__ import print_function
from __future__ import division

import time
from datetime import datetime as dt
from my_safe_inertial_measurement_unit import SafeIMUSensor
import myBNO055 as BNO055


VERBOSITY = True
READING_DELAY = 0.5



def main():
    IMUPORT = "AD1"   # Must be AD1 or AD2 only

    print("\nSafe Reads of DI IMU (BNO055 chip)")

    #print("(Fusion based on Gyros, and Accels - no mags)")
    print("Using mutex-protected, exception-tolerant SW I2C on GoPiGo3 port {}\n".format(IMUPORT))

    imu = SafeIMUSensor(port = IMUPORT, use_mutex = True, init = False, verbose = VERBOSITY)
    print("Chip operating in {} mode".format(imu.safe_get_op_mode_str()))

    time.sleep(1.0)  # allow for all measurements to initialize

    exCnt = imu.getExceptionCount()

    try:
        imu.printCalStatus()
        # readAndPrint(imu,cnt=1,cr=True)

        print("Not Resetting Chip")
        """
        print("\nRun System Self-Test: Success = (5,15,0)")
        print("get_system_status:",imu.safe_get_system_status(run_self_test=True))
        # or
        print("\nGet System Status (no self test): Fusion running with no errors= (5,None,0)")
        print("get_system_status:",imu.safe_get_system_status(run_self_test=False))

        print("\n(Reset chip to Heading:0, Roll:0, Pitch:90)")
        imu.safe_resetBNO055(verbose=VERBOSITY)
        print("\nRemap for GoPiGo3: Point-Up, Chip-Toward Front")
        imu.safe_axis_remap(verbose=VERBOSITY)
        imu.printCalStatus()
        """

        print("\nReading every {} seconds starting at {}".format(READING_DELAY, dt.now().strftime('%m-%d-%Y %H:%M:%S')[:-3]))
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

