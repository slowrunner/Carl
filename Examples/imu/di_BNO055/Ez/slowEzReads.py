#!/usr/bin/env python3
#
# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Extended Python example program for the Dexter Industries IMU Sensor
#
# Usage:  Expand a console to be 192 chars wide (next line does not appear wrapped)
# 3456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012
# ./slowEzReads.py  or python3 slowEzReads.py
#
# Uses Alan's extended mutex protected EasyIMUSensor() class from my_easy_inertial_measurement_unit.py
# to print/overwrite a line of values 5 times a second or print once per second without overwrite
#
# If an I2C exception occurs, the time will be printed
# (Software I2C read exceptions will occur and must be tolerated.)
#
# If a rotation greater than 0.5 dps is seen, the time will be printed forcing the values to remain visible
#
# Ensure PORT ("AD1") and OVERWRITE (True) are desired values



from __future__ import print_function
from __future__ import division

import time
from datetime import datetime as dt

# di_sensors EasyIMUSensor() class does not implement all the needed mutex protected methods
# from di_sensors.easy_inertial_measurement_unit import EasyIMUSensor
# so uses my_easy_inertial_measurement_unit.py
from my_easy_inertial_measurement_unit import EasyIMUSensor

# Port must be "AD1" or "AD2" to force software I2C that properly implements clock stretch
PORT = "AD1"

# to repeatedly overwrite readings line 5 times a second, set True
# to list readings once per second without overwriting, set False
OVERWRITE = True

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

# Read and Print values
#
# If cnt = 0, repeats until cntrl-C

def readAndPrint(imu,cnt=1,delay=0.01,cr = False):
    if cnt == 0:
        while True:
            printReadings(readIMU(imu),cr)
            time.sleep(delay)
    else:
        for i in range(cnt):
            printReadings(readIMU(imu),cr)
            time.sleep(delay)


def main():
    print("\nMy example program for reading a Dexter Industries IMU Sensor")
    print("Using mutex-protected, exception-tolerant SW I2C on GoPiGo3 port {}\n".format(PORT))

    imu = EasyIMUSensor(port = PORT, use_mutex = True)

    time.sleep(1.0)  # allow for all measurements to initialize

    # exception count will probably be zero at the start
    exCnt = imu.getExceptionCount()

    try:
        print("\n{}: Exception Count: {}".format(dt.now(),exCnt))
        while True:
            if OVERWRITE:
                # read and print/overwrite line of values 5 times per second
                readAndPrint(imu,cnt=1,delay=0.2)
            else:
                # read and print new line of values 1 time per second
                readAndPrint(imu,cnt=1,delay=1.0,cr = True)


            if (imu.getExceptionCount() != exCnt):
                # when exception occurs print the count and time
                exCnt = imu.getExceptionCount()
                print("\n{}: Exception Count: {}".format(dt.now(),exCnt))

            # if rotation or detected print time forcing last values to remain visible
            # if (abs(imu.safe_read_gyroscope()[2]) > 0.5): print("\n                                              ** {} **\n".format(dt.now().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]))
            # if (abs(imu.safe_read_linear_acceleration()[1]) > 0.5): print("\n    xx                                        ** {} **\n".format(dt.now().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]))
            if ((abs(imu.safe_read_gyroscope()[2]) > 0.5) or \
                (abs(imu.safe_read_linear_acceleration()[1]) > 0.5) ):
                print("\n                                              ** {} **\n".format(dt.now().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]))



        print("\n")

    except KeyboardInterrupt:
        print("\nCntrl-C detected. Exiting..")
        # break


# Main loop
if __name__ == '__main__':
	main()

