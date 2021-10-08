#
# FILE:  ros_safe_inertial_measurement_unit.py

# With kudos to https://www.dexterindustries.com
#
# Portions Copyright (c) 2020 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#

"""
  Modification and extensions by Alan McDonley

  EASIER WRAPPERS FOR IMU SENSOR
  MUTEX SUPPORT WHEN NEEDED
  Allow non NDOF modes
  Allow SW Obj init without HW initialization
  Defaults to no axis remap for ROS

  NOTE: DI IMU Hardware
   - Y is direction of arrow head
   - X is toward right side when head up looking at the chip side
   - Z is coming at you when looking at the chip side

  DI IMU For ROS On GoPiGo3 (No axis remap needed if mounted like this)
   - Mount with chip side up, arrow head pointing to left side of bot
   - X is forward
   - Y is toward left side
   - Z is up


DI Methods Implemented (Unchanged from easy_inertial_measurement_unit.py)
 - imu.reconfig_bus()
 - imu.safe_calibration_status()
 - imu.convert_heading(in_heading)
 - imu.safe_read_euler()
 - imu.safe_read_magnetometer()
 - imu.safe_north_point()

Expanded mutex protected Methods Implemented:
 - SafeIMUSensor()                        EasyIMUSensor() that allows all operation modes
 - imu.resetExceptionCount()              reset count of recent I2C exceptions
 - imu.getExceptionCount()                get number of recent I2C exceptions
 - imu.printCalStatus()                   prints sys, gyro, acc, mag status 0=not cal, 3=fully calibrated
 - imu.dumpCalDataJSON()                  writes out calibration data to ./calData.json
 - imu.loadCalDataJSON()                  returns calibration data from file ./calData.json
 - imu.loadAndSetCalDataJSON()            Resets calibrarion from data in file ./calData.json
 - imu.safe_resetBNO055()                 reset the IMU and print calibration status
 - imu.safe_axis_remap()                  remap axis for actual chip orientation (default GoPiGo3)
 - imu.safe_calibrate()                   uses the NDOF SYS value instead of just mags value as in DI easy_i_m_u
 - imu.safe_sgam_calibration_status()  returns all four cal status: sys, gyro, accels, mags
 - imu.safe_read_quaternion()             returns the quaternian values x, y, z, w
 - imu.safe_read_gyroscope()              returns the gyroscope values x, y, z
 - imu.safe_read_accelerometer()          returns the accels values x, y, z
 - imu.safe_read_linear_acceleration()    returns the linear accel values x, y, z
 - imu.safe_read_temperature()            returns the chip temp degC
 - imu.safe_set_mode()                    change operation mode
 - imu.sefe_get_mode()                    check current operation mode
 - imu.safe_get_system_status()           opt run self test and return system status
 - imu.safe_get_operation_mode()          returns operating mode of hardware
 - imu.safe_get_op_mode_str()             returns string name of hardware operating mode
 - imu.safe_read_imu()                    returns tuple of all readings
 - imu.safe_print_imu_readings()          prints tuple of all readings passed in
 - imu.readAndPrint()                     read and print with options for num times, delay, and EOL
"""

from __future__ import print_function
from __future__ import division


# from di_sensors import inertial_measurement_unit
import ros_inertial_measurement_unit as inertial_measurement_unit
import rosBNO055 as BNO055
from math import atan2, pi
from time import sleep
import json
import sys
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
OP_MODE_STRINGS = ["CONFIG", "ACCONLY", "MAGONLY", "GYRONLY", "ACCMAG", "ACCGYRO", "MAGGYRO", "AMG", "IMUPLUS", "COMPASS", "M4G", "NDOF_FMC_OFF", "NDOF"]


class SafeIMUSensor(inertial_measurement_unit.InertialMeasurementUnit):
    '''
    "Safe for MultiProcessing" Class for interfacing with the `InertialMeasurementUnit Sensor`_.

    This class compared to :py:class:`~di_sensors.inertial_measurement_unit.InertialMeasurementUnit` uses mutexes that allows a given
    object to be accessed simultaneously from multiple threads/processes.

    Additionally support for:
        Variable exceptionCount: tracks "soft" I2C exceptions
        Modes other than full fusion OPERATION_MODE_NDOF
    '''

    def __init__(self, port="AD1", use_mutex=True, mode = BNO055.OPERATION_MODE_NDOF, verbose = False, init=True):
        """Constructor for initializing link with the `InertialMeasurementUnit Sensor`_.

        :param str port = "AD1": The port to which the IMU sensor gets connected to. Can also be connected to port ``"AD2"`` of a `GoPiGo3`_ robot or to any ``"I2C"`` port of any of our platforms. If you're passing an **invalid port**, then the sensor resorts to an ``"I2C"`` connection. Check the :ref:`hardware specs <hardware-interface-section>` for more information about the ports.
        :param bool use_mutex = True: Enables multiple threads/processes to access the same resource/device.
        ;param const mode = BNO055.OPERATION_MODE_NDOF:  Default is full fusion mode using gyros, accellerometers, and magnetometers.
        :param bool init = True: Enable/Disables chip initialization.  False creates software object but does not affect hardware configuration or mode.
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
            if verbose:
                if (init==True): 
                    print("SafeIMUSensor INSTANTIATING ON PORT {} OR BUS {} WITH MUTEX {} TO MODE {} INIT {}".format(port, bus, use_mutex, OP_MODE_STRINGS[mode], init))
                else:
                    print("SafeIMUSensor INSTANTIATING ON PORT {} OR BUS {} WITH MUTEX {} INIT {} (no mode change)".format(port, bus, use_mutex, init))

            if sys.version_info[0] < 3: 
                super(self.__class__, self).__init__(bus = bus, mode = mode, verbose = verbose, init=init)
            else:
                super().__init__(bus = bus, mode = mode, verbose = verbose, init=init)

            # NON-ROS: on GPG3 we ask that the IMU be at the back of the robot, facing outward
            # if (bus != "RPI_1SW") and (init==True):
            #     if verbose: print("Performing axis_remap for GoPiGo3 Configuration")
            #     self.BNO055.set_axis_remap( BNO055.AXIS_REMAP_X,
            #                             BNO055.AXIS_REMAP_Z,
            #                             BNO055.AXIS_REMAP_Y,
            #                             BNO055.AXIS_REMAP_POSITIVE,
            #                             BNO055.AXIS_REMAP_NEGATIVE,
            #                             BNO055.AXIS_REMAP_POSITIVE,verbose=verbose)
            #     if verbose: print("Completed axis_remap")

        except Exception as e:
            print("Initiating error: "+str(e))
            raise
        finally:
            sleep(0.1)  # add a delay to let the IMU stabilize before control panel can pull from it
            ifMutexRelease(self.use_mutex)
        if verbose: print("SafeIMUSensor Instantiation Complete\n")


    def resetExceptionCount(self):
        self.exceptionCount = 0

    def getExceptionCount(self):
        return self.exceptionCount

    def printCalStatus(self, cr=True):
        sysCalStat,gyroCalStat,accCalStat,magCalStat = self.safe_sgam_calibration_status()
        if cr:
            print("BNO055 Calibration Status (sys,gyro,acc,mag): ({},{},{},{})".format(sysCalStat,gyroCalStat,accCalStat,magCalStat))
        else:
            print("BNO055 Calibration Status (sys,gyro,acc,mag): ({},{},{},{})".format(sysCalStat,gyroCalStat,accCalStat,magCalStat),end="\r")

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
            print("Restoring Operation Mode")
            self.BNO055._operation_mode()
            sleep(1.0)
            status = True
        except:
            status = False
        finally:
            ifMutexRelease(self.use_mutex)
        printCalStatus(imu)
        print("\n")
        return status

    def safe_get_mode(self):
        ifMutexAcquire(self.use_mutex)
        mode = self.BNO055._mode
        ifMutexRelease(self.use_mutex)
        return mode

    def safe_set_mode(self, mode, verbose=False):
        success = False
        if verbose: 
            print("\nEntering safe_set_mode()")
            print("Existing Mode:{}".format(self.safe_get_mode()))
        ifMutexAcquire(self.use_mutex)

        # Send a thow-away command and ignore any response or I2C errors
        # just to make sure the BNO055 is in a good state and ready to accept
        # commands (this seems to be necessary).
        try:
            self.BNO055.i2c_bus.write_reg_8(BNO055.REG_PAGE_ID, 0)
        except IOError:
            self.exceptionCount +=1
            # pass on an I2C IOError
            pass


        try:
            # self.BNO055._config_mode()
            # time.sleep(0.05)

            self._mode = mode
            self.BNO055.set_mode(mode)
            # time.sleep(0.05)
            success = True
        except Exception as e:
            print("set_mode exception:{}".format(str(e)))
            self.exceptionCount +=1
        finally:
            ifMutexRelease(self.use_mutex)
            if verbose:
                print("Current Mode:{}".format(self.safe_get_mode()))
                print("safe_set_mode() Returning success: {}\n".format(success))
        return success

    def safe_resetBNO055(self,verbose=False):
        if verbose: print("\nResetting BNO055")
        ifMutexAcquire(self.use_mutex)
        try:
            initial_mode = self.BNO055._mode
            if verbose:
                print("save initial mode: {}".format(initial_mode))

                print("save initial units")
            initial_units = self.BNO055.i2c_bus.read_8(BNO055.REG_UNIT_SEL)  # m/s**2, DegPerSec, degC

            if verbose: print("Resetting BNO055")

            # Send a thow-away command and ignore any response or I2C errors
            # just to make sure the BNO055 is in a good state and ready to accept
            # commands (this seems to be necessary after a hard power down).
            try:
                self.BNO055.i2c_bus.write_reg_8(BNO055.REG_PAGE_ID, 0)
            except IOError:
                # pass on an I2C IOError
                pass

            if verbose: print("switch to config mode")
            self.BNO055._config_mode()

            if verbose: print("write reset byte")
            self.BNO055.i2c_bus.write_reg_8(BNO055.REG_PAGE_ID, 0)

            if verbose: print("check the chip ID")
            if BNO055.ID != self.BNO055.i2c_bus.read_8(BNO055.REG_CHIP_ID):
                raise RuntimeError("BNO055 failed to respond")

            if verbose: print("reset the device using the reset command")
            self.BNO055.i2c_bus.write_reg_8(BNO055.REG_SYS_TRIGGER, 0x20)

            if verbose: print("wait 650ms after reset for chip to be ready (recommended in datasheet)")
            sleep(0.65)

            if verbose: print("set to normal power mode")
            self.BNO055.i2c_bus.write_reg_8(BNO055.REG_PWR_MODE, BNO055.POWER_MODE_NORMAL)

            if verbose: print("default to internal oscillator")
            self.BNO055.i2c_bus.write_reg_8(BNO055.REG_SYS_TRIGGER, 0x00)

            if verbose: print("set temperature source to gyroscope, as it seems to be more accurate.")
            self.BNO055.i2c_bus.write_reg_8(BNO055.REG_TEMP_SOURCE, 0x01)

            if verbose: print("set the unit selection bits")
            self.BNO055.i2c_bus.write_reg_8(BNO055.REG_UNIT_SEL, initial_units)

            if verbose: print("restore mode {}".format(initial_mode))
            self.BNO055.set_mode(initial_mode)

            if verbose: print("current mode: {}".format(self.BNO055._mode))

        except:
            raise RuntimeError("BNO055 reset failure")
        finally:
            ifMutexRelease(self.use_mutex)
        sleep(1.0)
        if verbose: print("safe_resetBNO055 Complete\n\n")

    # NON-ROS: Remap Axis for actual orientation, Default: GoPiGo3 Point-Up, Chip-Toward Front
    # NON-ROS: Use safe_axis_remap after safe_resetBNO055()
    def safe_axis_remap(self,x=BNO055.AXIS_REMAP_X, y=BNO055.AXIS_REMAP_Z, z=BNO055.AXIS_REMAP_Y, \
                             xo=BNO055.AXIS_REMAP_POSITIVE, yo=BNO055.AXIS_REMAP_NEGATIVE, zo=BNO055.AXIS_REMAP_POSITIVE, \
                             verbose=False):
                if verbose:
                    print("Performing safe_axis_remap()")
                    if ((x==BNO055.AXIS_REMAP_X) and
                       (y==BNO055.AXIS_REMAP_Z) and
                       (z==BNO055.AXIS_REMAP_Y) and
                       (xo==BNO055.AXIS_REMAP_POSITIVE) and
                       (yo==BNO055.AXIS_REMAP_NEGATIVE) and
                       (zo==BNO055.AXIS_REMAP_POSITIVE)):
                        print("For GoPiGo3 Configuration: Point-Up, Chip-Toward Front")
                self.BNO055.set_axis_remap( x,y,z, xo,yo,zo, verbose=verbose)
                if verbose: print("Completed safe_axis_remap")



    def reconfig_bus(self):
        """Use this method when the `InertialMeasurementUnit Sensor`_ becomes unresponsive but it's still plugged into the board.
        There will be times when due to improper electrical contacts, the link between the sensor and the board gets disrupted - using this method restablishes the connection.

        .. note::

           Sometimes the sensor won't work just by calling this method - in this case, switching the port will do the job. This is something that happens
           very rarely, so there's no need to worry much about this scenario.


        """

        ifMutexAcquire(self.use_mutex)
        self.BNO055.i2c_bus.reconfig_bus()
        ifMutexRelease(self.use_mutex)

    def safe_calibrate(self):
        """Once called, the method returns when the magnemometers of the `InertialMeasurementUnit Sensor`_ gets fully calibrated. Rotate the sensor in the air to help the sensor calibrate faster.

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

    def safe_calibrate(self, verbose=False):
        """Once called, the method returns when the NDOF SYS of the `InertialMeasurementUnit Sensor`_ gets fully calibrated.
        Rotate the sensor in the air to two orthoganal directions of each axis.

        .. note::
           Also, this method is not used to trigger the process of calibrating the sensor (the IMU does that automatically),
           but its purpose is to block a given script until the sensor reports it has fully calibrated.

           If you wish to block your code until the sensor calibrates and still have control over your script, use
           :py:meth:`ros_safe_inertial_measurement_unit.SafeIMUSensor.safe_sgam_calibration_status` method along with  
            a ``while`` loop to continuously check it.

        """

        status = -1
        while status < 3:
            ifMutexAcquire(self.use_mutex)
            try:
                new_status = self.BNO055.get_calibration_status()[0]
                if verbose: print("Sys Status: {}".format(new_status),end='\r')
            except Exception as e:
                new_status = -1
                print("get_calibration_status()[0] Exception {}".format(str(e)))
                self.exceptionCount +=1
            finally:
                ifMutexRelease(self.use_mutex)
            if new_status != status:
                status = new_status

    def safe_calibration_status(self):
        """Returns the calibration level of the mags of the `InertialMeasurementUnit Sensor`_.

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

    def safe_sgam_calibration_status(self):
        """Returns all calibration levels of the `InertialMeasurementUnit Sensor`_.

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
        """This method takes in a heading in degrees and return the name of the corresponding heading.
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
        """Read the absolute orientation.

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

    def safe_read_quaternion(self):
        """Read the quaternion values.

        :returns: current orientation as tuple of X, Y, Z, W quaternion values..
        :rtype: (float,float,float,float)
        :raises ~exceptions.OSError: When the sensor is not reachable.

        """

        ifMutexAcquire(self.use_mutex)
        try:
            x, y, z, w = self.read_quaternion()
        except Exception as e:
            # print("safe read quaternion: {}".format(str(e)))
            x, y, z, w = 0, 0, 0, 0
            self.exceptionCount += 1
            # raise
        finally:
            ifMutexRelease(self.use_mutex)
        return x,y,z,w

    def safe_read_gyroscope(self):
        """Read the gyro values.

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
        """Read the magnetometer values.

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
        """Read the accelerometer values.

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
        """Read the accelerometer values from movement without gravitational acceleration.

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
        """Read chip temperature

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
        """Determines the heading of the north point.
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

    def safe_get_system_status(self, run_self_test=True):

        """Get the sensor system status
        Keyword arguments:
        run_self_test (default True) -- Run a self test? This will make the sensor go into config mode which will stop the fusion engine.

        :returns: a tuple with status information. Three values will be returned:
          - System status register value with the following meaning:
              0 = Idle
              1 = System Error
              2 = Initializing Peripherals
              3 = System Initialization
              4 = Executing Self-Test
              5 = Sensor fusion algorithm running
              6 = System running without fusion algorithms
          - Self test result register value with the following meaning:
              Bit value: 1 = test passed, 0 = test failed
              Bit 0 = Accelerometer self test
              Bit 1 = Magnetometer self test
              Bit 2 = Gyroscope self test
              Bit 3 = MCU self test
              Value of 0x0F = all good!
          - System error register value with the following meaning:
              0 = No error
              1 = Peripheral initialization error
              2 = System initialization error
              3 = Self test result failed
              4 = Register map value out of range
              5 = Register map address out of range
              6 = Register map write error
              7 = BNO low power mode not available for selected operation mode
              8 = Accelerometer power mode not available
              9 = Fusion algorithm configuration error
             10 = Sensor configuration error
        """


        ifMutexAcquire(self.use_mutex)
        try:
            status = self.BNO055.get_system_status(run_self_test=run_self_test)
        except Exception as e:
            status = (1,0,3)
            print("safe get system status:{}".format(str(e)))
            self.exceptionCount += 1
        finally:
            ifMutexRelease(self.use_mutex)
        return status

    def safe_get_operation_mode(self):
        """Read chip operating mode

        :returns: REG_OPR_MODE
        :rtype: byte

        """

        ifMutexAcquire(self.use_mutex)
        try:
            op_mode = self.BNO055.get_operation_mode()
        except Exception as e:
            op_mode = 0  # config mode
            self.exceptionCount += 1
        finally:
            ifMutexRelease(self.use_mutex)
        return op_mode


    def safe_get_op_mode_str(self):

        """Read chip operating mode
        :returns: REG_OPR_MODE string name:

             0=CONFIG
             1=ACCONLY
             2=MAGONLY
             3=GYRONLY
             4=ACCMAG
             5=ACCGYRO
             6=MAGGYRO
             7=AMG
             8=IMUPLUS
             9=COMPASS
             10=M4G
             11=NDOF_FMC_OFF
             12=NDOF
        """
        op_mode_str = OP_MODE_STRINGS[self.safe_get_operation_mode()]
        return op_mode_str

    def printHeading(self,cr = True):
        euler = self.safe_read_euler()

        string_to_print = "Heading: {:>5.1f} ".format(round(euler[0],1))
        if cr:
            print(string_to_print)
        else:
            print(string_to_print, end='\r')

    def safe_readIMU(self):
        # Read the magnetometer, gyroscope, accelerometer, euler, and temperature values
        mag    = self.safe_read_magnetometer()
        gyro   = self.safe_read_gyroscope()
        accel  = self.safe_read_accelerometer()
        euler  = self.safe_read_euler()
        linacc = self.safe_read_linear_acceleration()
        temp   = self.safe_read_temperature()
        return [mag, gyro, accel, euler, linacc, temp]

    def printReadings(self, readingsMGAELT, cr = False):
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


    def readAndPrint(self,cnt=1,delay=0.02,cr = False):
        if cnt == 0:
            while True:
                self.printReadings(self.safe_readIMU(),cr)
                sleep(delay)
        else:
            for i in range(cnt):
                self.printReadings(self.safe_readIMU(),cr)
                sleep(delay)

