#!/usr/bin/env python3
"""
   Documentation

   Purpose:  Test new motor/encoder routines with timeouts in my_easygopigo3.py

   Usage:  ./test.py

   Result:
       - drive fwd 1m with default 60s timeout (cut short at 60s)
       - drive bwd 10cm with default 60s timeout
       - drive fwd 50cm with 0.25s timeout (cut short at 0.25s)
       - drive bwd 50cm with 0.25s timeout (cut short at 0.25s)
       - drive fwd 12in with 0.5s timeout  (cut short at 0.5s)
       - drive bwd 12in with 0.5s timeout (cut short at 0.5s)
       - turn cw  180 deg with 0.25s timeout (cut short at 0.25s)
       - turn ccw 180 deg with 0.25s timeout (cut short at 0.25s)
       - turn cw  180 deg with default 60s timeout
       - turn ccw 180 deg with default 60s timeout
       - drive fwd 10cm with default 60s timeout
       - drive bwd 1m with default 60s timeout (cut short at 60s)


import time
from my_easygopigo3 import EasyGoPiGo3

def main():
    egpg = EasyGoPiGo3(use_mutex=True)

    egpg.set_speed(150)

    print("Test Ready")

    print("\n1m (100 cm) with default 60s timeout TEST DRIVE WILL BEGIN IN 5 SECONDS")
    time.sleep(5)
    egpg.drive_cm(100)

    print("\n-10cm with default 60s timeout TEST DRIVE WILL BEGIN IN 5 SECONDS")
    time.sleep(5)
    egpg.drive_cm(-10)

    print("\n50cm with .25sec timeout TEST DRIVE WILL BEGIN IN 5 SECONDS")
    time.sleep(5)
    egpg.drive_cm(50, timeout=0.25)

    print("\n-50cm with .25sec timeout TEST DRIVE WILL BEGIN IN 5 SECONDS")
    time.sleep(5)
    egpg.drive_cm(-50, timeout=0.25)

    print("\n12in with .25sec timeout TEST DRIVE WILL BEGIN IN 5 SECONDS")
    time.sleep(5)
    egpg.drive_inches(12, timeout=0.25)

    print("\n-12in with .25sec timeout TEST DRIVE WILL BEGIN IN 5 SECONDS")
    time.sleep(5)
    egpg.drive_inches(-12, timeout=0.25)


    print("\n180 degrees with 0.5sec timeout TEST SPIN WILL BEGIN IN 5 SECONDS")
    time.sleep(5)
    egpg.turn_degrees(180, timeout=0.5)

    print("\n-180 degrees with 0.5sec timeout TEST SPIN WILL BEGIN IN 5 SECONDS")
    time.sleep(5)
    egpg.turn_degrees(-180, timeout=0.5)

    print("\n180 degrees with default timeout TEST SPIN WILL BEGIN IN 5 SECONDS")
    time.sleep(5)
    egpg.turn_degrees(180)

    print("\n-180 degrees with default timeout TEST SPIN WILL BEGIN IN 5 SECONDS")
    time.sleep(5)
    egpg.turn_degrees(-180)

    print("\n10cm with default 60s timeout TEST DRIVE WILL BEGIN IN 5 SECONDS")
    time.sleep(5)
    egpg.drive_cm(10)

    print("\n-1m (100 cm) with default 60s timeout TEST DRIVE WILL BEGIN IN 5 SECONDS")
    time.sleep(5)
    egpg.drive_cm(-100)


if (__name__ == "__main__"):  main()

