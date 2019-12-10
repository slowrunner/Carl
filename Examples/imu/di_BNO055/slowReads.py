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
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit
import numpy as np

def readIMU(imu):
        # Read the magnetometer, gyroscope, accelerometer, euler, and temperature values
        mag    = imu.read_magnetometer()
        gyro   = imu.read_gyroscope()
        accel  = imu.read_accelerometer()
        euler  = imu.read_euler()
        linacc = imu.read_linear_acceleration()
        temp   = imu.read_temperature()
        return [mag, gyro, accel, euler, linacc, temp]

def printReadings(readingsMGAELT):
        mag = readingsMGAELT[0]
        gyro = readingsMGAELT[1]
        accel = readingsMGAELT[2]
        euler = readingsMGAELT[3]
        linacc = readingsMGAELT[4]
        temp = readingsMGAELT[5]

        string_to_print = \
                          "Euler Heading: {:>4.0f} Roll: {:>4.0f} Pitch: {:>4.0f} | " \
                          "Linear Acc XYZ: {:>4.1f} {:>4.1f} {:>4.1f} | " \
                          "Mag XYZ: {:>6.1f} {:>6.1f} {:>6.1f} | " \
                          "Gyro XYZ: {:>6.1f} {:>6.1f} {:>6.1f} | " \
                          "Accel XYZ: {:>6.1f} {:>6.1f} {:>6.1f} | " \
                          "Temp: {:.1f}C".format(
                                                    round(euler[0],0), round(euler[1],0), round(euler[2],0),
                                                    round(linacc[0],1), round(linacc[1],1), round(linacc[2],1),
                                                    mag[0], mag[1], mag[2],
                                                    round(gyro[0],1), round(gyro[1],1), round(gyro[2],1),
                                                    accel[0], round(accel[1],1), accel[2],
                                                    temp)
        print(string_to_print, end='\r')


def readAndPrint(imu,cnt=1,delay=0.01):
    print("\nRead And Print {} times with delay: {:.3f}".format(cnt,delay))
    if cnt == 0:
        while True:
            printReadings(readIMU(imu))
            time.sleep(delay)
    else:
        for i in range(cnt):
            printReadings(readIMU(imu))
            time.sleep(delay)
    print("\n")


def main():
    print("\nExample program for reading a Dexter Industries IMU Sensor")
    print("Using SW I2C on GoPiGo3 port AD1\n")

    imu = InertialMeasurementUnit(bus = "GPG3_AD1")
    # Note: HW I2C does not properly implement clock stretching
    #       and will result in invalid readings
    # imu = InertialMeasurementUnit(bus = "RPI_1")  # do not use HW I2C

    time.sleep(1.0)  # allow for all measurements to initialize


    try:
        # readAndPrint(2,1.0)  # twice, 1s apart

        # multiReadAndPrint(100,0.01)

        # calibrateMags(imu)

        # print("Place Carl on Floor")
        # time.sleep(10.0)

        # readAndPrint(2,1.0)
        # multiReadAndPrint(imu,100,0.01)

        readAndPrint(imu,0,1.0)

        #XYZ = track(imu, 1000, 0.01)
        print("\n")

    except KeyboardInterrupt:
        print("\nCntrl-C detected. Exiting..")
        # break


# Main loop
if __name__ == '__main__':
	main()

