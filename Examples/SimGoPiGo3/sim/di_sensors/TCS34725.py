# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python drivers for the TCS34725 light color sensor

from __future__ import print_function
from __future__ import division

import di_i2c
import time

# Constants
ADDRESS          = 0x29
ID               = 0x12 # Register should be equal to 0x44 for the TCS34721 or TCS34725, or 0x4D for the TCS34723 or TCS34727.

COMMAND_BIT      = 0x80

ENABLE           = 0x00
ENABLE_AIEN      = 0x10 # RGBC Interrupt Enable
ENABLE_WEN       = 0x08 # Wait enable - Writing 1 activates the wait timer
ENABLE_AEN       = 0x02 # RGBC Enable - Writing 1 actives the ADC, 0 disables it
ENABLE_PON       = 0x01 # Power on - Writing 1 activates the internal oscillator, 0 disables it
ATIME            = 0x01 # Integration time
WTIME            = 0x03 # Wait time (if ENABLE_WEN is asserted)
AILTL            = 0x04 # Clear channel lower interrupt threshold
AILTH            = 0x05
AIHTL            = 0x06 # Clear channel upper interrupt threshold
AIHTH            = 0x07
PERS             = 0x0C # Persistence register - basic SW filtering mechanism for interrupts
PERS_NONE        = 0b0000 # Every RGBC cycle generates an interrupt
PERS_1_CYCLE     = 0b0001 # 1 clean channel value outside threshold range generates an interrupt
PERS_2_CYCLE     = 0b0010 # 2 clean channel values outside threshold range generates an interrupt
PERS_3_CYCLE     = 0b0011 # 3 clean channel values outside threshold range generates an interrupt
PERS_5_CYCLE     = 0b0100 # 5 clean channel values outside threshold range generates an interrupt
PERS_10_CYCLE    = 0b0101 # 10 clean channel values outside threshold range generates an interrupt
PERS_15_CYCLE    = 0b0110 # 15 clean channel values outside threshold range generates an interrupt
PERS_20_CYCLE    = 0b0111 # 20 clean channel values outside threshold range generates an interrupt
PERS_25_CYCLE    = 0b1000 # 25 clean channel values outside threshold range generates an interrupt
PERS_30_CYCLE    = 0b1001 # 30 clean channel values outside threshold range generates an interrupt
PERS_35_CYCLE    = 0b1010 # 35 clean channel values outside threshold range generates an interrupt
PERS_40_CYCLE    = 0b1011 # 40 clean channel values outside threshold range generates an interrupt
PERS_45_CYCLE    = 0b1100 # 45 clean channel values outside threshold range generates an interrupt
PERS_50_CYCLE    = 0b1101 # 50 clean channel values outside threshold range generates an interrupt
PERS_55_CYCLE    = 0b1110 # 55 clean channel values outside threshold range generates an interrupt
PERS_60_CYCLE    = 0b1111 # 60 clean channel values outside threshold range generates an interrupt
CONFIG           = 0x0D
CONFIG_WLONG     = 0x02 # Choose between short and long (12x) wait times via WTIME
CONTROL          = 0x0F # Set the gain level for the sensor
ID               = 0x12 # 0x44 = TCS34721/TCS34725, 0x4D = TCS34723/TCS34727
STATUS           = 0x13
STATUS_AINT      = 0x10 # RGBC Clean channel interrupt
STATUS_AVALID    = 0x01 # Indicates that the RGBC channels have completed an integration cycle

CDATAL           = 0x14 # Clear channel data
CDATAH           = 0x15
RDATAL           = 0x16 # Red channel data
RDATAH           = 0x17
GDATAL           = 0x18 # Green channel data
GDATAH           = 0x19
BDATAL           = 0x1A # Blue channel data
BDATAH           = 0x1B

GAIN_1X          = 0x00 #  1x gain
GAIN_4X          = 0x01 #  4x gain
GAIN_16X         = 0x02 # 16x gain
GAIN_60X         = 0x03 # 60x gain


class TCS34725(object):
    """Drivers for TCS34725 light color sensor"""

    def __init__(self, integration_time = 0.0024, gain = GAIN_16X, bus = "RPI_1SW"):
        """Initialize the sensor

        Keyword arguments:
        integration_time (default 0.0024 seconds) -- Time in seconds for each sample. 0.0024 second (2.4ms) increments. Clipped to the range of 0.0024 to 0.6144 seconds.
        gain (default GAIN_16X) -- The gain constant. Valid values are GAIN_1X, GAIN_4X, GAIN_16X, and GAIN_60X
        bus (default "RPI_1SW") -- The I2C bus"""
        self.i2c_bus = di_i2c.DI_I2C(bus = bus, address = ADDRESS, big_endian = False)

        # Make sure we're connected to the right sensor.
        chip_id = self.i2c_bus.read_8((COMMAND_BIT | ID))
        if chip_id != 0x44:
            raise RuntimeError('Incorrect chip ID.')

        # Set default integration time and gain.
        self.set_integration_time(integration_time)
        self.set_gain(gain)

        # Enable the device (by default, the device is in power down mode on bootup).
        self.enable()

    def enable(self):
        """Enable the sensor"""
        # Set the power and enable bits.
        self.i2c_bus.write_reg_8((COMMAND_BIT | ENABLE), ENABLE_PON)
        time.sleep(0.01)
        self.i2c_bus.write_reg_8((COMMAND_BIT | ENABLE), (ENABLE_PON | ENABLE_AEN))

    def disable(self):
        """Disable the sensor"""
        # Clear the power and enable bits.
        reg = self.i2c_bus.read_8((COMMAND_BIT | ENABLE))
        reg &= ~(ENABLE_PON | ENABLE_AEN)
        self.i2c_bus.write_reg_8((COMMAND_BIT | ENABLE), reg)

    def set_integration_time(self, time):
        """Set the integration (sampling) time for the sensor

        Keyword arguments:
        time -- Time in seconds for each sample. 0.0024 second (2.4ms) increments. Clipped to the range of 0.0024 to 0.6144 seconds."""
        val = int(0x100 - (time / 0.0024))
        if val > 255:
            val = 255
        elif val < 0:
            val = 0
        self.i2c_bus.write_reg_8((COMMAND_BIT | ATIME), val)
        self.integration_time_val = val

    def set_gain(self, gain):
        """Set the sensor gain (light sensitivity)

        Keyword arguments:
        gain -- The gain constant. Valid values are GAIN_1X, GAIN_4X, GAIN_16X, and GAIN_60X"""
        self.i2c_bus.write_reg_8((COMMAND_BIT | CONTROL), gain)

    def set_interrupt(self, state):
        self.i2c_bus.write_reg_8((COMMAND_BIT | PERS), PERS_NONE)
        enable = self.i2c_bus.read_8((COMMAND_BIT | ENABLE))
        if state:
            enable |= ENABLE_AIEN
        else:
            enable &= ~ENABLE_AIEN
        self.i2c_bus.write_reg_8((COMMAND_BIT | ENABLE), enable)

    def get_raw_data(self, delay = True):
        """Read the Red Green Blue and Clear values from the sensor

        Keyword arguments:
        delay (default True) -- Delay for the time it takes to sample. This allows immediately consecutive readings that aren't redundant.

        Returns the values as a 4-tuple on a scale of 0-1. Red Green Blue Clear."""
        if delay:
            # Delay for the integration time to allow reading immediately after the previous read.
            time.sleep(((256 - self.integration_time_val) * 0.0024))

        div = ((256 - self.integration_time_val) * 1024)

        # Read each color register.
        r = self.i2c_bus.read_16((COMMAND_BIT | RDATAL)) / div
        g = self.i2c_bus.read_16((COMMAND_BIT | GDATAL)) / div
        b = self.i2c_bus.read_16((COMMAND_BIT | BDATAL)) / div
        c = self.i2c_bus.read_16((COMMAND_BIT | CDATAL)) / div
        if r > 1:
            r = 1
        if g > 1:
            g = 1
        if b > 1:
            b = 1
        if c > 1:
            c = 1
        return (r, g, b, c)
