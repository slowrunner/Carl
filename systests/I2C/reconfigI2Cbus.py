#!/usr/bin/env python3
#
#
# Usage:  Attempt to fix fatal I2C bus errors condition
# ./reconfigI2Cbus.py
#



import time
from datetime import datetime as dt

import sys
import easygopigo3 # import the EasyGoPiGo3 class

from di_sensors.easy_inertial_measurement_unit import EasyIMUSensor

# Port must be "AD1" or "AD2" to force software I2C that properly implements clock stretch
PORT = "AD1"



def main():
    print("\nReconfiguring I2C bus using EasyIMUSensor().reconfig_bus()")
    print("   on GoPiGo3 port {}\n".format(PORT))

    try:
        imu = EasyIMUSensor(port = PORT, use_mutex = True)
    except Exception as e:
        print("EasyIMUSensor() instantiation failed")
        print(str(e)

    time.sleep(1.0)  # allow chip to initialize

    try:
        imu.reconfig_bus()
    except Exception as e:
        print("reconfigI2Cbus.py: Exception")
        print(str(e))
    except KeyboardInterrupt:
        print("\nCntrl-C detected. Exiting..")


# Invoke main() 
if __name__ == '__main__':
	main()

