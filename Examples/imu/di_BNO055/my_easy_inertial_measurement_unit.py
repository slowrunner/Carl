#!/usr/bin/python3

# FILE:  my_easy_inertial_measurement_unit.py

# https://www.dexterindustries.com
#
# Copyright (c) 2018 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#

# EASIER WRAPPERS FOR:
# IMU SENSOR

# MUTEX SUPPORT WHEN NEEDED
#
"""
DI Methods Implemented (Unchanged)
 - EasyIMUSensor(port="AD1", use_mutex=False)
 - imu.reconfig_bus()
 - imu.safe_calibrate()
 - imu.safe_calibration_status()
 - imu.convert_heading(in_heading)
 - imu.safe_read_euler()
 - imu.safe_read_magnetometer()
 - imu.safe_north_point()

Expanded mutex protected Methods Implemented:
 - imu.resetExceptionCount()              resset count of recent I2C exceptions
 - imu.getExceptionCount()                get number of recent I2C exceptions
 - imu.printCalStatus()                   prints sys, gyro, acc, mag status 0=not cal, 3=fully calibrated
 - imu.dumpCalDataJSON()                  writes out calibration data to ./calData.json
 - imu.loadCalDataJSON()                  returns calibration data from file ./calData.json
 - imu.loadAndSetCalDataJSON()            Resets calibrarion from data in file ./calData.json
 - imu.resetBNO055()                      reset the IMU and print calibration status
 - imu.my_safe_calibrate()                uses the NDOF SYS value instead of just mags value
 - imu.my_safe_sgam_calibration_status()  returns all four cal status: sys, gyro, accels, mags
 - imu.safe_read_gyroscope()              returns the gyroscope values x, y, z
 - imu.safe_read_accelerometer()          returns the accels values x, y, z
 - imu.safe_read_linear_acceleration()    returns the linear accel values x, y, z
 - imu_safe_read_temperature()            returns the chip temp degC

"""

# from di_sensors import inertial_measurement_unit
import my_inertial_measurement_unit as inertial_measurement_unit
from di_sensors import BNO055
from math import atan2, pi
from time import sleep
import json

'''
MUTEX HANDLING
'''
from di_sensors.easy_mutex import ifMutexAcquire, ifMutexRelease

'''
PORT TRANSLATION
'''
ports = {
    "AD1": "GPG3_AD1",
    "AD2": "GPG3_AD2"
}

'''
IMU CALIBRATION FILE NAME
'''
IMU_CAL_FILENAME = "./imuCalData.json"


class EasyIMUSensor(inertial_measurement_unit.InertialMeasurementUnit):
    '''
    Class for interfacing with the `InertialMeasurementUnit Sensor`_.

    This class compared to :py:class:`~di_sensors.inertial_measurement_unit.InertialMeasurementUnit` uses mutexes that allows a given
    object to be accessed simultaneously from multiple threads/processes.
    Apart from this difference, there may
    also be functions that are more user-friendly than the latter.
    '''

    def __init__(self, port="AD1", use_mutex=False, mode = BNO055.OPERATION_MODE_NDOF):
        """
        Constructor for initializing link with the `InertialMeasurementUnit Sensor`_.

        :param str port = "AD1": The port to which the IMU sensor gets connected to. Can also be connected to port ``"AD2"`` of a `GoPiGo3`_ robot or to any ``"I2C"`` port of any of our platforms. If you're passing an **invalid port**, then the sensor resorts to an ``"I2C"`` connection. Check the :ref:`hardware specs <hardware-interface-section>` for more information about the ports.
        :param bool use_mutex = False: When using multiple threads/processes that access the same resource/device, mutexes should be enabled.
        :raises RuntimeError: When the chip ID is incorrect. This happens when we have a device pointing to the same address, but it's not a `InertialMeasurementUnit Sensor`_.
        :raises ~exceptions.OSError: When the `InertialMeasurementUnit Sensor`_ is not reachable.

        """
        self.use_mutex = use_mutex
        self.exceptionCount = 0

        try:
            bus = ports[port]
        except KeyError:
            bus = "RPI_1SW"

        ifMutexAcquire(self.use_mutex)
        try:
            # print("INSTANTIATING ON PORT {} OR BUS {} WITH MUTEX {}".format(port, bus, use_mutex))
            super(self.__class__, self).__init__(bus = bus, mode = mode)
            # on GPG3 we ask that the IMU be at the back of the robot, facing outward
            # We do not support the IMU on GPG2  but leaving the if statement in case
            if bus != "RPI_1SW":
                self.BNO055.set_axis_remap( BNO055.AXIS_REMAP_X,
                                        BNO055.AXIS_REMAP_Z,
                                        BNO055.AXIS_REMAP_Y,
                                        BNO055.AXIS_REMAP_POSITIVE,
                                        BNO055.AXIS_REMAP_NEGATIVE,
                                        BNO055.AXIS_REMAP_POSITIVE)

        except Exception as e:
            print("Initiating error: "+str(e))
            raise
        finally:
            sleep(0.1)  # add a delay to let the IMU stabilize before control panel can pull from it
            ifMutexRelease(self.use_mutex)

    def resetExceptionCount(self):
        self.exceptionCount = 0

    def getExceptionCount(self):
        return self.exceptionCount

    def printCalStatus(self):
        sysCalStat,gyroCalStat,accCalStat,magCalStat = self.my_safe_sgam_calibration_status()
        print("BNO055 Calibration Status (sys,gyro,acc,mag): ({},{},{},{})".format(sysCalStat,gyroCalStat,accCalStat,magCalStat))

    def dumpCalDataJSON(self,verbose=False):
        if verbose:
            self.printCalStatus()
        ifMutexAcquire(self.use_mutex)
        try:
            if verbose: print("Entering IMU Config Mode")
            self.BNO055._config_mode()
            if verbose: print("Reading Cal Data From IMU")
            calData = self.BNO055.get_calibration()
            with open(IMU_CAL_FILENAME, 'w') as outfile:
                json.dump(calData, outfile)
            if verbose:
                print("Wrote {}:\n".format(IMU_CAL_FILENAME),calData)
        except Exception as e:
            self.exceptionCount += 1
            if verbose:  print("Exception {} Occurred: {}".format(self.exceptionCount,str(e)))
        finally:
            if verbose: print("Restoring NDOF Mode")
            self.BNO055.set_mode(BNO055.OPERATION_MODE_NDOF)
            ifMutexRelease(self.use_mutex)
        sleep(1.0)

    def loadCalDataJSON(self):
        ifMutexAcquire(self.use_mutex)
        try:
            with open(IMU_CAL_FILENAME) as json_file:
                calData = json.load( json_file )
            # print("calData",calData)
        except:
            self.exceptionCount += 1
        finally:
            ifMutexRelease(self.use_mutex)
        return calData

    def loadAndSetCalDataJSON(self):
        calData = loadCalDataJSON(imu)
        ifMutexAcquire(self.use_mutex)
        try:
            print("Switching to CONFIG_MODE")
            self.BNO055._config_mode()
            print("Setting Calibration Data From {} File".format(IMU_CAL_FILENAME))
            self.BNO055.set_calibration(calData)
            print("Setting NDOF Mode")
            self.BNO055.set_mode(BNO055.OPERATION_MODE_NDOF)
            time.sleep(1.0)
            status = True
        except:
            status = False
        finally:
            ifMutexRelease(self.use_mutex)
        printCalStatus(imu)
        print("\n")
        return status

    def resetBNO055(self):

        ifMutexAcquire(self.use_mutex)
        try:
            initial_mode = self.BNO055._mode
            print("save initial mode: {}".format(initial_mode))

            print("save initial units")
            initial_units = self.BNO055.i2c_bus.read_8(BNO055.REG_UNIT_SEL)  # m/s**2, DegPerSec, degC

            print("Resetting BNO055")

            # Send a thow-away command and ignore any response or I2C errors
            # just to make sure the BNO055 is in a good state and ready to accept
            # commands (this seems to be necessary after a hard power down).
            try:
                self.BNO055.i2c_bus.write_reg_8(BNO055.REG_PAGE_ID, 0)
            except IOError:
                # pass on an I2C IOError
                pass

            print("switch to config mode")
            self.BNO055._config_mode()

            print("write reset byte")
            self.BNO055.i2c_bus.write_reg_8(BNO055.REG_PAGE_ID, 0)

            print("check the chip ID")
            if BNO055.ID != self.BNO055.i2c_bus.read_8(BNO055.REG_CHIP_ID):
                raise RuntimeError("BNO055 failed to respond")

            print("reset the device using the reset command")
            self.BNO055.i2c_bus.write_reg_8(BNO055.REG_SYS_TRIGGER, 0x20)

            print("wait 650ms after reset for chip to be ready (recommended in datasheet)")
            sleep(0.65)

            print("set to normal power mode")
            self.BNO055.i2c_bus.write_reg_8(BNO055.REG_PWR_MODE, BNO055.POWER_MODE_NORMAL)

            print("default to internal oscillator")
            self.BNO055.i2c_bus.write_reg_8(BNO055.REG_SYS_TRIGGER, 0x00)

            print("set temperature source to gyroscope, as it seems to be more accurate.")
            self.BNO055.i2c_bus.write_reg_8(BNO055.REG_TEMP_SOURCE, 0x01)

            print("set the unit selection bits")
            self.BNO055.i2c_bus.write_reg_8(BNO055.REG_UNIT_SEL, initial_units)

            print("set temperature source to gyroscope, as it seems to be more accurate.")
            self.BNO055.i2c_bus.write_reg_8(BNO055.REG_TEMP_SOURCE, 0x01)

            print("restore mode")
            self.BNO055.set_mode(initial_mode)
        except:
            raise RuntimeError("BNO055 reset failure")
        finally:
            ifMutexRelease(self.use_mutex)
        sleep(1.0)
        print("BNO055 Reset Complete")




    def reconfig_bus(self):
        """
        Use this method when the `InertialMeasurementUnit Sensor`_ becomes unresponsive but it's still plugged into the board.
        There will be times when due to improper electrical contacts, the link between the sensor and the board gets disrupted - using this method restablishes the connection.

        .. note::

           Sometimes the sensor won't work just by calling this method - in this case, switching the port will do the job. This is something that happens
           very rarely, so there's no need to worry much about this scenario.


        """

        ifMutexAcquire(self.use_mutex)
        self.BNO055.i2c_bus.reconfig_bus()
        ifMutexRelease(self.use_mutex)

    def safe_calibrate(self):
        """
        Once called, the method returns when the magnemometers of the `InertialMeasurementUnit Sensor`_ gets fully calibrated. Rotate the sensor in the air to help the sensor calibrate faster.

        .. note::
           Also, this method is not used to trigger the process of calibrating the sensor (the IMU does that automatically),
           but its purpose is to block a given script until the sensor reports it has fully calibrated.

           If you wish to block your code until the sensor calibrates and still have control over your script, use
           :py:meth:`~di_sensors.easy_inertial_measurement_unit.EasyIMUSensor.safe_calibration_status` method along with a ``while`` loop to continuously check it.

        """

        status = -1
        while status < 3:
            ifMutexAcquire(self.use_mutex)
            try:
                new_status = self.BNO055.get_calibration_status()[3]
            except:
                new_status = -1
            finally:
                ifMutexRelease(self.use_mutex)
            if new_status != status:
                status = new_status

    def my_safe_calibrate(self):
        """
        Once called, the method returns when the NDOF SYS of the `InertialMeasurementUnit Sensor`_ gets fully calibrated.
        Rotate the sensor in the air to two orthoganal directions of each axis.

        .. note::
           Also, this method is not used to trigger the process of calibrating the sensor (the IMU does that automatically),
           but its purpose is to block a given script until the sensor reports it has fully calibrated.

           If you wish to block your code until the sensor calibrates and still have control over your script, use
           :py:meth:`my_easy_inertial_measurement_unit.EasyIMUSensor.my_safe_sgam_calibration_status` method along with a ``while`` loop to continuously check it.

        """

        status = -1
        while status < 3:
            ifMutexAcquire(self.use_mutex)
            try:
                new_status = self.BNO055.get_calibration_status()[0]
            except Exception as e:
                new_status = -1
                print("get_calibration_status()[0] Exception {}".format(str(e)))
                self.exceptionCount +=1
            finally:
                ifMutexRelease(self.use_mutex)
            if new_status != status:
                status = new_status

    def safe_calibration_status(self):
        """
        Returns the calibration level of the mags of the `InertialMeasurementUnit Sensor`_.

        :returns: Calibration level of the mags. Range is **0-3** and **-1** is returned when the sensor can't be accessed.
        :rtype: int

        """
        ifMutexAcquire(self.use_mutex)
        try:
            status = self.BNO055.get_calibration_status()[3]
        except Exception as e:
            status = -1
        finally:
            ifMutexRelease(self.use_mutex)
        return status

    def my_safe_sgam_calibration_status(self):
        """
        Returns the calibration levels of the `InertialMeasurementUnit Sensor`_.

        :returns: Calibration levels sysCal, gyroCal, accCal, magCal Range is **0-3** and **-1** is returned when the sensor can't be accessed.
        :rtype: int

        """
        ifMutexAcquire(self.use_mutex)
        try:
            sysCal, gyroCal, accCal, magCal = self.BNO055.get_calibration_status()
        except Exception as e:
            sysCal = -1
            gyroCal = -1
            accCal = -1
            magCal = -1
        finally:
            ifMutexRelease(self.use_mutex)
        return sysCal, gyroCal, accCal, magCal


    def convert_heading(self, in_heading):
        """
        This method takes in a heading in degrees and return the name of the corresponding heading.
        :param float in_heading: the value in degree that needs to be converted to a string.

        :return: The heading of the sensor as a string.
        :rtype: str

        The possible strings that can be returned are: ``"North"``, ``"North East"``, ``"East"``,
        ``"South East"``, ``"South"``, ``"South West"``, ``"West"``, ``"North West"``, ``"North"``.

        .. note::

           First use :py:meth:`~di_sensors.easy_inertial_measurement_unit.EasyIMUSensor.safe_calibrate` or :py:meth:`~di_sensors.easy_inertial_measurement_unit.EasyIMUSensor.safe_calibration_status`
           methods to determine if the magnetometer sensor is fully calibrated.

        """

        headings = ["North", "North East",
                    "East", "South East",
                    "South", "South West",
                    "West", "North West",
                    "North"]

        nb_headings = len(headings)-1 # North is listed twice
        heading_index = int(round(in_heading/(360.0/nb_headings),0))
        # sometimes the IMU will return a in_heading of -1000 and higher.
        if heading_index < 0:
            heading_index = 0
        # print("heading {} index {}".format(in_heading, heading_index))
        # print(" {} ".format( headings[heading_index]))
        return(headings[heading_index])

    def safe_read_euler(self):
        """
        Read the absolute orientation.

        :returns: Tuple of euler angles in degrees of *heading*, *roll* and *pitch*.
        :rtype: (float,float,float)
        :raises ~exceptions.OSError: When the sensor is not reachable.

        """

        ifMutexAcquire(self.use_mutex)
        try:
            x, y, z = self.read_euler()
        except Exception as e:
            # print("safe read euler: {}".format(str(e)))
            x, y, z = 0, 0, 0
            self.exceptionCount += 1
            # raise
        finally:
            ifMutexRelease(self.use_mutex)
        return x,y,z

    def safe_read_gyroscope(self):
        """
        Read the gyro values.

        :returns: Tuple of angular rotation in degrees about *X*, *Y* and *Z* axis.
        :rtype: (float,float,float)

        """

        ifMutexAcquire(self.use_mutex)
        try:
            x, y, z = self.read_gyroscope()
        except Exception as e:
            # print("safe read gyros: {}".format(str(e)))
            self.exceptionCount += 1
            x, y, z = 0, 0, 0
        finally:
            ifMutexRelease(self.use_mutex)
        return x,y,z

    def safe_read_magnetometer(self):
        """
        Read the magnetometer values.

        :returns: Tuple containing X, Y, Z values in *micro-Teslas* units. You can check the X, Y, Z axes on the sensor itself.
        :rtype: (float,float,float)

        .. note::

           In case of an exception occurring within this method, a tuple of 3 elements where all values are set to **0** is returned.

        """
        ifMutexAcquire(self.use_mutex)
        try:
            x, y, z = self.read_magnetometer()
        except Exception as e:
            x, y, z = 0, 0, 0
            self.exceptionCount += 1
        finally:
            ifMutexRelease(self.use_mutex)
        return x,y,z

    def safe_read_accelerometer(self):
        """
        Read the accelerometer values.

        :returns: Tuple of acceleration in degrees along *X*, *Y* and *Z* axis (includes gravitational).
        :rtype: (float,float,float)

        """

        ifMutexAcquire(self.use_mutex)
        try:
            x, y, z = self.read_accelerometer()
        except Exception as e:
            x, y, z = 0, 0, 0
            self.exceptionCount += 1
        finally:
            ifMutexRelease(self.use_mutex)
        return x,y,z

    def safe_read_linear_acceleration(self):
        """
        Read the accelerometer values from movement without gravitational acceleration.

        :returns: Tuple of acceleration in degrees along *X*, *Y* and *Z* axis (includes gravitational).
        :rtype: (float,float,float)

        """

        ifMutexAcquire(self.use_mutex)
        try:
            x, y, z = self.read_linear_acceleration()
        except Exception as e:
            x, y, z = 0, 0, 0
            self.exceptionCount += 1
        finally:
            ifMutexRelease(self.use_mutex)
        return x,y,z

    def safe_read_temperature(self):
        """
        Read chip temperature

        :returns: Tuple of temperature in degC
        :rtype: float

        """

        ifMutexAcquire(self.use_mutex)
        try:
            temp = self.read_temperature()
        except Exception as e:
            temp = 0.0
            self.exceptionCount += 1
        finally:
            ifMutexRelease(self.use_mutex)
        return temp

    def safe_north_point(self):
        """
        Determines the heading of the north point.
        This function doesn't take into account the declination.

        :return: The heading of the north point measured in degrees. The north point is found at **0** degrees.
        :rtype: int

        .. note::

           In case of an exception occurring within this method, **0** is returned.

        """
        ifMutexAcquire(self.use_mutex)
        try:
            x, y, z = self.read_magnetometer()
        except:
            x, y, z = 0,0,0
        finally:
            ifMutexRelease(self.use_mutex)

        # using the x and z axis because the sensor is mounted vertically
        # the sensor's top face is oriented towards the front of the robot

        heading = -atan2(-x, z) * 180 / pi

        # adjust it to 360 degrees range

        if heading < 0:
            heading += 360
        elif heading > 360:
            heading -= 360

        return heading
