# https://www.dexterindustries.com
#
# Copyright (c) 2019 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python drivers for the Dexter Industries Line Follower sensor

from __future__ import print_function
from __future__ import division

import di_i2c
import time


class LineFollower(object):
    """
    Class for interfacing with the `Line Follower Sensor (black board)`_.

    .. important::

        This sensor is the replacement for the red one :py:class:`~di_sensors.line_follower.LineFollowerRed`, which is getting retired, 
        but we'll still support it. The improvements of this one over the red one are:

        1. Much faster poll rate - **~130** times a second vs the red one at **~60Hz**.
        2. More energy efficient - this one uses a **minimum** amount of power compared to the previous generation which tended to get hot to touch.
        3. Sensors are much more **accurate and consistent** over the red ones.
        4. **Reduced overhead** on the I2C line.

    """

    def __init__(self, bus = "RPI_1SW"):
        """
        Constructor for initializing an object to interface with the `Line Follower Sensor (black board)`_.

        :param str bus = "RPI_1SW": The bus to which the `Line Follower Sensor (black board)`_ is connected to. By default, it's set to ``"RPI_1SW"``. Check the :ref:`hardware specs <hardware-interface-section>` for more information about the ports.
        """

        # create an I2C bus object and set the address
        self.i2c_bus = di_i2c.DI_I2C(bus = bus, address = 0x06)

    def read_sensors(self):
        """
        Read the line follower's values.

        :returns: A 6-element tuple with line sensors 1 through 6 **(from left to right with the arrow pointing forward)** with values between **0** (black) and **1** (white).
        :rtype: tuple
        :raises ~exceptions.OSError: When the `Line Follower Sensor (black board)`_ is not reachable.
        """

        array = self.i2c_bus.read_list(0x01, 8)
        for s in range(6):
            array[s] = (array[s] << 2) | ((array[6 + int(s / 4)] >> (2 * (s % 4))) & 0x03)
            array[s] = (1023 - array[s]) / 1023.0
        
        array = array[:6]
        array = array[::-1]

        return array

    def get_manufacturer(self):
        """
        Read the manufacturer of the `Line Follower Sensor (black board)`_'s.

        :returns: The name of the manufacturer.
        :rtype: str
        :raises ~exceptions.OSError: When the `Line Follower Sensor (black board)`_ is not reachable.
        """

        array = self.i2c_bus.read_list(0x11, 20)

        name = ""
        for c in range(20):
            if array[c] != 0:
                name += chr(array[c])
            else:
                break
        return name

    def get_board(self):
        """
        Read the board name of the `Line Follower Sensor (black board)`_.

        :returns: The name of the board.
        :rtype: str
        :raises ~exceptions.OSError: When the `Line Follower Sensor (black board)`_ is not reachable.
        """

        array = self.i2c_bus.read_list(0x12, 20)

        name = ""
        for c in range(20):
            if array[c] != 0:
                name += chr(array[c])
            else:
                break
        return name

    def get_version_firmware(self):
        """
        Get the firmware version currently residing on the `Line Follower Sensor (black board)`_.

        :returns: The version of the firmware.
        :rtype: str
        :raises ~exceptions.OSError: When the `Line Follower Sensor (black board)`_ is not reachable.
        """
        self.i2c_bus.write_8(0x13)
        return self.i2c_bus.read_32()


class LineFollowerRed(object):
    """
    Class for interfacing with the depreciated `Line Follower Sensor (red board)`_.
    """
    def __init__(self, bus = "RPI_1SW"):
        """
        Constructor for initializing an object to interface with the depreciated `Line Follower Sensor (red board)`_.

        :param str bus = "RPI_1SW": The bus to which the depreciated `Line Follower Sensor (red board)`_ is connected to. By default, it's set to ``"RPI_1SW"``. Check the :ref:`hardware specs <hardware-interface-section>` for more information about the ports.
        """

        # create an I2C bus object and set the address
        self.i2c_bus = di_i2c.DI_I2C(bus = bus, address = 0x06)

    def read_sensors(self):
        """
        Read the line follower's values.

        :returns: A 5-element tuple with the 1st element starting from the left of the sensor going to the right of it **(check the markings on the sensor)** with values between **0** (for black) and **1** (for white).
        :rtype: tuple
        :raises ~exceptions.OSError: When the depreciated `Line Follower Sensor (red board)`_ is not reachable.
        """

        self.i2c_bus.write_reg_list(0x01, [0x03] + 3 * [0x00])
        time.sleep(0.01)
        self.i2c_bus.write_reg_list(0x01, [0x03] + 3 * [0x00])
        array = self.i2c_bus.read_list(None, 10)

        output = []
        for step in range(5):
            temp = array[2 * step] * 256 + array[2 * step + 1]
            output.append((1023 - temp) / 1023.0)

        return output[::-1]
