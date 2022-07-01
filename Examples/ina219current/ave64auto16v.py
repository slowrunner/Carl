#!/usr/bin/env python3
from ina219 import INA219
from ina219 import DeviceRangeError
import logging
import time

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 1.0   # 12v at 0.75 expected
AVE_SAMPLES = INA219.ADC_64SAMP  # ~35ms update  sample range 2-128


def read():
    # ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, log_level=logging.INFO)
    # ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, log_level=logging.DEBUG)
    ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)

    # Choose lower voltage range, average over multiple samples
    ina.configure(ina.RANGE_16V, shunt_adc=AVE_SAMPLES) 
    print("")
    print("Bus Voltage: %.3f V" % ina.voltage())
    print("Supply Voltage: %.3f" % ina.supply_voltage())
    try:
        print("Bus Current: %.0f mA" % ina.current())
        print("Power: %.3f W" % (ina.power()/1000.0))
        print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print("Current out of range with specified shunt resistor\n",e)


if __name__ == "__main__":

    print("AVERAGE OVER 64 SAMPLES, AUTO GAIN - MAX RESOLUTION using 16V RANGE")
    print("MAX_EXPECTED_AMPS = {:1.3f}A".format(MAX_EXPECTED_AMPS))
    while True:
        try:
            read()
            time.sleep(5)
        except KeyboardInterrupt:
            break
