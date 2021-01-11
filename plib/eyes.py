#!/usr/bin/env python3

# FILE: eyes.py
"""
  Allow setting Carl's eyes to display status
  - light blue: waiting for keyword "Marvin"
    (later "Carl", "Hey Carl", "Carl Listen" )
  - bright blue: simulates waiting for voice command mode
  - light green: simulates performing voice command
  - light red:   simulates voice command rejected
"""


# add Carl's plib to path
import sys
sys.path.append("/home/pi/Carl/plib")
import noinit_easygopigo3
from time import sleep

# ==== GoPiGo3 Eye Management =====

EYE_COLOR_COMMANDABLE = ( 0, 0,128)    # BRIGHT_BLUE
EYE_COLOR_HOTWORD     = ( 0, 0, 20)    # LIGHT_BLUE
EYE_COLOR_ACCEPTED    = ( 0,20,  0)    # LIGHT_GREEN
EYE_COLOR_REJECTED    = (20, 0,  0)    # LIGHT_RED
EYE_COLOR_OFF         = ( 0, 0,  0)    # OFF

def carl_eyes(egpg,newState=None):
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
		if (newState == EYE_COLOR_OFF) or (newState == False):
			egpg.close_eyes()
			newState = False
		else:
			egpg.set_eye_color(egpg._carl_eyes)
			egpg.open_eyes()


	# returns either False or color tuple
	return newState

# TEST MAIN FOR eyes.py
def main():
	egpg = noinit_easygopigo3.EasyGoPiGo3(use_mutex=True, noinit=True)

	print("\nTesting eyes.carl_eyes()")
	carlEyes = carl_eyes(egpg)
	print("carl_eyes() returned: ", carlEyes)

	print("\nTesting EYE_COLOR_HOTWORD")
	carl_eyes(egpg,EYE_COLOR_HOTWORD)
	carlEyes = carl_eyes(egpg)
	print("carl_eyes() returned: ", carlEyes)
	sleep(1)

	print("\nTesting EYE_COLOR_COMMANDABLE")
	carl_eyes(egpg,EYE_COLOR_COMMANDABLE)
	carlEyes = carl_eyes(egpg)
	print("carl_eyes() returned: ", carlEyes)
	sleep(1)

	print("\nTesting EYE_COLOR_ACCEPTED")
	carl_eyes(egpg,EYE_COLOR_ACCEPTED)
	carlEyes = carl_eyes(egpg)
	print("carl_eyes() returned: ", carlEyes)
	sleep(1)

	print("\nTesting EYE_COLOR_REJECTED")
	carl_eyes(egpg,EYE_COLOR_REJECTED)
	carlEyes = carl_eyes(egpg)
	print("carl_eyes() returned: ", carlEyes)
	sleep(1)

	print("\nTesting EYE_COLOR_OFF")
	carl_eyes(egpg,EYE_COLOR_OFF)
	carlEyes = carl_eyes(egpg)
	print("carl_eyes() returned: ", carlEyes)
	sleep(1)

	print("\nTesting carl_eyes(egpg,False)")
	carl_eyes(egpg,False)
	carlEyes = carl_eyes(egpg)
	print("carl_eyes() returned: ", carlEyes)





if __name__ == '__main__': main()
