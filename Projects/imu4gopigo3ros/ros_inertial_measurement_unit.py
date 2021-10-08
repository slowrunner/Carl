# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python drivers for the Dexter Industries Inertial Measurement Unit sensor

# ROS_INERTIAL_MEASUREMENT_UNIT
#
# modified to allow initializing the BNO055 to a mode other than the default, full NDOF operation
# modified to use rosBNO055 (to set self._mode)
#

from __future__ import print_function
from __future__ import division

import rosBNO055 as BNO055


class InertialMeasurementUnit(object):
    """
    Class for interfacing with the `InertialMeasurementUnit Sensor`_.
    """
    def __init__(self, bus = "RPI_1SW", mode = BNO055.OPERATION_MODE_NDOF, init = True, verbose=False):
        """
        Constructor for initializing link with the `InertialMeasurementUnit Sensor`_.

        :param str bus = "RPI_1SW": The bus to which the distance sensor is connected to. By default, it's set to bus ``"RPI_1SW"``. Check the :ref:`hardware specs <hardware-interface-section>` for more information about the ports.
        :param bool init = True:  Enables/Disables hardware initialization.  False creates software object but does not change hardware configuration or mode.
        :param bool verbose = False: True provides additional console output of actions.
        :raises RuntimeError: When the chip ID is incorrect. This happens when we have a device pointing to the same address, but it's not a `InertialMeasurementUnit Sensor`_.
        :raises ~exceptions.OSError: When the `InertialMeasurementUnit Sensor`_ is not reachable.

        """
        try:
            if verbose:
                if (init==True):
                    print("InertialMeasurementUnit INSTANTIATING ON BUS {} TO MODE {} INIT {}".format(bus, mode, init))
                else:
                    print("InertialMeasurementUnit INSTANTIATING ON BUS {} INIT {} (no mode change)".format(bus, init))
            self.BNO055 = BNO055.BNO055(bus = bus, mode = mode, init = init, verbose = verbose)
        except RuntimeError:
            raise RuntimeError('Failed to initialize Dexter Industries IMU sensor')
        if verbose: print("InertialMeasurementUnit Instantiation Complete")

    def read_euler(self):
        """
        Read the absolute orientation.

        :returns: Tuple of euler angles in degrees of *heading*, *roll* and *pitch*.
        :rtype: (float,float,float)
        :raises ~exceptions.OSError: When the sensor is not reachable.

        """
        return  self.BNO055.read_euler()

    def read_magnetometer(self):
        """
        Read the magnetometer values.

        :returns: Tuple containing X, Y, Z values in *micro-Teslas* units. You can check the X, Y, Z axes on the sensor itself.
        :rtype: (float,float,float)
        :raises ~exceptions.OSError: When the sensor is not reachable.

        """
        return self.BNO055.read_magnetometer()

    def read_gyroscope(self):
        """
        Read the angular velocity of the gyroscope.

        :returns: The angular velocity as a tuple of X, Y, Z values in *degrees/s*. You can check the X, Y, Z axes on the sensor itself.
        :rtype: (float,float,float)
        :raises ~exceptions.OSError: When the sensor is not reachable.

        """
        return self.BNO055.read_gyroscope()

    def read_accelerometer(self):
        """
        Read the accelerometer.

        :returns: A tuple of X, Y, Z values in *meters/(second^2)* units. You can check the X, Y, Z axes on the sensor itself.
        :rtype: (float,float,float)
        :raises ~exceptions.OSError: When the sensor is not reachable.

        """
        return self.BNO055.read_accelerometer()

    def read_linear_acceleration(self):
        """
        Read the linear acceleration - that is, the acceleration from movement and without the gravitational acceleration in it.

        :returns: The linear acceleration as a tuple of X, Y, Z values measured in *meters/(second^2)* units. You can check the X, Y, Z axes on the sensor itself.
        :rtype: (float,float,float)
        :raises ~exceptions.OSError: When the sensor is not reachable.

        """
        return self.BNO055.read_linear_acceleration()

    def read_gravity(self):
        """
        Read the gravitational acceleration.

        :returns: The gravitational acceleration as a tuple of X, Y, Z values in *meters/(second^2)* units. You can check the X, Y, Z axes on the sensor itself.
        :rtype: (float,float,float)
        :raises ~exceptions.OSError: When the sensor is not reachable.

        """
        return self.BNO055.read_gravity()

    def read_quaternion(self):
        """
        Read the quaternion values.

        :returns: The current orientation as a tuple of X, Y, Z, W quaternion values.
        :rtype: (float,float,float,float)
        :raises ~exceptions.OSError: When the sensor is not present.

        """
        return self.BNO055.read_quaternion()

    def read_temperature(self):
        """
        Read the temperature in Celsius degrees.

        :returns: Temperature in Celsius degrees.
        :rtype: int
        :raises ~exceptions.OSError: When the sensor can't be contacted.

        """
        return self.BNO055.read_temp()
