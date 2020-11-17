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
# ./SW_I2C_Stress_with_IMU.py 
#



from __future__ import print_function
from __future__ import division

import time
from datetime import datetime as dt

import sys
import easygopigo3 # import the EasyGoPiGo3 class

# Note: The di_sensors EasyIMUSensor() class does not implement mutex protected methods for linear accelerometer or temperature
from di_sensors.easy_inertial_measurement_unit import EasyIMUSensor

# Port must be "AD1" or "AD2" to force software I2C that properly implements clock stretch
PORT = "AD1"



def main():
    print("\nReading the Dexter Industries IMU Sensor")
    # print("Using mutex-protected, exception-tolerant SW I2C on GoPiGo3 port {}\n".format(PORT))
    print("Using EasyIMUSensor (DI mutex protected SW I2C) on GoPiGo3 port {}\n".format(PORT))
    print("Expand the window till this line fits")
    for i in range(0,5):
        print("123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890")
        time.sleep(2)

    imu = EasyIMUSensor(port = PORT, use_mutex = True)

    time.sleep(1.0)  # allow for all measurements to initialize

    count = 0
    try:
        while True:
            count+=1
            try:
                # Read the magnetometer, gyroscope, accelerometer, euler, and temperature values
                mag   = imu.safe_read_magnetometer()
                gyro  = imu.safe_read_gyroscope()
                accel = imu.safe_read_accelerometer()
                euler = imu.safe_read_euler()

                string_to_print = "Magnetometer X: {:>6.1f}  Y: {:>6.1f}  Z: {:>6.1f} " \
                      "Gyroscope X: {:>6.1f}  Y: {:>6.1f}  Z: {:>6.1f} " \
                      "Accelerometer X: {:>6.1f}  Y: {:>6.1f} Z: {:>6.1f} " \
                      "Euler Heading: {:>5.1f}  Roll: {:>5.1f}  Pitch: {:>5.1f}".format(mag[0], mag[1], mag[2],
                                                        round(gyro[0],1), round(gyro[1],1), round(gyro[2],1),
                                                        accel[0], round(accel[1],1), round(accel[2],1),
                                                        round(euler[0],1), round(euler[1],1), round(euler[2],1))
            except Exception as e:

                string_to_print = "Soft Error"
                print("SW_I2C_Stress_with_IMU.py: Exception")
                print(str(e))

            # read IMU 10 times per second and print once per second
            if (count%10)==1:
                print("{} {}".format(time.strftime("%H:%M:%S"),count))
                # read and print new line of values 1 time per second
                print(string_to_print)
            else:
                time.sleep(0.1)


    except KeyboardInterrupt:
        print("\nCntrl-C detected. Exiting..")
        # break


# Main loop
if __name__ == '__main__':
	main()

