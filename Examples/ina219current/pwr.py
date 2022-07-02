#!/usr/bin/env python3

"""
  FILE: pwr.py

  PURPOSE:  Log to terminal voltage, current, power usage from INA219a

  OUTPUT:

2022-07-02 11:46:32,845| vBatt 11.72  vBot 11.70 volts    iCur -286 mA -764 mAh     iPwr 3.346 W 8.55 Wh    dT 1.001 s  total 2.5

  CONFIGUATION:  128 samples in 68ms integrated as approximately 1 second intervals

  ACCURACY:  (Tested against Eversame USB C Power Meter Tester)
             Instantaneous Voltage appears to be within 20 mV low
             Instantaneous Current within 3mA, 
             Total mAh and Wh within 1% (perhaps estimates slightly high)
"""

from ina219 import INA219
from ina219 import DeviceRangeError
import logging
import time

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 1.0   # 12v at 0.75 expected
# AVE_SAMPLES = INA219.ADC_4SAMP   # ~ 2ms update  sample range 2-128
# AVE_SAMPLES = INA219.ADC_64SAMP  # ~35ms update  sample range 2-128
AVE_SAMPLES = INA219.ADC_128SAMP  # ~68ms update  sample range 2-128
SAMPLES = pow(2,(AVE_SAMPLES-8))

if __name__ == "__main__":


    logging.basicConfig(level=logging.INFO, format='%(asctime)s| %(message)s')
    print("AVERAGE OVER {} SAMPLES, AUTO GAIN - MAX RESOLUTION using 16V RANGE".format(SAMPLES))
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
    cntr = 0
    while True:
        try:
            cntr += 1
            vShunt = ina.shunt_voltage()/1000.0  # mv to volts
            vBot = ina.voltage()           # (bus) at the bot voltage
            vBatt = ina.supply_voltage()   # bus + shunt voltage
            if vShunt < 0:                 # if shunt voltage is negative, appears like battery is less than bot
                vBatt += 2 * abs(vShunt)   # needed to add the absolute value of shunt instead of the negative voltage

            iCur  = ina.current()      # mA
            iPwr  = ina.power()/1000.0        # W
            tNow = time.time()
            dT = (tNow - tStart)/3600.0  # hours
            tStart = time.time()
            tTotal = (tNow - tDischarge) / 3600.0

            mAh += (dT * iCur)
            Wh += (dT * iPwr)
            if (cntr % 10 == 0):
                logging.info("vBatt {:.2f}  vBot {:.2f} volts    iCur {:>4.0f} mA {:4.0f} mAh     iPwr {:2.3f} W {:>4.2f} Wh    dT {:.3f} s  total {:3.1f} h".format(vBatt,vBot,iCur,mAh,iPwr,Wh, dT*3660.0,tTotal))

        except DeviceRangeError as e:
            # Current out of device range with specified shunt resistor
            print("Current out of range with specified shunt resistor\n",e)
        except KeyboardInterrupt:
            break

        time.sleep(0.974)
