#!/usr/bin/env python
#
# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python example program for the Dexter Industries IMU Sensor

from __future__ import print_function
from __future__ import division

import time
from easy_inertial_measurement_unit import EasyIMUSensor

print("create.py: Example instantiating a Dexter Industries IMU Sensor on GoPiGo3 AD1 port.")
imu = EasyIMUSensor(port = "AD1")

time.sleep(1.0) # allow warmup
print("create.py complete")
