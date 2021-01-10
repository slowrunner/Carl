#!/usr/bin/env python3

"""
FILE: voicecmdr.py

DESCRIPTION:
Combines ...   
- the Nyumaya Hotword speech recognition engine,  
  * (uses machine learning technology),
  * (extremely low processing load to conserve Carl's battery)
  * Recognizes hotword "Marvin" (soon "Carl", "Hey Carl", or "Carl Listen" )   
with ...
- the Vosk-API general speech recognition engine  
  * (uses machine learning technology),
  * With small language model especially for Raspberry Pi applications
  * Can be further constrained by a list of words
  * Recognizes multi-word commands

# voicecmdr.py

USAGE:  ./voicecmdr.py  

- When SOFT BLUE LIGHT eyes are on, (HOTWORD MODE) say "Marvin"  

- When BRIGHT BLUE LIGHT eyes are on, (COMMAND MODE), say a command:  
  * "quit voice commander" - will exit program   
  * "battery voltage" - will speak battery voltage  
  * "go to sleep" - ignore all commands until "wake up" command heard  
  * "be quiet", or "quiet mode" - only print to console and use eye color responses. Do not use TTS
  * "cancel quiet mode" - resume using TTS in responses
  * (more to come)  

- When SOFT RED LIGHT eyes are on, (SLEEP MODE) say command:  
  * "wake up" - to return to command mode  

- When BRIGHT GREEN LIGHT eyes are on, command accepted

- When BRIGHT RED LIGHT eyes are on, command rejected


"""


import time
import sys
import random

# add Carl's plib to path
sys.path.append("/home/pi/Carl/plib")

import noinit_easygopigo3
import hotword



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


# ==== voicecmdr.py  MAIN ====

def main():

	egpg = noinit_easygopigo3.EasyGoPiGo3(use_mutex=True, noinit=True)

	print("\n==== VOICE COMMANDER ====")

	while True:
		# Wait for wakup keyword/phrase
		try:
			print("\nListening For Hotword (Marvin)")
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

