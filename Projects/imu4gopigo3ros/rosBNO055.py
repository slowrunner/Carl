# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python drivers for the BNO055 IMU sensor
#
# Modifications by Alan for ROS and to allow NON-NDOF modes
#
# set_mode() sets self._mode
#

from __future__ import print_function
from __future__ import division

import di_i2c
import time

# Constants

# I2C addresses
ADDRESS_A                   = 0x28
ADDRESS_B                   = 0x29

ID                          = 0xA0

# Page id register definition
REG_PAGE_ID                 = 0x07

# PAGE0 REGISTER DEFINITION START
REG_CHIP_ID                 = 0x00
REG_ACCEL_REV_ID            = 0x01
REG_MAG_REV_ID              = 0x02
REG_GYRO_REV_ID             = 0x03
REG_SW_REV_ID_LSB           = 0x04
REG_SW_REV_ID_MSB           = 0x05
REG_BL_REV_ID               = 0x06

# Accel data register
REG_ACCEL_DATA_X_LSB        = 0x08
REG_ACCEL_DATA_X_MSB        = 0x09
REG_ACCEL_DATA_Y_LSB        = 0x0A
REG_ACCEL_DATA_Y_MSB        = 0x0B
REG_ACCEL_DATA_Z_LSB        = 0x0C
REG_ACCEL_DATA_Z_MSB        = 0x0D

# Mag data register
REG_MAG_DATA_X_LSB          = 0x0E
REG_MAG_DATA_X_MSB          = 0x0F
REG_MAG_DATA_Y_LSB          = 0x10
REG_MAG_DATA_Y_MSB          = 0x11
REG_MAG_DATA_Z_LSB          = 0x12
REG_MAG_DATA_Z_MSB          = 0x13

# Gyro data registers
REG_GYRO_DATA_X_LSB         = 0x14
REG_GYRO_DATA_X_MSB         = 0x15
REG_GYRO_DATA_Y_LSB         = 0x16
REG_GYRO_DATA_Y_MSB         = 0x17
REG_GYRO_DATA_Z_LSB         = 0x18
REG_GYRO_DATA_Z_MSB         = 0x19

# Euler data registers
REG_EULER_H_LSB             = 0x1A
REG_EULER_H_MSB             = 0x1B
REG_EULER_R_LSB             = 0x1C
REG_EULER_R_MSB             = 0x1D
REG_EULER_P_LSB             = 0x1E
REG_EULER_P_MSB             = 0x1F

# Quaternion data registers
REG_QUATERNION_DATA_W_LSB   = 0x20
REG_QUATERNION_DATA_W_MSB   = 0x21
REG_QUATERNION_DATA_X_LSB   = 0x22
REG_QUATERNION_DATA_X_MSB   = 0x23
REG_QUATERNION_DATA_Y_LSB   = 0x24
REG_QUATERNION_DATA_Y_MSB   = 0x25
REG_QUATERNION_DATA_Z_LSB   = 0x26
REG_QUATERNION_DATA_Z_MSB   = 0x27

# Linear acceleration data registers
REG_LINEAR_ACCEL_DATA_X_LSB = 0x28
REG_LINEAR_ACCEL_DATA_X_MSB = 0x29
REG_LINEAR_ACCEL_DATA_Y_LSB = 0x2A
REG_LINEAR_ACCEL_DATA_Y_MSB = 0x2B
REG_LINEAR_ACCEL_DATA_Z_LSB = 0x2C
REG_LINEAR_ACCEL_DATA_Z_MSB = 0x2D

# Gravity data registers
REG_GRAVITY_DATA_X_LSB      = 0x2E
REG_GRAVITY_DATA_X_MSB      = 0x2F
REG_GRAVITY_DATA_Y_LSB      = 0x30
REG_GRAVITY_DATA_Y_MSB      = 0x31
REG_GRAVITY_DATA_Z_LSB      = 0x32
REG_GRAVITY_DATA_Z_MSB      = 0x33

# Temperature data register
REG_TEMP                    = 0x34

# Status registers
REG_CALIB_STAT              = 0x35
REG_SELFTEST_RESULT         = 0x36
REG_INTR_STAT               = 0x37

REG_SYS_CLK_STAT            = 0x38
REG_SYS_STAT                = 0x39
REG_SYS_ERR                 = 0x3A

# Unit selection register
REG_UNIT_SEL                = 0x3B
UNIT_SEL_ACC  = 0x01
UNIT_SEL_GYR  = 0x02
UNIT_SEL_EUL  = 0x04
UNIT_SEL_TEMP = 0x10
UNIT_SEL_ORI  = 0x80

REG_DATA_SELECT             = 0x3C

# Mode registers
REG_OPR_MODE                = 0x3D
REG_PWR_MODE                = 0x3E

REG_SYS_TRIGGER             = 0x3F
REG_TEMP_SOURCE             = 0x40

# Axis remap registers
REG_AXIS_MAP_CONFIG         = 0x41
REG_AXIS_MAP_SIGN           = 0x42

# Axis remap values
AXIS_REMAP_X                = 0x00
AXIS_REMAP_Y                = 0x01
AXIS_REMAP_Z                = 0x02
AXIS_REMAP_POSITIVE         = 0x00
AXIS_REMAP_NEGATIVE         = 0x01

# SIC registers
REG_SIC_MATRIX_0_LSB        = 0x43
REG_SIC_MATRIX_0_MSB        = 0x44
REG_SIC_MATRIX_1_LSB        = 0x45
REG_SIC_MATRIX_1_MSB        = 0x46
REG_SIC_MATRIX_2_LSB        = 0x47
REG_SIC_MATRIX_2_MSB        = 0x48
REG_SIC_MATRIX_3_LSB        = 0x49
REG_SIC_MATRIX_3_MSB        = 0x4A
REG_SIC_MATRIX_4_LSB        = 0x4B
REG_SIC_MATRIX_4_MSB        = 0x4C
REG_SIC_MATRIX_5_LSB        = 0x4D
REG_SIC_MATRIX_5_MSB        = 0x4E
REG_SIC_MATRIX_6_LSB        = 0x4F
REG_SIC_MATRIX_6_MSB        = 0x50
REG_SIC_MATRIX_7_LSB        = 0x51
REG_SIC_MATRIX_7_MSB        = 0x52
REG_SIC_MATRIX_8_LSB        = 0x53
REG_SIC_MATRIX_8_MSB        = 0x54

# Accelerometer Offset registers
REG_ACCEL_OFFSET_X_LSB      = 0x55
REG_ACCEL_OFFSET_X_MSB      = 0x56
REG_ACCEL_OFFSET_Y_LSB      = 0x57
REG_ACCEL_OFFSET_Y_MSB      = 0x58
REG_ACCEL_OFFSET_Z_LSB      = 0x59
REG_ACCEL_OFFSET_Z_MSB      = 0x5A

# Magnetometer Offset registers
REG_MAG_OFFSET_X_LSB        = 0x5B
REG_MAG_OFFSET_X_MSB        = 0x5C
REG_MAG_OFFSET_Y_LSB        = 0x5D
REG_MAG_OFFSET_Y_MSB        = 0x5E
REG_MAG_OFFSET_Z_LSB        = 0x5F
REG_MAG_OFFSET_Z_MSB        = 0x60

# Gyroscope Offset registers
REG_GYRO_OFFSET_X_LSB       = 0x61
REG_GYRO_OFFSET_X_MSB       = 0x62
REG_GYRO_OFFSET_Y_LSB       = 0x63
REG_GYRO_OFFSET_Y_MSB       = 0x64
REG_GYRO_OFFSET_Z_LSB       = 0x65
REG_GYRO_OFFSET_Z_MSB       = 0x66

# Radius registers
REG_ACCEL_RADIUS_LSB        = 0x67
REG_ACCEL_RADIUS_MSB        = 0x68
REG_MAG_RADIUS_LSB          = 0x69
REG_MAG_RADIUS_MSB          = 0x6A

# Power modes
POWER_MODE_NORMAL           = 0x00
POWER_MODE_LOWPOWER         = 0x01
POWER_MODE_SUSPEND          = 0x02

# Operation mode settings
OPERATION_MODE_CONFIG       = 0x00
OPERATION_MODE_ACCONLY      = 0x01
OPERATION_MODE_MAGONLY      = 0x02
OPERATION_MODE_GYRONLY      = 0x03
OPERATION_MODE_ACCMAG       = 0x04
OPERATION_MODE_ACCGYRO      = 0x05
OPERATION_MODE_MAGGYRO      = 0x06
OPERATION_MODE_AMG          = 0x07
OPERATION_MODE_IMUPLUS      = 0x08
OPERATION_MODE_COMPASS      = 0x09
OPERATION_MODE_M4G          = 0x0A
OPERATION_MODE_NDOF_FMC_OFF = 0x0B
OPERATION_MODE_NDOF         = 0x0C


class BNO055(object):

    def __init__(self, bus = "RPI_1SW", address = ADDRESS_A, mode = OPERATION_MODE_NDOF, units = 0, init = True, verbose=False):
        """
        Initialize the object and optionally the hardware sensor

        Keyword arguments:
        bus (default "RPI_1SW") -- The I2C bus
        address (default ADDRESS_A) -- The BNO055 I2C address
        mode (default OPERATION_MODE_NDOF) -- The operation mode
        units (default 0) -- The value unit selection bits
        init (default True) -- False initializes software object only, does not alter hardware configuration.
        """

        if verbose:
            if (init == True):
                print("BNO055 Instantiating on BUS {} with ADDRESS {} to MODE {} using UNITS {} HW INIT {}".format(bus, address, mode, units, init))
            else:
                print("BNO055 Instantiating on BUS {} with ADDRESS {} using UNITS {} HW INIT {}".format(bus, address, units, init))

        # create an I2C bus object and set the address
        self.i2c_bus = di_i2c.DI_I2C(bus = bus, address = address)


        if init==True:

            # Save desired operation mode
            self._mode = mode
            # Send a thow-away command and ignore any response or I2C errors
            # just to make sure the BNO055 is in a good state and ready to accept
            # commands (this seems to be necessary after a hard power down).
            try:
                self.i2c_bus.write_reg_8(REG_PAGE_ID, 0)
            except IOError:
                # pass on an I2C IOError
                pass

            # switch to config mode
            self._config_mode(verbose=verbose)

            self.i2c_bus.write_reg_8(REG_PAGE_ID, 0)

            # check the chip ID
            if ID != self.i2c_bus.read_8(REG_CHIP_ID):
                raise RuntimeError("BNO055 failed to respond")

            if self.i2c_bus.read_8(REG_TEMP_SOURCE) != 0x01:
                if verbose: print("Doing init")

                # reset the device using the reset command
                self.i2c_bus.write_reg_8(REG_SYS_TRIGGER, 0x20)

                # wait 650ms after reset for chip to be ready (recommended in datasheet)
                time.sleep(0.65)

                # set to normal power mode
                self.i2c_bus.write_reg_8(REG_PWR_MODE, POWER_MODE_NORMAL)

                # default to internal oscillator
                self.i2c_bus.write_reg_8(REG_SYS_TRIGGER, 0x00)

                # set temperature source to gyroscope, as it seems to be more accurate.
                self.i2c_bus.write_reg_8(REG_TEMP_SOURCE, 0x01)
            else:
                pass
                if verbose: print("Skipping init")

            # set the unit selection bits
            self.i2c_bus.write_reg_8(REG_UNIT_SEL, units)

            # set temperature source to gyroscope, as it seems to be more accurate.
            self.i2c_bus.write_reg_8(REG_TEMP_SOURCE, 0x01)

            # switch to normal operation mode
            self._operation_mode(verbose=verbose)

        else:    # init = False
            self._mode = self.get_operation_mode()
            if verbose: print("Set _mode to:",self._mode)
        if verbose: print("BNO055 Instantiation Complete")


    def _config_mode(self, verbose=False):
        # switch to configuration mode
        #self.set_mode(OPERATION_MODE_CONFIG)
        mode = OPERATION_MODE_CONFIG
        if verbose: print("config_mode: {}".format(mode))

        self.i2c_bus.write_reg_8(REG_OPR_MODE, mode & 0xFF)
        # delay for 30 milliseconds according to datasheet
        time.sleep(0.03)

    def _operation_mode(self,verbose=False):
        # switch to operation mode (to read sensor data)
        self.set_mode(self._mode,verbose=verbose)

    def set_mode(self, mode, verbose=False):
        """Set operation mode for the sensor

        Keyword arguments:
        mode -- the operation mode. See BNO055 datasheet tables 3-3 and 3-5."""

        if verbose: print("set_mode: {}".format(mode))

        self.i2c_bus.write_reg_8(REG_OPR_MODE, mode & 0xFF)
        # delay for 30 milliseconds according to datasheet
        time.sleep(0.03)
        self._mode = mode

    def get_revision(self):
        """Get revision numbers

        Returns a tuple with revision numbers for Software revision, Bootloader
            version, Accelerometer ID, Magnetometer ID, and Gyro ID."""
        # Read revision values.
        accel = self.i2c_bus.read_8(REG_ACCEL_REV_ID)
        mag = self.i2c_bus.read_8(REG_MAG_REV_ID)
        gyro = self.i2c_bus.read_8(REG_GYRO_REV_ID)
        bl = self.i2c_bus.read_8(REG_BL_REV_ID)
        sw_lsb = self.i2c_bus.read_8(REG_SW_REV_ID_LSB)
        sw_msb = self.i2c_bus.read_8(REG_SW_REV_ID_MSB)
        sw = ((sw_msb << 8) | sw_lsb) & 0xFFFF
        # Return the results as a tuple of all 5 values.
        return (sw, bl, accel, mag, gyro)

    def set_external_crystal(self, external_crystal):
        """Set the BNO055 to use the internal/external oscillator

        Keyword arguments:
        external_crystal -- use external crystal?"""
        # Switch to configuration mode.
        self._config_mode()
        # Set the clock bit appropriately in the SYS_TRIGGER register.
        if external_crystal:
            self.i2c_bus.write_reg_8(REG_SYS_TRIGGER, 0x80)
        else:
            self.i2c_bus.write_reg_8(REG_SYS_TRIGGER, 0x00)
        # Go back to normal operation mode.
        self._operation_mode()

    def get_system_status(self, run_self_test = True):
        """Get the sensor system status

        Keyword arguments:
        run_self_test (default True) -- Run a self test? This will make the sensor go into config mode which will stop the fusion engine.

        Returns a tuple with status information. Three values will be returned:
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
        # run a self test?
        if run_self_test:
            # Switch to configuration mode if running self test.
            self._config_mode()
            # Perform a self test.
            sys_trigger = self.i2c_bus.read_8(REG_SYS_TRIGGER)
            self.i2c_bus.write_reg_8(REG_SYS_TRIGGER, sys_trigger | 0x1)
            # Wait for self test to finish.
            time.sleep(1.0)
            # Read test result.
            self_test = self.i2c_bus.read_8(REG_SELFTEST_RESULT)
            # Go back to operation mode.
            self._operation_mode()
        else:
            self_test = None

        # read status and error values
        status = self.i2c_bus.read_8(REG_SYS_STAT)
        error = self.i2c_bus.read_8(REG_SYS_ERR)

        # return the results as a tuple of all 3 values
        return (status, self_test, error)

    def get_calibration_status(self):
        """
        Get calibration status of the `InertialMeasurementUnit Sensor`_.

        The moment the sensor is powered, this method should be called almost continuously until the sensor is fully calibrated.
        For calibrating the sensor faster, it's enough to hold the sensor for a couple of seconds on each "face" of an imaginary cube.

        For each component of the system, there is a number that says how much the component has been calibrated:

          * **System**, ``3`` = fully calibrated, ``0`` = not calibrated.
          * **Gyroscope**, ``3`` = fully calibrated, ``0`` = not calibrated.
          * **Accelerometer**, ``3`` = fully calibrated, ``0`` = not calibrated.
          * **Magnetometer**, ``3`` = fully calibrated, ``0`` = not calibrated.

        :returns:  A tuple where each member shows how much a component of the IMU is calibrated. See the above description of the method.
        :rtype: (int,int,int,int)
        :raises ~exceptions.OSError: When the `InertialMeasurementUnit Sensor`_ is not reachable.

        .. important::

            The sensor needs a new calibration each time it's powered up.

        """
        # Return the calibration status register value.
        cal_status = self.i2c_bus.read_8(REG_CALIB_STAT)
        sys = (cal_status >> 6) & 0x03
        gyro = (cal_status >> 4) & 0x03
        accel = (cal_status >> 2) & 0x03
        mag = cal_status & 0x03
        # Return the results as a tuple of all 3 values.
        return (sys, gyro, accel, mag)

    def get_calibration(self):
        """Get calibration data

        Returns the sensor's calibration data as an array of 22 bytes.
        Can be saved and then reloaded with set_calibration to quickly
        calibrate from a previously calculated set of calibration data.
        """
        # Switch to configuration mode, as mentioned in section 3.10.4 of datasheet.
        self._config_mode()
        # Read the 22 bytes of calibration data
        cal_data = self.i2c_bus.read_list(REG_ACCEL_OFFSET_X_LSB, 22)
        # Go back to normal operation mode.
        self._operation_mode()
        return cal_data

    def set_calibration(self, data):
        """Set calibration data

        Keyword arguments:
        data -- a 22 byte list of calibration data to write to the sensor that was previously read with get_calibration.
        """
        # Check that 22 bytes were passed in with calibration data.
        if data is None or len(data) != 22:
            raise ValueError('set_calibration Expects a list of 22 bytes of calibration data')
        # Switch to configuration mode, as mentioned in section 3.10.4 of datasheet.
        self._config_mode()
        # Set the 22 bytes of calibration data.
        self.i2c_bus.write_reg_list(REG_ACCEL_OFFSET_X_LSB, data)
        # Go back to normal operation mode.
        self._operation_mode()

    def get_axis_remap(self):
        """Get axis remap information

        Returns a tuple with the axis remap register values. This will return
        6 values with the following meaning:
          - X axis remap (a value of AXIS_REMAP_X, AXIS_REMAP_Y, or AXIS_REMAP_Z.
                          which indicates that the physical X axis of the chip
                          is remapped to a different axis)
          - Y axis remap (see above)
          - Z axis remap (see above)
          - X axis sign (a value of AXIS_REMAP_POSITIVE or AXIS_REMAP_NEGATIVE
                         which indicates if the X axis values should be positive/
                         normal or negative/inverted.  The default is positive.)
          - Y axis sign (see above)
          - Z axis sign (see above)

        Note that by default the axis orientation of the BNO chip looks like
        the following (taken from section 3.4, page 24 of the datasheet).  Notice
        the dot in the corner that corresponds to the dot on the BNO chip:

                           | Z axis
                           |
                           |   / X axis
                       ____|__/____
          Y axis     / *   | /    /|
          _________ /______|/    //
                   /___________ //
                  |____________|/


        NOTE: DI IMU
          - Y is direction of arrow head
          - X is toward right side when head up looking at the chip side
          - Z is coming at you when looking at the chip side

        DI IMU For ROS On GoPiGo3 (No axis remap needed if mounted like this)
          - Mount with chip side up, arrow head pointing to left side of bot
          - X is forward
          - Y is toward left side
          - Z is up

        """
        # Get the axis remap register value.
        map_config = self.i2c_bus.read_8(REG_AXIS_MAP_CONFIG)
        z = (map_config >> 4) & 0x03
        y = (map_config >> 2) & 0x03
        x = map_config & 0x03
        # Get the axis remap sign register value.
        sign_config = self.i2c_bus.read_8(REG_AXIS_MAP_SIGN)
        x_sign = (sign_config >> 2) & 0x01
        y_sign = (sign_config >> 1) & 0x01
        z_sign = sign_config & 0x01
        # Return the results as a tuple of all 3 values.
        return (x, y, z, x_sign, y_sign, z_sign)

    def set_axis_remap(self, x, y, z, x_sign=AXIS_REMAP_POSITIVE,
           y_sign=AXIS_REMAP_POSITIVE, z_sign=AXIS_REMAP_POSITIVE, verbose=False):
        """Set axis remap

        Keyword arguments:
        x -- set to one of AXIS_REMAP_X, AXIS_REMAP_Y, or AXIS_REMAP_Z
        y --                     ''
        z --                     ''
        x_sign -- set to AXIS_REMAP_POSITIVE or AXIS_REMAP_NEGATIVE
        y_sign --                    ''
        z_sign --                    ''

        See the get_axis_remap documentation and datasheet section 3.4 for more information
        """
        # Switch to configuration mode.
        self._config_mode(verbose=verbose)
        # Set the axis remap register value.
        map_config = 0x00
        map_config |= (z & 0x03) << 4
        map_config |= (y & 0x03) << 2
        map_config |= x & 0x03
        self.i2c_bus.write_reg_8(REG_AXIS_MAP_CONFIG, map_config)
        # Set the axis remap sign register value.
        sign_config = 0x00
        sign_config |= (x_sign & 0x01) << 2
        sign_config |= (y_sign & 0x01) << 1
        sign_config |= z_sign & 0x01
        self.i2c_bus.write_reg_8(REG_AXIS_MAP_SIGN, sign_config)
        # Go back to normal operation mode.
        self._operation_mode(verbose=verbose)

    def _read_vector(self, reg, count = 3):
        # Read count number of 16-bit signed values starting from the provided
        # register. Returns a tuple of the values that were read.
        data = self.i2c_bus.read_list(reg, count*2)
        result = [0]*count
        for i in range(count):
            result[i] = (((data[(i * 2) + 1] & 0xFF) << 8) | (data[(i * 2)] & 0xFF)) & 0xFFFF
            if result[i] & 0x8000: #> 32767:
                result[i] -= 0x10000 #65536
        return result

    def read_euler(self):
        """Read the absolute orientation

        Returns the current absolute orientation as a tuple of heading, roll, and pitch euler angles in degrees."""
        heading, roll, pitch = self._read_vector(REG_EULER_H_LSB)
        return (heading/16.0, roll/16.0, pitch/16.0)

    def read_magnetometer(self):
        """Read the magnetometer

        Returns the current magnetometer reading as a tuple of X, Y, Z values in micro-Teslas."""
        x, y, z = self._read_vector(REG_MAG_DATA_X_LSB)
        return (x/16.0, y/16.0, z/16.0)

    def read_gyroscope(self):
        """Read the gyroscope

        Returns the current gyroscope (angular velocity) reading as a tuple of X, Y, Z values in degrees per second."""
        (x, y, z) = self._read_vector(REG_GYRO_DATA_X_LSB)
        return (x/16.0, y/16.0, z/16.0)

    def read_accelerometer(self):
        """Read the accelerometer

        Returns the current accelerometer reading as a tuple of X, Y, Z values in meters/second^2."""
        x, y, z = self._read_vector(REG_ACCEL_DATA_X_LSB)
        return (x/100.0, y/100.0, z/100.0)

    def read_linear_acceleration(self):
        """Read linear acceleration

        Returns the current linear acceleration (acceleration from movement not from gravity) reading as a tuple of X, Y, Z values in meters/second^2."""
        x, y, z = self._read_vector(REG_LINEAR_ACCEL_DATA_X_LSB)
        return (x/100.0, y/100.0, z/100.0)

    def read_gravity(self):
        """Read gravity

        Returns the current gravity reading as a tuple of X, Y, Z values in meters/second^2."""
        x, y, z = self._read_vector(REG_GRAVITY_DATA_X_LSB)
        return (x/100.0, y/100.0, z/100.0)

    def read_quaternion(self):
        """Read the quaternion values

        Returns the current orientation as a tuple of X, Y, Z, W quaternion values."""
        w, x, y, z = self._read_vector(REG_QUATERNION_DATA_W_LSB, 4)
        # Scale values, see 3.6.5.5 in the datasheet.
        scale = (1.0 / (1<<14))
        return (x*scale, y*scale, z*scale, w*scale)

    def read_temp(self):
        """Read the temperature

        Returns the current temperature in degrees celsius."""
        return self.i2c_bus.read_8(REG_TEMP, signed = True)

    def get_operation_mode(self):
        """Read the operation mode

        """
        op_mode =self.i2c_bus.read_8(REG_OPR_MODE)
        # print("op_mode: {:d}".format(op_mode))
        return op_mode
