#!/usr/bin/env python3
#
# FILE: gopigo_hw_read_info.py
#       (from ~/Dexter/GoPiGo3/Software/Python/Examples/Read_Info.py)
#
# PURPOSE: Read GoPiGo3 hardware and firmware information
#
# https://www.dexterindustries.com/GoPiGo/
# https://github.com/DexterInd/GoPiGo3
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md
#
# This code is an example for reading GoPiGo3 information
#
# Results: Print information about the attached GoPiGo3.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''


# Use insert plib first in path to get gopigo3.py from plib/ not from gopigo3 site-package
import sys
sys.path.insert(1,"/home/pi/Carl/plib/")

import gopigo3 # import the GoPiGo3 drivers

try:
    GPG = gopigo3.GoPiGo3() # Create an instance of the GoPiGo3 class. GPG will be the GoPiGo3 object.

    # Each of the following GPG.get functions return a list of 2 values
    print("Manufacturer    : ", GPG.get_manufacturer()    ) # read and display the serial number
    print("Board           : ", GPG.get_board()           ) # read and display the serial number
    print("Serial Number   : ", GPG.get_id()              ) # read and display the serial number
    print("Hardware version: ", GPG.get_version_hardware()) # read and display the hardware version
    print("Firmware version: ", GPG.get_version_firmware()) # read and display the firmware version
    print("Battery voltage : ", GPG.get_voltage_battery() ) # read and display the current battery voltage
    print("5v voltage      : ", GPG.get_voltage_5v()      ) # read and display the current 5v regulator voltage
    print("\nThe following are from /home/pi/Dexter/gpg3_config.json if exists otherwise from gopigo3.py")
    print("WHEEL DIAMETER  : ", GPG.WHEEL_DIAMETER        )
    print("WHEEL BASE WIDTH: ", GPG.WHEEL_BASE_WIDTH      )
    print("ENCODER TICKS PER ROTATION: ", GPG.ENCODER_TICKS_PER_ROTATION )
    print("MOTOR TICKS PER DEGREE    : ", GPG.MOTOR_TICKS_PER_DEGREE     )
except IOError as error:
    print(error)

except gopigo3.FirmwareVersionError as error:
    print(error)
