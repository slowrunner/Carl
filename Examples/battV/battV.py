#!/usr/bin/python3

# battV.py    Read Battery Voltage (thread-safe)


# IMPORTS
import time
from datetime import datetime
import easygopigo3

def printStatus(egpg):
    vBatt = egpg.volt()  # use thread-safe version not get_battery_voltage
    print("{} Battery Voltage: {:0.2f}".format( datetime.now().date(),vBatt))


# ##### MAIN ######


def main():

    # #### Create a mutex protected instance of EasyGoPiGo3 base class
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    try:
        while True:
            printStatus(egpg)
            time.sleep(5)
        # end while
    except KeyboardInterrupt:
        print("\nExiting battV.py")
        time.sleep(1)


if __name__ == "__main__":
    main()
