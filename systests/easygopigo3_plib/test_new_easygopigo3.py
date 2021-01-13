#!/usr/bin/env python3

# FILE: test_new_easygopigo3.py

import sys

# get local easygopigo3 and plib versions of everything else
import easygopigo3  # from local since/if it exists

sys.path.append('/home/pi/Carl/plib')

import tiltpan
import my_safe_inertial_measurement_unit

print("Testing local easygopigo3.py")
try:
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True, noinit=True)
except Exception as e:
    print("Exception while instantiating EasyGoPiGo3(noinit=True)")
    print("If complaint is TypeError: __init__() got an unexpected keyword argument \'noinit\'")
    print("Check that local easygopigo3.py exists (use make_locals.sh)")
    exit(1)

egpg.tp = tiltpan.TiltPan(egpg)

# use HW I2C: "RPI_1" default is SW I2C: "I2C"
egpg.ds = egpg.init_distance_sensor(port="RPI_1")

# port must be "AD1" or "AD2" for SW I2C with clock stretching
egpg.imu = my_safe_inertial_measurement_unit.SafeIMUSensor(port="AD1", use_mutex=True, init=False)

print("Success")

