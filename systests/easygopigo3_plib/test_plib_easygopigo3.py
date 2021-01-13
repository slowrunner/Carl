#!/usr/bin/env python3

# FILE: test_plib_easygopigo3.py

import sys
# get plib version of everything

# get plib version of everything ignoring the local easygopigo3
sys.path.insert(0,'/home/pi/Carl/plib')  # note 0 puts it before local
import easygopigo3
import tiltpan
import my_safe_inertial_measurement_unit

print("Testing plib easygopigo3.py")
egpg = easygopigo3.EasyGoPiGo3(use_mutex=True, noinit=True)

egpg.tp = tiltpan.TiltPan(egpg)

# use HW I2C: "RPI_1" default is SW I2C: "I2C"
egpg.ds = egpg.init_distance_sensor(port="RPI_1")

# port must be "AD1" or "AD2" for SW I2C with clock stretching
egpg.imu = my_safe_inertial_measurement_unit.SafeIMUSensor(port="AD1", use_mutex=True, init=False)

print("Success")

