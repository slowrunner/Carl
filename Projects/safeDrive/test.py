#!/usr/bin/env python3

import time
from my_easygopigo3 import EasyGoPiGo3

def main():
    egpg = EasyGoPiGo3(use_mutex=True)

    print("Test Ready")

    print("\n10cm TEST DRIVE WILL BEGIN IN 5 SECONDS")
    time.sleep(5)
    egpg.drive_cm(10)

    print("\n-10cm TEST DRIVE WILL BEGIN IN 5 SECONDS")
    time.sleep(5)
    egpg.drive_cm(-10)

    print("\n50cm with .25sec timeout TEST DRIVE WILL BEGIN IN 5 SECONDS")
    time.sleep(5)
    egpg.drive_cm(50, timeout=0.25)

    print("\n-50cm with .25sec timeout TEST DRIVE WILL BEGIN IN 5 SECONDS")
    time.sleep(5)
    egpg.drive_cm(-50, timeout=0.25)


if (__name__ == "__main__"):  main()

