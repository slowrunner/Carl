# ======= SIMULATED DISTANCE SENSOR =========

# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python drivers for the Dexter Industries Distance Sensor

from __future__ import print_function
from __future__ import division

from sim.di_sensors import VL53L0X
import time

import sim.simLog as simLog
import sim.simDataJson as simDataJson


class DistanceSensor(object):
    """
    Class for interfacing with the `Distance Sensor`_.
    """

    def __init__(self, bus = "RPI_1SW"):
        """
        Constructor for initializing a :py:class:`~di_sensors.distance_sensor.DistanceSensor` class.

        :param str bus = "RPI_1SW": The bus to which the distance sensor is connected to. By default, it's set to bus ``"RPI_1SW"``. Check the :ref:`hardware specs <hardware-interface-section>` for more information about the ports.
        :raises ~exceptions.OSError: When the distance sensor is not connected to the designated bus/port. Most probably, this means the distance sensor is not connected at all.

        """
        simLog.logger.info("Initializing sim.di_sensor.distance_sensor.DistanceSensor() object")

        # self.VL53L0X = VL53L0X.VL53L0X(bus = bus)

        # SIM - initialize range to 36 inches 914.4 mm
        simDataJson.saveData('rangeSensor_mm',914.4)
        # set to long range (about 2.3 meters)
        # self.VL53L0X.set_signal_rate_limit(0.1)
        # self.VL53L0X.set_vcsel_pulse_period(self.VL53L0X.VcselPeriodPreRange, 18)
        # self.VL53L0X.set_vcsel_pulse_period(self.VL53L0X.VcselPeriodFinalRange, 14)

    def start_continuous(self, period_ms = 0):
        """
        Start taking continuous measurements.
        Once this method is called, then the :py:meth:`~di_sensors.distance_sensor.DistanceSensor.read_range_continuous` method should be called periodically, depending on the value that was set to ``period_ms`` parameter.

        :param int period_ms = 0: The time between measurements. Can be set to anywhere between **20 ms** and **5 secs**.
        :raises ~exceptions.OSError: When it cannot communicate with the device.

        The advantage of this method over the simple :py:meth:`~di_sensors.distance_sensor.DistanceSensor.read_range_single` method is that this method allows for faster reads. Therefore, this method should be used by those that
        want maximum performance from the sensor.

        Also, the greater the value set to ``period_ms``, the higher is the accuracy of the distance sensor.

        """
        self.VL53L0X.start_continuous(period_ms)

    def read_range_continuous(self):
        """
        Read the detected range while the sensor is taking continuous measurements at the set rate.

        :returns: The detected range of the sensor as measured in millimeters. The range can go up to 2.3 meters.
        :rtype: int
        :raises ~exceptions.OSError: When the distance sensor is not reachable or when the :py:meth:`~di_sensors.distance_sensor.DistanceSensor.start_continuous` hasn't been called before. This exception gets raised also when the user is trying to poll data faster than how it was initially set with the :py:meth:`~di_sensors.distance_sensor.DistanceSensor.start_continuous` method.

        .. important::

            If this method is called in a shorter timeframe than the period that was set through :py:meth:`~di_sensors.distance_sensor.DistanceSensor.start_continuous`, an :py:exc:`~exceptions.OSError` exception is thrown.

            There's also a timeout on this method that's set to **0.5 secs**. Having this timeout set to **0.5 secs** means that the :py:exc:`~exceptions.OSError` gets thrown when the ``period_ms`` parameter of the :py:meth:`~di_sensors.distance_sensor.DistanceSensor.start_continuous`
            method is bigger than **500 ms**.

        """
        return self.VL53L0X.read_range_continuous_millimeters()

    def read_range_single(self, safe_infinity=True):
        """
        Read the detected range with a single measurement. This is less precise/fast than its counterpart :py:meth:`~di_sensors.distance_sensor.DistanceSensor.read_range_continuous`, but it's easier to use.

        :param boolean safe_infinity = True: As sometimes the distance sensor returns a small value when there's nothing in front of it, we need to poll again and again to confirm the presence of an obstacle. Setting ``safe_infinity`` to ``False`` will avoid that extra polling.

        :returns: The detected range of the sensor as measured in millimeters. The range can go up to 2.3 meters.
        :rtype: int
        :raises ~exceptions.OSError: When the distance sensor is not reachable.

        """
        # value = self.VL53L0X.read_range_single_millimeters()
        value = simDataJson.getData('rangeSensor_mm')
        # Because it happens that the distance sensor will return a small value
        # when it should read infinity, if we do read a small value,
        # then poll again and again to ensure it's an actual small value
        # if safe_infinity and value < 8190:
        #     for i in range(3):
        #         value = self.VL53L0X.read_range_single_millimeters()
        #         if value >= 8190:
        #                 return value

        return value


    def timeout_occurred(self):
        """
        Checks if a timeout has occurred on the :py:meth:`~di_sensors.distance_sensor.DistanceSensor.read_range_continuous` method.

        :returns: Whether a timeout has occurred or not.
        :rtype: bool

        """
        return self.VL53L0X.timeout_occurred()
