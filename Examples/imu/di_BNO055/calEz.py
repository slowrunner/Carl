#!/usr/bin/env python3
#
# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python example program for the Dexter Industries IMU Sensor

from __future__ import print_function
from __future__ import division

import time
from datetime import datetime as dt
#from di_sensors.easy_inertial_measurement_unit import EasyIMUSensor
from my_easy_inertial_measurement_unit import EasyIMUSensor
# import calBNO055
import numpy as np

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


def readAndPrint(imu,cnt=1,delay=0.01,cr = False):
    if cnt > 1:
        print("\nRead And Print {} times with delay: {:.3f}".format(cnt,delay))
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

    print("\nExample program for reading a Dexter Industries IMU Sensor")
    print("Using SW I2C on GoPiGo3 port {}\n".format(IMUPORT))

    imu = EasyIMUSensor(port = IMUPORT, use_mutex = True)  


    time.sleep(1.0)  # allow for all measurements to initialize

    exCnt = imu.getExceptionCount()

    try:
        calStatus = imu.safe_calibration_status()
        print("NDOF Calibration {}".format(calStatus))

        if calStatus < 3:
            print("Rotate GoPiGo3 in swinging figure-8 until calibrated")
            imu.safe_calibrate()
            print("Calibration Complete")
            time.slieep(1.0)

        # print("\n{}: Exception Count: {}".format(dt.now(),exCnt))


        while True:
            readAndPrint(imu,cnt=1,delay=0.2)
            if (imu.getExceptionCount() != exCnt):
                exCnt = imu.getExceptionCount()
                print("\n{}: Exception Count: {}".format(dt.now(),exCnt))
            if (abs(imu.safe_read_gyroscope()[2]) > 0.5): print("\n                                              ** {} **\n".format(dt.now().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]))
        #XYZ = track(imu, 1000, 0.01)
        print("\n")

    except KeyboardInterrupt:
        print("\nCntrl-C detected. Exiting..")
        # break


# Main loop
if __name__ == '__main__':
	main()

