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

# add Carl's plib to path
sys.path.append("/home/pi/Carl/plib")
import hotword

import noinit_easygopigo3

# ==== GoPiGo3 Eye Management =====

EYE_COLOR_COMMANDABLE = ( 0, 0,255)    # BRIGHT_BLUE
EYE_COLOR_HOTWORD     = ( 0, 0, 20)    # LIGHT_BLUE
EYE_COLOR_ACCEPTED    = ( 0,20,  0)    # LIGHT_GREEN
EYE_COLOR_REJECTED    = (20, 0,  0)    # LIGHT_RED
EYE_COLOR_OFF         = ( 0, 0,  0)    # OFF

def carl_eyes(egpg,newState):
	if newState == None:
		try:
			newState = egpg._carl_eyes
			if newState == EYE_COLOR_OFF:
				newState = False
		except:
			egpg._carl_eyes = EYE_COLOR_OFF
			egpg.close_eyes()
			newState = False

	else:
		egpg._carl_eyes = newState
		if newState == EYE_COLOR_OFF:
			egpg.close_eyes()
			newState = False
		else:
			egpg.set_eye_color(egpg._carl_eyes)
			egpg.open_eyes()


	# returns either False or color tuple
	return newState


# ==== carl_hotword_eyes.py  MAIN ====

def main():

	egpg = noinit_easygopigo3.EasyGoPiGo3(use_mutex=True, noinit=True)

	while True:
		# Wait for wakup keyword/phrase
		try:
			print("\nListening For Hotword")
			carl_eyes(egpg,EYE_COLOR_HOTWORD)
			detected = hotword.detectKeywords()

		except KeyboardInterrupt:
			carl_eyes(egpg,EYE_COLOR_OFF)
			break

		if detected == "Exit":
			carl_eyes(egpg,EYE_COLOR_OFF)
			break

		# Listen For Command
		try:
			print("\nSimulating Listening For A Command")
			carl_eyes(egpg,EYE_COLOR_COMMANDABLE)
			time.sleep(3)
			if random.choice([True, False]):
				print("\nSimulating Command Accepted")
				carl_eyes(egpg,EYE_COLOR_ACCEPTED)
			else:
				print("\nSimulating Command Rejected")
				carl_eyes(egpg,EYE_COLOR_REJECTED)
			time.sleep(.5)
		except KeyboardInterrupt:
			carl_eyes(egpg,EYE_COLOR_OFF)
			break


if __name__ == '__main__': main()
