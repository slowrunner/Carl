#!/usr/bin/env python
#
# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python example program for the Dexter Industries Distance Sensor

from __future__ import print_function
from __future__ import division

import time
from di_sensors.distance_sensor import DistanceSensor

print("Example program for reading a Dexter Industries Distance Sensor on an I2C port.")

# establish communication with the DistanceSensor
ds = DistanceSensor()

# set the sensor in fast-polling-mode
ds.start_continuous()

while True:
    # read the distance in millimeters
    read_distance = ds.read_range_continuous()
    print("distance from object: {} mm".format(read_distance))
