# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python drivers for the BME280 Temperature Humidity Pressure sensor

from __future__ import print_function
from __future__ import division

import di_i2c
import time

# Constants

# BME280 default address.
ADDRESS = 0x76

# Operating Modes
OSAMPLE_1 = 1
OSAMPLE_2 = 2
OSAMPLE_4 = 3
OSAMPLE_8 = 4
OSAMPLE_16 = 5

# Standby Settings
STANDBY_0p5 = 0
STANDBY_62p5 = 1
STANDBY_125 = 2
STANDBY_250 = 3
STANDBY_500 = 4
STANDBY_1000 = 5
STANDBY_10 = 6
STANDBY_20 = 7

# Filter Settings
FILTER_off = 0
FILTER_2 = 1
FILTER_4 = 2
FILTER_8 = 3
FILTER_16 = 4

# BME280 Registers
REG_DIG_T1 = 0x88  # Trimming parameter registers
REG_DIG_T2 = 0x8A
REG_DIG_T3 = 0x8C

REG_DIG_P1 = 0x8E
REG_DIG_P2 = 0x90
REG_DIG_P3 = 0x92
REG_DIG_P4 = 0x94
REG_DIG_P5 = 0x96
REG_DIG_P6 = 0x98
REG_DIG_P7 = 0x9A
REG_DIG_P8 = 0x9C
REG_DIG_P9 = 0x9E

REG_DIG_H1 = 0xA1
REG_DIG_H2 = 0xE1
REG_DIG_H3 = 0xE3
REG_DIG_H4 = 0xE4
REG_DIG_H5 = 0xE5
REG_DIG_H6 = 0xE6
REG_DIG_H7 = 0xE7

REG_CHIPID = 0xD0
REG_VERSION = 0xD1
REG_SOFTRESET = 0xE0

REG_STATUS = 0xF3
REG_CONTROL_HUM = 0xF2
REG_CONTROL = 0xF4
REG_CONFIG = 0xF5
#REG_DATA = 0xF7
REG_PRESSURE_DATA = 0xF7
REG_TEMP_DATA     = 0xFA
REG_HUMIDITY_DATA = 0xFD


class BME280(object):

    def __init__(self, bus = "RPI_1SW", t_mode = OSAMPLE_1, h_mode = OSAMPLE_1, p_mode = OSAMPLE_1,
                 standby = STANDBY_250, filter = FILTER_off):
        """Initialize the sensor

        Keyword arguments:
        bus (default "RPI_1SW") -- The I2C bus
        t_mode (default OSAMPLE_1) -- The temperature measurement mode
        h_mode (default OSAMPLE_1) -- The humidity measurement mode
        p_mode (default OSAMPLE_1) -- The pressure measurement mode
        standby (default STANDBY_250) -- The delay constant for waiting between taking readings
        filter (default FILTER_off) -- The filter mode"""

        # confirm that all the values are valid
        if t_mode not in [OSAMPLE_1, OSAMPLE_2, OSAMPLE_4, OSAMPLE_8, OSAMPLE_16]:
            raise ValueError('Unexpected t_mode %d. Valid modes are OSAMPLE_1, OSAMPLE_2, OSAMPLE_4, OSAMPLE_8, and OSAMPLE_16.' % t_mode)
        self._t_mode = t_mode

        if h_mode not in [OSAMPLE_1, OSAMPLE_2, OSAMPLE_4, OSAMPLE_8, OSAMPLE_16]:
            raise ValueError('Unexpected h_mode %d. Valid modes are OSAMPLE_1, OSAMPLE_2, OSAMPLE_4, OSAMPLE_8, and OSAMPLE_16.' % h_mode)
        self._h_mode = h_mode

        if p_mode not in [OSAMPLE_1, OSAMPLE_2, OSAMPLE_4, OSAMPLE_8, OSAMPLE_16]:
            raise ValueError('Unexpected p_mode %d. Valid modes are OSAMPLE_1, OSAMPLE_2, OSAMPLE_4, OSAMPLE_8, and OSAMPLE_16.' % p_mode)
        self._p_mode = p_mode

        if standby not in [STANDBY_0p5, STANDBY_62p5, STANDBY_125, STANDBY_250,
                        STANDBY_500, STANDBY_1000, STANDBY_10, STANDBY_20]:
            raise ValueError('Unexpected standby value %d. Valid values are STANDBY_0p5, STANDBY_10, STANDBY_20, STANDBY_62p5, STANDBY_125, STANDBY_250, STANDBY_500, and STANDBY_1000.' % standby)
        self._standby = standby

        if filter not in [FILTER_off, FILTER_2, FILTER_4, FILTER_8, FILTER_16]:
            raise ValueError('Unexpected filter value %d. Valid values are FILTER_off, FILTER_2, FILTER_4, FILTER_8, and FILTER_16' % filter)
        self._filter = filter

        # create an I2C bus object and set the address
        self.i2c_bus = di_i2c.DI_I2C(bus = bus, address = ADDRESS, big_endian = False) # little endian

        # load calibration values.
        self._load_calibration()
        self.i2c_bus.write_reg_8(REG_CONTROL, 0x24)  # Sleep mode
        time.sleep(0.002)

        # set the standby time
        self.i2c_bus.write_reg_8(REG_CONFIG, ((standby << 5) | (filter << 2)))
        time.sleep(0.002)

        # set the sample modes
        self.i2c_bus.write_reg_8(REG_CONTROL_HUM, h_mode)  # Set Humidity Oversample
        self.i2c_bus.write_reg_8(REG_CONTROL, ((t_mode << 5) | (p_mode << 2) | 3))  # Set Temp/Pressure Oversample and enter Normal mode
        self.t_fine = 0.0

    def _load_calibration(self):
        # Read calibration data

        self.dig_T1 = self.i2c_bus.read_16(REG_DIG_T1)
        self.dig_T2 = self.i2c_bus.read_16(REG_DIG_T2, signed = True)
        self.dig_T3 = self.i2c_bus.read_16(REG_DIG_T3, signed = True)

        self.dig_P1 = self.i2c_bus.read_16(REG_DIG_P1)
        self.dig_P2 = self.i2c_bus.read_16(REG_DIG_P2, signed = True)
        self.dig_P3 = self.i2c_bus.read_16(REG_DIG_P3, signed = True)
        self.dig_P4 = self.i2c_bus.read_16(REG_DIG_P4, signed = True)
        self.dig_P5 = self.i2c_bus.read_16(REG_DIG_P5, signed = True)
        self.dig_P6 = self.i2c_bus.read_16(REG_DIG_P6, signed = True)
        self.dig_P7 = self.i2c_bus.read_16(REG_DIG_P7, signed = True)
        self.dig_P8 = self.i2c_bus.read_16(REG_DIG_P8, signed = True)
        self.dig_P9 = self.i2c_bus.read_16(REG_DIG_P9, signed = True)

        self.dig_H1 = self.i2c_bus.read_8(REG_DIG_H1)
        self.dig_H2 = self.i2c_bus.read_16(REG_DIG_H2, signed = True)
        self.dig_H3 = self.i2c_bus.read_8(REG_DIG_H3)
        self.dig_H6 = self.i2c_bus.read_8(REG_DIG_H7, signed = True)

        h4 = self.i2c_bus.read_8(REG_DIG_H4, signed = True)
        h4 = (h4 << 4)
        self.dig_H4 = h4 | (self.i2c_bus.read_8(REG_DIG_H5) & 0x0F)

        h5 = self.i2c_bus.read_8(REG_DIG_H6, signed = True)
        h5 = (h5 << 4)
        self.dig_H5 = h5 | (
        self.i2c_bus.read_8(REG_DIG_H5) >> 4 & 0x0F)

    def _read_raw_temp(self):
        # read raw temperature data once it's available
        while (self.i2c_bus.read_8(REG_STATUS) & 0x08):
            time.sleep(0.002)
        data = self.i2c_bus.read_list(REG_TEMP_DATA, 3)
        return ((data[0] << 16) | (data[1] << 8) | data[2]) >> 4

    def _read_raw_pressure(self):
        # read raw pressure data once it's available
        while (self.i2c_bus.read_8(REG_STATUS) & 0x08):
            time.sleep(0.002)
        data = self.i2c_bus.read_list(REG_PRESSURE_DATA, 3)
        return ((data[0] << 16) | (data[1] << 8) | data[2]) >> 4

    def _read_raw_humidity(self):
        # read raw humidity data once it's available
        while (self.i2c_bus.read_8(REG_STATUS) & 0x08):
            time.sleep(0.002)
        data = self.i2c_bus.read_list(REG_HUMIDITY_DATA, 2)
        return (data[0] << 8) | data[1]

    def read_temperature(self):
        """Get the temperature

        Returns temperature in degrees celsius."""
        # float in Python is double precision
        UT = float(self._read_raw_temp())
        var1 = (UT / 16384.0 - float(self.dig_T1) / 1024.0) * float(self.dig_T2)
        var2 = ((UT / 131072.0 - float(self.dig_T1) / 8192.0) * (
        UT / 131072.0 - float(self.dig_T1) / 8192.0)) * float(self.dig_T3)
        self.t_fine = int(var1 + var2)
        return (var1 + var2) / 5120.0

    def read_humidity(self):
        """Get the humidity

        Returns the temperature-compensated humidity. read_temperature must be called to update the temperature compensation."""
        adc = float(self._read_raw_humidity())
        # print 'Raw humidity = {0:d}'.format (adc)
        h = float(self.t_fine) - 76800.0
        h = (adc - (float(self.dig_H4) * 64.0 + float(self.dig_H5) / 16384.0 * h)) * (
        float(self.dig_H2) / 65536.0 * (1.0 + float(self.dig_H6) / 67108864.0 * h * (
        1.0 + float(self.dig_H3) / 67108864.0 * h)))
        h = h * (1.0 - float(self.dig_H1) * h / 524288.0)
        if h > 100:
            h = 100
        elif h < 0:
            h = 0
        return h

    def read_pressure(self):
        """Get the pressure

        Returns the temperature-compensated pressure in Pascals. read_temperature must be called to update the temperature compensation."""
        adc = float(self._read_raw_pressure())
        var1 = float(self.t_fine) / 2.0 - 64000.0
        var2 = var1 * var1 * float(self.dig_P6) / 32768.0
        var2 = var2 + var1 * float(self.dig_P5) * 2.0
        var2 = var2 / 4.0 + float(self.dig_P4) * 65536.0
        var1 = (
               float(self.dig_P3) * var1 * var1 / 524288.0 + float(self.dig_P2) * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * float(self.dig_P1)
        if var1 == 0:
            return 0
        p = 1048576.0 - adc
        p = ((p - var2 / 4096.0) * 6250.0) / var1
        var1 = float(self.dig_P9) * p * p / 2147483648.0
        var2 = p * float(self.dig_P8) / 32768.0
        return p + (var1 + var2 + float(self.dig_P7)) / 16.0

    def read_temperature_f(self):
        # Wrapper to get temp in F
        return self.read_temperature() * 1.8 + 32

    def read_dewpoint(self):
        # Return calculated dewpoint in C, only accurate at > 50% RH
        return self.read_temperature() - ((100 - self.read_humidity()) / 5)

    def read_dewpoint_f(self):
        # Return calculated dewpoint in F, only accurate at > 50% RH
        return self.read_dewpoint() * 1.8 + 32

    def read_pressure_inches(self):
        # Wrapper to get pressure in inches of Hg
        return self.read_pressure() * 0.0002953
