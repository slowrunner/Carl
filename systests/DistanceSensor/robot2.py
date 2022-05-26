#!/usr/bin/python3

# FILE: robot2.py

# PURPOSE: Test reading distance sensor and ultrasonic sensor

from easygopigo3 import EasyGoPiGo3
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

DIODE_DROP = 0.7
ULTRASONIC_CORRECTION_AT_100mm = 17.0 # mm
ToF_CORRECTION_AT_100mm = -3.0 # mm 

def main():
    egpg = EasyGoPiGo3(use_mutex=True)
    egpg.ds = egpg.init_distance_sensor()
    egpg.us = egpg.init_ultrasonic_sensor(port="AD1")

    while True:
        try:
            vBatt = egpg.volt()+DIODE_DROP
            dist_ds_mm = egpg.ds.read_mm()+ToF_CORRECTION_AT_100mm
            time.sleep(0.01)
            dist_us_mm = egpg.us.read_mm()+ULTRASONIC_CORRECTION_AT_100mm
            logging.info(": vBatt:{:>5.2f}v  ds:{:>5.0f}mm  us:{:>5.0f}mm".format(vBatt,dist_ds_mm,dist_us_mm))
            time.sleep(1)

        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
