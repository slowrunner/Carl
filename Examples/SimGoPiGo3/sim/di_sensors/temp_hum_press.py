# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python drivers for the Dexter Industries Temperature Humidity Pressure Sensor

from __future__ import print_function
from __future__ import division

from di_sensors import BME280


class TempHumPress(object):
    """
    Class for interfacing with the `Temperature Humidity Pressure Sensor`_.
    """

    def __init__(self, bus = "RPI_1SW"):
        """
        Constructor for initializing link with the `Temperature Humidity Pressure Sensor`_.

        :param str bus = "RPI_1SW": The bus to which the THP sensor is connected to. By default, it's set to bus ``"RPI_1SW"``. Check the :ref:`hardware specs <hardware-interface-section>` for more information about the ports.
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        """
        self.BME280 = BME280.BME280(bus = bus, t_mode = BME280.OSAMPLE_2, p_mode = BME280.OSAMPLE_4, h_mode = BME280.OSAMPLE_4, standby = BME280.STANDBY_10, filter = BME280.FILTER_8)

    def get_temperature_celsius(self):
        """
        Read temperature in Celsius degrees.

        :returns: Temperature in Celsius degrees.
        :rtype: float
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        """
        return self.BME280.read_temperature()

    def get_temperature_fahrenheit(self):
        """
        Read temperature in Fahrenheit degrees.

        :returns: Temperature in Fahrenheit degrees.
        :rtype: float
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        """
        return self.BME280.read_temperature_f()


    def get_pressure(self):
        """
        Read the air pressure in pascals.

        :returns: The air pressure in pascals.
        :rtype: float
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        """
        return self.BME280.read_pressure()

    def get_humidity(self):
        """
        Read the relative humidity as a percentage.

        :returns: Percentage of the relative humidity.
        :rtype: float
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        """
        return self.BME280.read_humidity()
