# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python drivers for the PCA9570 I2C output expander

from __future__ import print_function
from __future__ import division

import di_i2c

# Constants
ADDRESS = 0x24


class PCA9570(object):
    """Drivers for PCA9570 I2C output expander"""

    def __init__(self, bus = "RPI_1SW"):
        """Initialize the I2C output expander

        Keyword arguments:
        bus (default RPI_1SW) -- The I2C bus"""
        self.i2c_bus = di_i2c.DI_I2C(bus = bus, address = ADDRESS)

    def set_pins(self, value):
        """Set the output pin states

        Keyword arguments:
        value -- The bit values for the 4 outputs"""
        self.i2c_bus.write_8((value & 0x0F))

    def get_pins(self):
        """Get the output pin states

        Returns the bit values for the 4 outputs"""
        return (self.i2c_bus.read_8() & 0x0F)
