#!/usr/bin/env python3
#
# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# My Python example program for the Dexter Industries IMU Sensor
# Uses my expanded mutex protected EasyIMUSensor() class from my_easy_inertial_measurement_unit.py
#

from __future__ import print_function
from __future__ import division

import time
#from di_sensors.inertial_measurement_unit import InertialMeasurementUnit
from my_easy_inertial_measurement_unit import EasyIMUSensor

# MUST be either AD1 or AD2 which implement sofware I2C with proper clock stretching
PORT = "AD1"

print("My example program for reading a Dexter Industries IMU Sensor on a GoPiGo3 {} port.".format(PORT))
imu = EasyIMUSensor(port = PORT, use_mutex = True)

time.sleep(1.0) # allow warmup

while True:
    try:
        # Read the magnetometer, gyroscope, accelerometer, euler, and temperature values
        mag   = imu.safe_read_magnetometer()
        gyro  = imu.safe_read_gyroscope()
        accel = imu.safe_read_accelerometer()
        euler = imu.safe_read_euler()
        temp  = imu.safe_read_temperature()

        string_to_print = \
                      "Euler Heading: {:>5.1f}  Roll: {:>5.1f}  Pitch: {:>5.1f} |  " \
                      "Mag XYZ: {:>4.1f} {:>4.1f} {:>4.1f} | " \
                      "Gyro XYZ: {:>4.1f} {:>4.1f} {:>4.1f} | " \
                      "Accel XYZ: {:>3.1f} {:>3.1f} {:>3.1f} | " \
                      "Temp: {:.1f}C".format(
                                             euler[0], euler[1], euler[2],
                                             mag[0], mag[1], mag[2],
                                             gyro[0], gyro[1], gyro[2],
                                             accel[0], accel[1], accel[2],
                                             temp)
        print(string_to_print)

        time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nCtrl-C Detected...")
        exit(0)
