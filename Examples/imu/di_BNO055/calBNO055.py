#!/usr/bin/env python3
#
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
#
# Python Calibration Program for the Dexter Industries IMU Sensor
#
# Usage:
#    import calBNO055
#
#    imu = InertialMeasurementUnit(bus = "GPG3_AD1")
#    calBNO055.calibrate(imu)   # uses calData.json if preent, or guides user through first calibration
#

from __future__ import print_function
from __future__ import division

import time
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit
import numpy as np
from di_sensors import BNO055
import json


TIME_TO_WAIT_AFTER_ERROR = 0.5 # measured in seconds


def my_reset_sys(imu):
     imu.BNO055.i2c_bus.write_reg_8(BNO055.REG_SYS_TRIGGER, 0x20)
     time.sleep(0.65)

def printCalStatus(imu):
    sysCalStat,gyroCalStat,accCalStat,magCalStat = imu.BNO055.get_calibration_status()
    print("BNO055 Calibration Status (sys,gyro,acc,mag): ({},{},{},{})".format(sysCalStat,gyroCalStat,accCalStat,magCalStat))

def dumpCalDataJSON(imu):
    printCalStatus(imu)
    imu.BNO055._config_mode()
    calData = imu.BNO055.get_calibration()
    imu.BNO055.set_mode(BNO055.OPERATION_MODE_NDOF)
    with open('calData.json', 'w') as outfile:
        json.dump(calData, outfile)
    print("Wrote calData.json",calData)
    time.sleep(1.0)

def loadCalDataJSON(imu):
    with open('calData.json') as json_file:
        calData = json.load( json_file )
    # print("calData",calData)
    return calData

def loadAndSetCalDataJSON(imu):
    try:
        calData = loadCalDataJSON(imu)
        print("Switching to CONFIG_MODE")
        imu.BNO055._config_mode()
        print("Setting Calibration Data From calData.json File")
        imu.BNO055.set_calibration(calData)
        print("Setting NDOF Mode")
        imu.BNO055.set_mode(BNO055.OPERATION_MODE_NDOF)
        time.sleep(1.0)
        printCalStatus(imu)
        print("\n")
        return True
    except:
        return False

def resetBNO055(imu):
        print("Switching to CONFIG_MODE")
        imu.BNO055._config_mode()
        print("Resetting BNO055")
        my_reset_sys(imu)
        print("Setting NDOF Mode")
        imu.BNO055.set_mode(BNO055.OPERATION_MODE_NDOF)
        printCalStatus(imu)
        print("\n")
        time.sleep(1.0)

def calibrateGyros(imu):

        # start the calibrating process of the gyros
        try:
            gyroCalStatus = imu.BNO055.get_calibration_status()[1]
        except Exception as msg:
            gyroCalStatus = 0
        values_already_printed = []
        max_conseq_errors = 3

        if gyroCalStatus != 3:
            print("Do not move GoPiGo3 until Gryos are fully calibrated")

        while gyroCalStatus != 3 and max_conseq_errors > 0:
            state = ""
            if gyroCalStatus == 0:
                state = "not yet calibrated"
            elif gyroCalStatus == 1:
                state = "partially calibrated"
            elif gyroCalStatus == 2:
                state = "almost calibrated"

            if not gyroCalStatus in values_already_printed:
                print("The GoPiGo3 Gyros are " + state)
            values_already_printed.append(gyroCalStatus)

            try:
                gyroCalStatus = imu.BNO055.get_calibration_status()[1]
            except Exception as msg:
                max_conseq_errors -= 1
                time.sleep(TIME_TO_WAIT_AFTER_ERROR)
                continue

        # if CTRL-C was triggered or if the calibration failed
        # then abort everything
        if  max_conseq_errors == 0:
            print("IMU sensor is not reacheable or kill event was triggered")
        else:
            state = "fully calibrated"
            print("The GoPiGo3 Gyros are " + state)
            printCalStatus(imu)

        print("\n")


def calibrateAccel(imu):
        # start the calibrating process of the accelerometers
        try:
            accCalStatus = imu.BNO055.get_calibration_status()[2]
        except Exception as msg:
            accCalStatus = 0
        values_already_printed = []
        max_conseq_errors = 3
        if accCalStatus != 3:
            print("Turn GoPiGo3 in 45 degree increments until Accelerometers are fully calibrated")

        while accCalStatus != 3 and max_conseq_errors > 0:
            state = ""
            if accCalStatus == 0:
                state = "not yet calibrated"
            elif accCalStatus == 1:
                state = "partially calibrated"
            elif accCalStatus == 2:
                state = "almost calibrated"

            if not accCalStatus in values_already_printed:
                print("The GoPiGo3 accelerometers are " + state)
            values_already_printed.append(accCalStatus)

            try:
                accCalStatus = imu.BNO055.get_calibration_status()[2]
            except Exception as msg:
                max_conseq_errors -= 1
                time.sleep(TIME_TO_WAIT_AFTER_ERROR)
                continue

        # if CTRL-C was triggered or if the calibration failed
        # then abort everything
        if  max_conseq_errors == 0:
            print("IMU sensor is not reacheable or kill event was triggered")
        else:
            state = "fully calibrated"
            print("The GoPiGo3 accelerometers are " + state)
            printCalStatus(imu)

        print("\n")

def calibrateMags(imu):
        # start the calibrating process of the compass
        try:
            magCalStatus = imu.BNO055.get_calibration_status()[3]
        except Exception as msg:
            magCalStatus = 0
        values_already_printed = []
        max_conseq_errors = 3

        if magCalStatus != 3:
            print("Rotate the GoPiGo3 robot in your hands until it's fully calibrated")

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
                time.sleep(TIME_TO_WAIT_AFTER_ERROR)
                continue

        # if CTRL-C was triggered or if the calibration failed
        # then abort everything
        if  max_conseq_errors == 0:
            print("IMU sensor is not reacheable or kill event was triggered")
        else:
            state = "fully calibrated"
            print("The GoPiGo3 mags are " + state)
            printCalStatus(imu)

        print("\n")

def calibrateFusionDP(imu):
        # start the system calibration process
        try:
            sysCalStatus = imu.BNO055.get_calibration_status()[0]
        except Exception as msg:
            sysCalStatus = 0
        values_already_printed = []
        max_conseq_errors = 3

        if sysCalStatus != 3:
            print("Rotate the GoPiGo3 robot in your hands until it's fully calibrated")

        while sysCalStatus != 3 and max_conseq_errors > 0:
            state = ""
            if sysCalStatus == 0:
                state = "not yet calibrated"
            elif sysCalStatus == 1:
                state = "partially calibrated"
            elif sysCalStatus == 2:
                state = "almost calibrated"

            if not sysCalStatus in values_already_printed:
                print("The GoPiGo3 Fusion SYS is " + state)
            values_already_printed.append(sysCalStatus)

            try:
                sysCalStatus = imu.BNO055.get_calibration_status()[0]
            except Exception as msg:
                max_conseq_errors -= 1
                time.sleep(TIME_TO_WAIT_AFTER_ERROR)
                continue

        # if CTRL-C was triggered or if the calibration failed
        # then abort everything
        if  max_conseq_errors == 0:
            print("IMU sensor is not reacheable or kill event was triggered")
        else:
            state = "fully calibrated"
            print("The GoPiGo3 Fusion SYS is " + state)
            printCalStatus(imu)
        print("\n")


"""
Calibration in the Fast Magnetometer Calibration (FMC_ON) mode consists of the following steps:
 1) Set Config Mode
 2) Reset to clear old data
 3) Set Operation Mode to NDoF (FMC_On)
 4) Leave IMU motionless until Gyros are fully calibrated
 5) Position IMU in +X, -X, +Y, -Y, +Z, -Z to calibrate accelerometers
 6) Move IMU in random motions until mags are fully calibrated
 7) Move IMU in figure 8 pattern until Fusion SYS is fully calibrated
 8) Write Calibration Data out to file calData.json
"""
def calibrate(imu,force=False):
    # Perform calibration if demanded, or calData.json not available
    if force or (loadAndSetCalDataJSON(imu) is not True):
        # Calibration Steps
        resetBNO055(imu)
        calibrateGyros(imu)
        calibrateAccel(imu)
        calibrateMags(imu)
        calibrateFusionDP(imu)

        dumpCalDataJSON(imu)
        print("\n")
    else:
        # calibration loaded from file
        time.sleep(1.0)
        if imu.BNO055.get_calibration_status()[0] != 3:
            calibrateFusionDP(imu)
        printCalStatus(imu)
    # done





def readAndPrint(imu,cnt=1,delay=0.01):
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


def main():
    print("\nCalibration Program for the Dexter Industries IMU Sensor")
    print("    (Using SW I2C on GoPiGo3 port AD1)\n")

    imu = InertialMeasurementUnit(bus = "GPG3_AD1")
    # Note: HW I2C does not properly implement clock stretching
    #       and will result in invalid readings

    time.sleep(1.0)  # allow for all measurements to initialize


    try:
        calibrate(imu)

        while True:
            readAndPrint(imu)
        # multiReadAndPrint(imu,100,0.01)

        # readAndPrint(imu,180,0.1)

        print("\n")

    except KeyboardInterrupt:
        print("\nCntrl-C detected. Exiting..")
        # break


# Main loop
if __name__ == '__main__':
    main()

