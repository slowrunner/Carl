# https://www.dexterindustries.com
#
# Copyright (c) 2018 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#

# EASIER WRAPPERS FOR:
# IMU SENSOR,
# LIGHT AND COLOR SENSOR
# TEMPERATURE, HUMIDITY and PRESSURE SENSOR

# MUTEX SUPPORT WHEN NEEDED


from di_sensors import temp_hum_press
from time import sleep

from di_sensors.easy_mutex import ifMutexAcquire, ifMutexRelease

'''
PORT TRANSLATION
'''
ports = {
    "AD1": "GPG3_AD1",
    "AD2": "GPG3_AD2"
}

class EasyTHPSensor(temp_hum_press.TempHumPress):
    """
    Class for interfacing with the `Temperature Humidity Pressure Sensor`_.

    This class compared to :py:class:`~di_sensors.temp_hum_press.TempHumPress` uses mutexes that allows a given
    object to be accessed simultaneously from multiple threads/processes.
    Apart from this difference, there may
    also be functions that are more user-friendly than the latter.

    """

    def __init__(self, port="I2C", use_mutex=False):
        """
        Constructor for initializing link with the `Temperature Humidity Pressure Sensor`_.

        :param str port = "I2C": The port to which the THP sensor is connected to. Can also be connected to ports ``"AD1"`` or ``"AD2"`` of the `GoPiGo3`_. If you're passing an **invalid port**, then the sensor resorts to an ``"I2C"`` connection. Check the :ref:`hardware specs <hardware-interface-section>` for more information about the ports.
        :param bool use_mutex = False: When using multiple threads/processes that access the same resource/device, mutexes should be enabled.
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        """
        self.use_mutex = use_mutex

        try:
            bus = ports[port]
        except KeyError:
            bus = "RPI_1SW"

        ifMutexAcquire(self.use_mutex)
        try:
            super(self.__class__, self).__init__(bus = bus)
        except Exception as e:
            raise
        finally:
            ifMutexRelease(self.use_mutex)

    def safe_celsius(self):
        """
        Read temperature in Celsius degrees.

        :returns: Temperature in Celsius degrees.
        :rtype: float
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        """
        ifMutexAcquire(self.use_mutex)
        try:
            temp = self.get_temperature_celsius()
        except Exception as e:
            raise
        finally:
            ifMutexRelease(self.use_mutex)

        return round(temp,0)

    def safe_fahrenheit(self):
        """
        Read temperature in Fahrenheit degrees.

        :returns: Temperature in Fahrenheit degrees.
        :rtype: float
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        """
        ifMutexAcquire(self.use_mutex)
        try:
            temp = self.get_temperature_fahrenheit()
        except Exception as e:
            raise
        finally:
            ifMutexRelease(self.use_mutex)

        return round(temp,0)

    def safe_pressure(self):
        """
        Read the air pressure in pascals.

        :returns: The air pressure in pascals.
        :rtype: float
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        """
        ifMutexAcquire(self.use_mutex)
        try:
            pressure = self.get_pressure()
        except Exception as e:
            raise
        finally:
            ifMutexRelease(self.use_mutex)

        return round(pressure,0)

    def safe_humidity(self):
        """
        Read the relative humidity as a percentage.

        :returns: Percentage of the relative humidity.
        :rtype: float
        :raises ~exceptions.OSError: When the sensor cannot be reached.

        """
        ifMutexAcquire(self.use_mutex)
        try:
            humidity = self.get_humidity()
        except Exception as e:
            raise
        finally:
            ifMutexRelease(self.use_mutex)

        return round(humidity,0)
