#!/usr/bin/env python3

# FILE: carl_hotword_eyes.py
"""
  Demonstrates setting Carl's eyes to display status
  - light blue: waiting for keyword "Marvin"
    (later "Carl", "Hey Carl", "Carl Listen" )
  - bright blue: simulates waiting for voice command mode
  - light green: simulates performing voice command
  - light red:   simulates voice command rejected
"""

import time
import sys
import random

# add Carl's plib to path, after local, before system
sys.path.insert(1,"/home/pi/Carl/plib")
import hotword
import eyes
# import noinit_easygopigo3
import easygopigo3

# ==== carl_hotword_eyes.py  MAIN ====

def main():

	# egpg = noinit_easygopigo3.EasyGoPiGo3(use_mutex=True, noinit=True)
	egpg = easygopigo3.EasyGoPiGo3(use_mutex=True, noinit=True)

	while True:
		# Wait for wakup keyword/phrase
		try:
			print("\nListening For Hotword")
			eyes.carl_eyes(egpg,eyes.EYE_COLOR_HOTWORD)
			detected = hotword.detectKeywords()

		except KeyboardInterrupt:
			eyes.carl_eyes(egpg,eyes.EYE_COLOR_OFF)
			break

		if detected == "Exit":
			eyes.carl_eyes(egpg,eyes.EYE_COLOR_OFF)
			break

		# Listen For Command
		try:
			print("\nSimulating Listening For A Command")
			eyes.carl_eyes(egpg,eyes.EYE_COLOR_COMMANDABLE)
			time.sleep(3)
			if random.choice([True, False]):
				print("\nSimulating Command Accepted")
				eyes.carl_eyes(egpg,eyes.EYE_COLOR_ACCEPTED)
			else:
				print("\nSimulating Command Rejected")
				eyes.carl_eyes(egpg,eyes.EYE_COLOR_REJECTED)
			time.sleep(.5)
		except KeyboardInterrupt:
			eyes.carl_eyes(egpg,eyes.EYE_COLOR_OFF)
			break


if __name__ == '__main__': main()
