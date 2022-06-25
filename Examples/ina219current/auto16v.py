#!/usr/bin/env python
from ina219 import INA219
from ina219 import DeviceRangeError
import logging


SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 1.0   # 12v at 0.75 expected


def read():
    # ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, log_level=logging.INFO)
    ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, log_level=logging.DEBUG)
    # ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
    ina.configure(ina.RANGE_16V)   # Choose lower voltage range

    print("Bus Voltage: %.3f V" % ina.voltage())
    try:
        print("Bus Current: %.3f mA" % ina.current())
        print("Power: %.3f mW" % ina.power())
        print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print(e)


if __name__ == "__main__":

    print("AUTO GAIN - MAX RESOLUTION using 16V RANGE")
    print("MAX_EXPECTED_AMPS = {:1.3f}A".format(MAX_EXPECTED_AMPS))
    read()

