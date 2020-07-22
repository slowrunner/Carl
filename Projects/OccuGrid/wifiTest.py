#!/usr/bin/python3

# FILE: wifiTest.py

# REQUIRES:
#         sudo pip3 install wifi

# USAGE:
#         ./wifiTest.py for 1/minute scans
#         sudo ./wifiTest.py for continuous scans

# NOTES:
#        - The USB WiFi Adapter does not return actual signal strength (program shows it as constnt -50)

import wifi
import time
from datetime import datetime
import os
import subprocess

def main():

    if os.geteuid() == 0:
        print("Priviledged Run")
    else:
        print("NonPriviledged Run")

    ip0 = subprocess.getoutput("ifconfig wlan0 | grep 'inet '")
    ip1 = subprocess.getoutput("ifconfig wlan1 | grep 'inet '")
    print("wlan0 address:",ip0)
    print("wlan1 address:",ip1)
    print("\n")

    sig0 = 0
    sig1 = 0

    last_sig0 = 0
    last_sig1 = 0

    while True:
        try:
            # if priviledged scan, otherwise return once per minute cached value
            cell0 = list(wifi.Cell.all('wlan0'))[0]
            cell1 = list(wifi.Cell.all('wlan1'))[0]
            sig0 = cell0.signal
            sig1 = cell1.signal

            if (sig0 != last_sig0) or (sig1 != last_sig1):
                print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                print("wlan0:",sig0, cell0.quality)
                print("wlan1:",sig1, cell1.quality, "\n")
                last_sig0 = sig0
                last_sig1 = sig1
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("\ncntr-c detected, exiting")
            break
        except Exception as e:
            # once a minute the OS scans wlan0 
            # if running priviledged causes device busy exception

            # print("Exception: {}".format(str(e)))
            continue


if __name__ == '__main__':  main()


