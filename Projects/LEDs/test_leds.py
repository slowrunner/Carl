#!/usr/bin/env python3

# FILE:  test_leds.py

# PURPOSE:  test the leds.py module

import sys
sys.path.insert(1,"/home/pi/Carl/plib")
import leds
import easygopigo3
import time

egpg = easygopigo3.EasyGoPiGo3(use_mutex=True, noinit=True)

blinking = False

while True:
	try:
		if blinking == False:
			leds.wifi_blinker_on(egpg,leds.VIOLET)
			blinking = True
		else:
			pass
		time.sleep(1)

	except KeyboardInterrupt:
		leds.wifi_blinker_off(egpg)
		print("\nExiting")
		break
