# https://www.dexterindustries.com
#
# Copyright (c) 2018 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#

from sim.di_sensors.easy_mutex import ifMutexAcquire, ifMutexRelease
import time
from sim.di_sensors import distance_sensor
import sim.simLog as simLog

class EasyDistanceSensor(distance_sensor.DistanceSensor):
    """
    Class for the `Distance Sensor`_ device.

    This class compared to :py:class:`~di_sensors.distance_sensor.DistanceSensor` uses mutexes that allows a given
    object to be accessed simultaneously from multiple threads/processes.
    Apart from this difference, there may also be functions that are more user-friendly than the latter.

    """
    def __init__(self, port="I2C", use_mutex=False):
        """
        Creates a :py:class:`~easygopigo3.EasyDistanceSensor` object which can be used for interfacing with a `distance sensor`_.

        :param string bus = ``"I2C"``: the bus for the sensor. For the GoPiGo3, options also include ``"GPG3_AD1"`` and ``"GPG3_AD2"``.
        :param bool use_mutex = False: When using multiple threads/processes that access the same resource/device, mutexes should be enabled. Check the :ref:`hardware specs <hardware-interface-section>` for more information about the ports.
        :raises ~exceptions.OSError: When the distance sensor is not connected to the designated bus/port, where in this case it must be ``"I2C"``. Most probably, this means the distance sensor is not connected at all.

        To see where the ports are located on the `GoPiGo3`_ robot, please take a look at the following diagram: :ref:`hardware-ports-section`.

        """
        simLog.logger.info("sim.di_sensors.EasyDistanceSensor object instantiated")
        self.descriptor = "Distance Sensor"
        self.use_mutex = use_mutex

        # let's be kind to the user who may get confused between ports and buses 
        # let's allow for all of them
        possible_ports = { "I2C" : "RPI_1SW",
                            "AD1" : "GPG3_AD1",
                            "AD2" : "GPG3_AD2",
                            "RPI_1SW": "RPI_1SW",
                            "RPI_1" : "RPI_1",
                            "RPI_1HW" : "RPI_1",   # doesn't really exist but can be a reflex for some users as we do have RPI_1SW
                            "GPG3_AD1": "GPG3_AD1",
                            "GPG3_AD2": "GPG3_AD2"}

        port = port.upper() # force to uppercase
        # switch quietly to default value if we receive gibberish
        if port in possible_ports.keys():
            bus = possible_ports[port]
        else:
            bus = "RPI_1SW"

        ifMutexAcquire(self.use_mutex)
        try:
            distance_sensor.DistanceSensor.__init__(self, bus=bus)
        except Exception as e:
            # remove print so that it doesn't show when starting Scratch
            # print("Distance Sensor init: {}".format(e))
            raise
        finally:
             ifMutexRelease(self.use_mutex)

    # Returns the values in cms
    def read_mm(self):
        """
        Reads the distance in millimeters.

        :returns: Distance from target in millimeters.
        :rtype: int

        .. note::

             1. Sensor's range is **5-2300** millimeters.
             2. When the values are out of the range, it returns **3000**.

        """

        # 8190 is what the sensor sends when it's out of range
        # we're just setting a default value
        mm = 8190
        readings = []
        attempt = 0

        # try 3 times to have a reading that is
        # smaller than 8m or bigger than 5 mm.
        # if sensor insists on that value, then pass it on
        while (mm > 8000 or mm < 5) and attempt < 3:
            ifMutexAcquire(self.use_mutex)
            try:
                mm = self.read_range_single()
            except Exception as e:
                print(e)
                mm = 0
            finally:
                ifMutexRelease(self.use_mutex)
            attempt = attempt + 1
            time.sleep(0.001)

        # add the reading to our last 3 readings
        # a 0 value is possible when sensor is not found
        if (mm < 8000 and mm > 5) or mm == 0:
            readings.append(mm)
        if len(readings) > 3:
            readings.pop(0)

        # calculate an average and limit it to 5 > X > 3000
        if len(readings) > 1: # avoid division by 0
            mm = round(sum(readings) / float(len(readings)))
        if mm > 3000:
            mm = 3000

        return mm

    def read(self):
        """
        Reads the distance in centimeters.

        :returns: Distance from target in centimeters.
        :rtype: int

        .. note::

             1. Sensor's range is **0-230** centimeters.
             2. When the values are out of the range, it returns **300**.

        """

        cm = self.read_mm()//10
        return (cm)

    def read_inches(self):
        """
        Reads the distance in inches.

        :returns: Distance from target in inches.
        :rtype: float with one decimal

        .. note::

             1. Sensor's range is **0-90** inches.
             2. Anything that's bigger than **90** inches is returned when the sensor can't detect any target/surface.

        """
        cm = self.read()
        return round(cm / 2.54, 1)
