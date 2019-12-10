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


def calibrateMags(imu):
    time_to_wait_after_error = 0.5 # measured in seconds


    # start the calibrating process of the compass
    print("Rotate the GoPiGo3 robot in your hands until it's fully calibrated")
    try:
        magCalStatus = imu.BNO055.get_calibration_status()[3]
    except Exception as msg:
        magCalStatus = 0
    values_already_printed = []
    max_conseq_errors = 3

    while magCalStatus != 3 and max_conseq_errors > 0:
        state = ""
        if magCalStatus == 0:
            state = "not yet calibrated"
        elif magCalStatus == 1:
            state = "partially calibrated"
        elif magCalStatus == 2:
            state = "almost calibrated"

        if not magCalStatus in values_already_printed:
            print("The GoPiGo3 mags are " + state)
        values_already_printed.append(magCalStatus)

        try:
            magCalStatus = imu.BNO055.get_calibration_status()[3]
        except Exception as msg:
            max_conseq_errors -= 1
            sleep(time_to_wait_after_error)
            continue

    # if CTRL-C was triggered or if the calibration failed
    # then abort everything
    if  max_conseq_errors == 0:
        print("IMU sensor is not reacheable or kill event was triggered")
    else:
        state = "fully calibrated"
        print("The GoPiGo3 mags are " + state)
        sysCalStat,gyroCalStat,accCalStat,magCalStat = imu.BNO055.get_calibration_status()
        print("BNO055 Calibration Status (sys,gyro,acc,mag): ({},{},{},{})".format(sysCalStat,gyroCalStat,accCalStat,magCalStat))

def multiReadAndPrint(imu, cnt=100, delay=0.01):

    magReadingsX = []
    magReadingsY = []
    magReadingsZ = []
    gyroReadingsX = []
    gyroReadingsY = []
    gyroReadingsZ = []
    accelReadingsX = []
    accelReadingsY = []
    accelReadingsZ = []
    eulerReadingsH = []
    eulerReadingsR = []
    eulerReadingsP = []
    tempReadings = []

    print("\nCollecting {} Readings".format(cnt))

    for i in range(cnt):
        time.sleep(delay)  # wait for new reading to be posted

        mag  = imu.read_magnetometer()
        gyro  = imu.read_gyroscope()
        accel = imu.read_accelerometer()
        euler = imu.read_euler()
        tempReadings  += [imu.read_temperature()]

        magReadingsX += [mag[0]]
        magReadingsY += [mag[1]]
        magReadingsZ += [mag[2]]

        gyroReadingsX += [gyro[0]]
        gyroReadingsY += [gyro[1]]
        gyroReadingsZ += [gyro[2]]

        accelReadingsX += [accel[0]]
        accelReadingsY += [accel[1]]
        accelReadingsZ += [accel[2]]

        eulerReadingsH += [euler[0]]
        eulerReadingsR += [euler[1]]
        eulerReadingsP += [euler[2]]


    for i in range(cnt):
        string_to_print = \
                          "Euler Heading: {:>5.1f} Roll: {:>5.1f} Pitch: {:>5.1f} | " \
                          "Mag XYZ: {:>4.0f} {:>4.0f} {:>4.0f} | " \
                          "Gyro XYZ: {:>4.1f} {:>4.1f} {:>4.1f} | " \
                          "Accel XYZ: {:>4.1f} {:>4.1f} {:>4.1f} | " \
                          "Temp: {:.1f}C".format(
                                                    round(eulerReadingsH[i],1), round(eulerReadingsR[i],1), round(eulerReadingsP[i],1),
                                                    magReadingsX[i], magReadingsY[i], magReadingsZ[i],
                                                    round(gyroReadingsX[i],1), round(gyroReadingsY[i],1), round(gyroReadingsZ[i],1),
                                                    accelReadingsX[i], round(accelReadingsY[i],1), accelReadingsZ[i],
                                                    tempReadings[i])
        print(string_to_print)

    # clean out bad temp readings
    tempReadings = [ ele for ele in tempReadings if ele > 0 ]

    print("\nAverage for {} Readings".format(cnt))
    aveMagX = np.mean(magReadingsX)
    aveMagY = np.mean(magReadingsY)
    aveMagZ = np.mean(magReadingsZ)
    aveGyroX = np.mean(gyroReadingsX)
    aveGyroY = np.mean(gyroReadingsY)
    aveGyroZ = np.mean(gyroReadingsZ)
    aveAccelX = np.mean(accelReadingsX)
    aveAccelY = np.mean(accelReadingsY)
    aveAccelZ = np.mean(accelReadingsZ)
    aveEulerH = np.mean(eulerReadingsH)
    aveEulerR = np.mean(eulerReadingsR)
    aveEulerP = np.mean(eulerReadingsP)
    aveTemp = np.mean(tempReadings)

    string_to_print = \
                          "Euler Heading: {:>4.0f} Roll: {:>4.0f} Pitch: {:>4.0f} | " \
                          "Mag XYZ: {:>4.0f} {:>4.0f} {:>4.0f} | " \
                          "Gyro XYZ: {:>4.1f} {:>4.1f} {:>4.1f} | " \
                          "Accel XYZ: {:>4.1f} {:>4.1f} {:>4.1f} | " \
                          "Temp: {:.1f}C".format(
                                                    aveEulerH, aveEulerR, round(aveEulerP,1),
                                                    aveMagX, aveMagY, aveMagZ,
                                                    round(aveGyroX,1), round(aveGyroY,1), round(aveGyroZ,1),
                                                    aveAccelX, round(aveAccelY,1), aveAccelZ,
                                                    aveTemp)
    print(string_to_print)

def getFusion(imu):
        euler = imu.read_euler()
        linacc = imu.read_linear_acceleration()
        return euler,linacc

def readAndPrint(imu,cnt=1,delay=0.01):
    print("\nRead And Print {} times with delay: {:.3f}".format(cnt,delay))
    for i in range(cnt):

        # Read the magnetometer, gyroscope, accelerometer, euler, and temperature values
        mag    = imu.read_magnetometer()
        gyro   = imu.read_gyroscope()
        accel  = imu.read_accelerometer()
        euler  = imu.read_euler()
        linacc = imu.read_linear_acceleration()
        temp   = imu.read_temperature()

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
        time.sleep(delay)
    print("\n")

def compFilter(imu,XYZ,Vxyz,dtTimer):
        tau = 0.98
        # Get the processed values from IMU
        euler, linacc = getFusion(imu)
        if dtTimer != None:
            # Get delta time and record time for next call
            dt = time.time() - dtTimer
            dtTimer = time.time()


            # Accellerometer integration is velocity
            Vxyz[0] += linacc[0] * dt
            Vxyz[1] += linacc[1] * dt
            Vxyz[2] += linacc[2] * dt
            Vx = Vxyz[0]
            Vy = Vxyz[1]
            Vz = Vxyz[2]

            # Comp filter
            X = tau*(XYZ[0] + Vx*dt) + (1-tau)*Vx
            Y = tau*(XYZ[1] + Vy*dt) + (1-tau)*Vy
            Z = tau*(XYZ[2] + Vz*dt) + (1-tau)*Vz
        else:
            dtTimer = time.time()
            X = XYZ[0]
            Y = XYZ[1]
            Z = XYZ[2]
            Vx = Vxyz[0]
            Vy = Vxyz[1]
            Vz = Vxyz[2]

        print("Heading: {:>6.0f} XYZ: [{:>4.1f}, {:>4.1f}, {:4.1f}] Vxyz: [{:>4.1f}, {:4.1f}, {:4.1f}]".format(
                           round(euler[0],0), round(X,1), round(Y,1), round(Z,1), round(Vx,1), round(Vy,1), round(Vz,1) ), end='\r')
        return [X,Y,Z], [Vx,Vy,Vz], dtTimer

def track(imu,cnt,dT=0.010):
    XYZ=[0.0, 0.0, 0.0]
    Vxyz=[0.0, 0.0, 0,0]
    dtTimer = None
    for i in range(cnt):
        XYZ,Vxyz,dtTimer = compFilter(imu,XYZ,Vxyz,dtTimer)
        time.sleep(dT)
    return XYZ

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

        multiReadAndPrint(imu, 100,0.01)
        multiReadAndPrint(imu, 100,0.01)
        multiReadAndPrint(imu, 100,0.01)

        # calibrateMags(imu)

        # print("Place Carl on Floor")
        # time.sleep(10.0)

        # readAndPrint(2,1.0)
        # multiReadAndPrint(imu,100,0.01)

        # readAndPrint(imu,300,0.1)

        # XYZ = track(imu, 1000, 0.01)
        print("\n")

    except KeyboardInterrupt:
        print("\nCntrl-C detected. Exiting..")
        # break


# Main loop
if __name__ == '__main__':
	main()

