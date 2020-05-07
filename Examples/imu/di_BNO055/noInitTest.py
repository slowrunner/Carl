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

# Requested Mode
# REQ_MODE = BNO055.OPERATION_MODE_NDOF
REQ_MODE = BNO055.OPERATION_MODE_IMUPLUS


op_mode_str = ["CONFIG", "ACCONLY", "MAGONLY", "GYRONLY", "ACCMAG", "ACCGYRO", "MAGGYRO", "AMG", "IMUPLUS", "COMPASS", "M4G", "NDOF_FMC_OFF", "NDOF"]

def readIMU(imu):
        # Read the magnetometer, gyroscope, accelerometer, euler, and temperature values
        mag    = imu.safe_read_magnetometer()
        gyro   = imu.safe_read_gyroscope()
        accel  = imu.safe_read_accelerometer()
        euler  = imu.safe_read_euler()
        linacc = imu.safe_read_linear_acceleration()
        temp   = imu.safe_read_temperature()
        return [mag, gyro, accel, euler, linacc, temp]

def printReadings(readingsMGAELT, cr = False):
        mag = readingsMGAELT[0]
        gyro = readingsMGAELT[1]
        accel = readingsMGAELT[2]
        euler = readingsMGAELT[3]
        linacc = readingsMGAELT[4]
        temp = readingsMGAELT[5]

        string_to_print = \
                          "Euler Heading: {:>5.1f} Roll: {:>5.1f} Pitch: {:>5.1f} | " \
                          "Linear Acc XYZ: {:>4.1f} {:>4.1f} {:>4.1f} | " \
                          "Mag XYZ: {:>6.1f} {:>6.1f} {:>6.1f} | " \
                          "Gyro XYZ: {:>6.1f} {:>6.1f} {:>6.1f} | " \
                          "Accel XYZ: {:>6.1f} {:>6.1f} {:>6.1f} | " \
                          "Temp: {:.1f}C".format(
                                                    round(euler[0],1), round(euler[1],1), round(euler[2],1),
                                                    round(linacc[0],1), round(linacc[1],1), round(linacc[2],1),
                                                    mag[0], mag[1], mag[2],
                                                    round(gyro[0],1), round(gyro[1],1), round(gyro[2],1),
                                                    accel[0], round(accel[1],1), round(accel[2],1),
                                                    temp)
        if cr:
            print(string_to_print)
        else:
            print(string_to_print, end='\r')


def readAndPrint(imu,cnt=1,delay=0.02,cr = False):
    if cnt == 0:
        while True:
            printReadings(readIMU(imu),cr)
            time.sleep(delay)
    else:
        for i in range(cnt):
            printReadings(readIMU(imu),cr)
            time.sleep(delay)


def main():
    IMUPORT = "AD1"   # Must be AD1 or AD2 only

    print("\nSafe Reads of DI IMU (BNO055 chip) WITHOUT INITIALIZING HARDWARE")
    print("Using mutex-protected, exception-tolerant SW I2C on GoPiGo3 port {}\n".format(IMUPORT))

    imu = SafeIMUSensor(port = IMUPORT, use_mutex = True, mode = REQ_MODE, init=False, verbose = VERBOSITY)

    time.sleep(1.0)  # allow for all measurements to initialize

    exCnt = imu.getExceptionCount()

    try:
        imu.printCalStatus()
        # readAndPrint(imu,cnt=1,cr=True)

        op_mode = imu.safe_get_operation_mode()

        print("Current Operation Mode: {}-{} Requested Mode: {}-{}".format(op_mode_str[op_mode],op_mode, op_mode_str[REQ_MODE],REQ_MODE))
        if (op_mode != REQ_MODE):
            print("WARNING SENSOR IS NOT RUNNING IN REQUESTED MODE\n")

        print("Not Resetting Chip")

        print("\nGet System Status (no self test): Fusion with no errors will return (5,None,0)")
        print("get_system_status:",imu.safe_get_system_status(run_self_test=False))

        print("\nReading every {} seconds".format(READING_DELAY))
        while True:
            readAndPrint(imu,cnt=1,delay=READING_DELAY,cr=False)
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

