#!/usr/bin/env python3
from ina219 import INA219
from ina219 import DeviceRangeError
import logging
import time

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 1.0   # 12v at 0.75 expected
AVE_SAMPLES = INA219.ADC_64SAMP  # ~35ms update  sample range 2-128


if __name__ == "__main__":


    logging.basicConfig(level=logging.INFO, format='%(asctime)s| %(message)s')
    print("AVERAGE OVER 64 SAMPLES, AUTO GAIN - MAX RESOLUTION using 16V RANGE")
    print("MAX_EXPECTED_AMPS = {:1.3f}A".format(MAX_EXPECTED_AMPS))
    # ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, log_level=logging.INFO)
    # ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, log_level=logging.DEBUG)
    ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
    # Choose lower voltage range, average over multiple samples
    ina.configure(ina.RANGE_16V, shunt_adc=AVE_SAMPLES) 

    mAh = 0
    Wh = 0
    tDischarge = time.time()
    tStart = time.time()
    while True:
        try:
            vBatt = ina.voltage()         # (bus) at the battery voltage
            vBot = ina.supply_voltage()   # voltage to bot
            iCur  = ina.current()      # mA
            iPwr  = ina.power()/1000.0        # W
            tNow = time.time()
            dT = (tNow - tStart)/3600.0  # hours
            tStart = time.time()
            tTotal = (tNow - tDischarge) / 3600.0

            mAh += (dT * iCur)
            Wh += (dT * iPwr)
            logging.info("vBatt {:.2f}  vBot {:.2f} volts    iCur {:>4.0f} mA {:4.0f} mAh     iPwr {:2.3f} W {:>4.2f} Wh    dT {:.3f} s  total {:3.1f}".format(vBatt,vBot,iCur,mAh,iPwr,Wh, dT*3660.0,tTotal))

        except DeviceRangeError as e:
            # Current out of device range with specified shunt resistor
            print("Current out of range with specified shunt resistor\n",e)
        except KeyboardInterrupt:
            break

        time.sleep(0.991)
