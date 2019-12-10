#!/usr/bin/env python
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
from di_sensors import BNO055

# print("Example program for reading a Dexter Industries IMU Sensor on a GoPiGo3 AD1 port.")
print("Example program for reading a Dexter Industries IMU Sensor on a GoPiGo3 HW I2C port.")

# imu = InertialMeasurementUnit(bus = "GPG3_AD1")
imu = InertialMeasurementUnit(bus = "RPI_1")  # use HW I2C on Carl
time.sleep(1.0) # wait for startup

while True:
  try:
    # Read the magnetometer, gyroscope, accelerometer, euler, and temperature values
    #mag   = imu.read_magnetometer()
    #gyro  = imu.read_gyroscope()
    #accel = imu.read_accelerometer()
    #euler = imu.read_euler()
    #temp  = imu.read_temperature()

    # try one i2c read for 22 16-bit signed values 
    # plus get temp+calibration_status as 16-bit signed value for unpacking later
    oneRead = imu.BNO055._read_vector(BNO055.REG_ACCEL_DATA_X_LSB,23)
    # print(oneRead)
    accel = [oneRead[i]/100.0 for i in range(0,3)]
    mag = [oneRead[i]/16.0 for i in range(3,6)]
    gyro = [oneRead[i]/16.0 for i in range(6,9)]
    euler = [oneRead[i]/16.0 for i in range(9,12)]
    #  quaternian scale factor
    quatScale = (1.0 / (1<<14))
    quat  = [oneRead[i]/quatScale for i in range(12,16)]
    linacc = [oneRead[i]/100.0 for i in range(16,19)]
    grav = [oneRead[i]/100.0 for i in range(19,22)]
    tempAndCal  = oneRead[22]
    temp = tempAndCal & 0xFF
    # print("temp:",temp)
    if temp & 0x80:  temp -= 0x100

    calStat = (tempAndCal >> 8)
    sysStat = (calStat >> 6) & 0x03
    gyroStat = (calStat >> 4) & 0x03
    accelStat = (calStat >> 2) & 0x03
    magStat = calStat & 0x03
    allCalStat = (sysStat, gyroStat, accelStat, magStat)

    string_to_print = \
                      "Euler Heading: {:>6.1f}  Roll: {:>6.1f}  Pitch: {:>6.1f} |  " \
                      "Mag XYZ: {:>4.1f} {:>4.1f} {:>4.1f} | " \
                      "Gyro XYZ: {:>4.1f} {:>4.1f} {:>4.1f} | " \
                      "Accel XYZ: {:>4.1f} {:>4.1f} {:>4.1f} | " \
                      "LinAcc XYZ: {:>4.1f} {:>4.1f} {:>4.1f} | " \
                      "Temp: {:.0f}C".format(
                                             euler[0], euler[1], euler[2],
                                             mag[0], mag[1], mag[2],
                                             gyro[0], gyro[1], gyro[2],
                                             accel[0], accel[1], accel[2],
                                             linacc[0], linacc[1], linacc[2],
                                             temp)
    print(string_to_print)

    time.sleep(0.1)
  except KeyboardInterrupt:
    print("\nCtrl-C detected. Exiting..")
    break
