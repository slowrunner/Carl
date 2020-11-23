# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python drivers for the Dexter Industries Light Color Sensor

from __future__ import print_function
from __future__ import division

from di_sensors import TCS34725
import time

PCA9570LED = False # set to True for Light Color Sensor boards v1.1.0 and earlier for the PCA9570 to control the LED
if PCA9570LED:
    from di_sensors import PCA9570


class LightColorSensor(object):
    """
    Class for interfacing with the `Light Color Sensor`_.
    """

    def __init__(self, sensor_integration_time = 0.0048, sensor_gain = TCS34725.GAIN_16X, led_state = False, bus = "RPI_1SW"):
        """
        Constructor for initializing a link to the `Light Color Sensor`_.

        :param float sensor_integration_time = 0.0048: Time in seconds for each sample (aka the time needed to take a sample). Range is between 0.0024 and 0.6144 seconds. Use increments of 2.4 ms.
        :param int sensor_gain = di_sensors.TCS34725.GAIN_16X: The gain constant of the sensor. Valid values are :py:const:`di_sensors.TCS34725.GAIN_1X`, :py:const:`di_sensors.TCS34725.GAIN_4X`, :py:const:`di_sensors.TCS34725.GAIN_16X` or :py:const:`di_sensors.TCS34725.GAIN_60X`.
        :param bool led_state = False: The LED state. If it's set to ``True``, then the LED will turn on, otherwise the LED will stay off. By default, the LED is turned on.
        :param str bus = "RPI_1SW": The bus to which the distance sensor is connected to. By default, it's set to bus ``"RPI_1SW"``. Check the :ref:`hardware specs <hardware-interface-section>` for more information about the ports.
        :raises ~exceptions.OSError: When the `Light Color Sensor`_ is not reachable.
        :raises ~exceptions.RuntimeError: When the chip ID is incorrect. This happens when we have a device pointing to the same address, but it's not a `Light Color Sensor`_.

        """
        self.TCS34725 = TCS34725.TCS34725(sensor_integration_time, sensor_gain, bus)
        if PCA9570LED:
            self.PCA9570 = PCA9570.PCA9570(bus)
        self.set_led(led_state)

    # set the state of the LED
    def set_led(self, value, delay = True):
        """
        Set the LED state.

        :param bool value: If set to ``True``, then the LED turns on, otherwise it stays off.
        :param bool delay = True: When it's set to ``True``, the LED turns on after *2 * time_to_take_sample* seconds have passed. This ensures that the next read following the LED change will be correct.
        :raises ~exceptions.OSError: When the `Light Color Sensor`_ is not reachable.

        """
        if PCA9570LED:
            if value:
                self.PCA9570.set_pins(0x00)
            else:
                self.PCA9570.set_pins(0x01)
        else:
            self.TCS34725.set_interrupt(value)

        if delay:
            # Delay for twice the integration time to ensure the LED state change has taken effect and a full sample has been made before the next reading.
            time.sleep((((256 - self.TCS34725.integration_time_val) * 0.0024) * 2))

    def get_raw_colors(self, delay = True):
        """
        Read the sensor values.

        :param bool delay = True: Delay for the time it takes to sample. If the delay is set to be added, then we are ensured to get fresh values on every call. Used in conjuction with the :py:meth:`~di_sensors.light_color_sensor.set_led` method.
        :returns: The RGBA values from the sensor. RGBA = Red, Green, Blue, Alpha (or Clear).
        :rtype: (float,float,float,float) where the range of each element is between 0 and 1.
        :raises ~exceptions.OSError: If the `Light Color Sensor`_ can't be reached.

        """

        return self.TCS34725.get_raw_data(delay)
