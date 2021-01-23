#!/usr/bin/env python3

"""
FILE: voicecmdr.py

DESCRIPTION:
Combines ...   
- the Nyumaya Hotword speech recognition engine,  
  * (uses machine learning technology),
  * (extremely low processing load to conserve Carl's battery)
  * Recognizes hotword "Hey Carl" (soon "Carl", or "Carl Listen" )  
with ...
- the Vosk-API general speech recognition engine  
  * (uses machine learning technology),
  * With small language model especially for Raspberry Pi applications
  * Can be further constrained by a list of words
  * Recognizes multi-word commands

# voicecmdr.py

USAGE:  ./voicecmdr.py  

- When SOFT BLUE LIGHT eyes are on, (HOTWORD MODE) say "Hey Carl"  

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
import traceback

# add Carl's plib to path and use plib easygopigo3
sys.path.insert(1,"/home/pi/Carl/plib")

import easygopigo3
import voiceLog
import hotword
import vcommand
import eyes
import tiltpan
import speak
from my_safe_inertial_measurement_unit import SafeIMUSensor
import runLog

"""
eyes.EYE_COLOR_COMMANDABLE = ( 0, 0,255)    # BRIGHT_BLUE
eyes.EYE_COLOR_HOTWORD     = ( 0, 0, 20)    # LIGHT_BLUE
eyes.EYE_COLOR_NL          = (50,50, 50)    # LIGHT_WHITE
eyes.EYE_COLOR_ACCEPTED    = ( 0,20,  0)    # LIGHT_GREEN
eyes.EYE_COLOR_REJECTED    = (20, 0,  0)    # LIGHT_RED
eyes.EYE_COLOR_OFF         = ( 0, 0,  0)    # OFF
"""

# ==== voicecmdr.py  MAIN ====
@runLog.logRun
@voiceLog.logRun
def main():
	# Using plib version of easygopigo3 to get noinit feature
	egpg = easygopigo3.EasyGoPiGo3(use_mutex=True, noinit=True)
	egpg.tp = tiltpan.TiltPan(egpg)
	egpg.ds = egpg.init_distance_sensor("RPI_1")  # HW I2C
	egpg.imu = SafeIMUSensor(port = "AD1", use_mutex = True)

	print("\n==== VOICE COMMANDER ====")
	voiceLog.entry("==== VOICE COMMANDER ====")

	cmd_mode = True
	verbose = True

	while True:
		# Wait for wakup keyword/phrase
		try:
			print("\n")
			msg="Listening For Hotword (Hey Carl)"
			print(msg)
			voiceLog.entry(msg)

			eyes.carl_eyes(egpg,eyes.EYE_COLOR_HOTWORD)
			detected = hotword.detectKeywords()

		except KeyboardInterrupt:
			eyes.carl_eyes(egpg,eyes.EYE_COLOR_OFF)
			break

		if detected == "Exit":
			eyes.carl_eyes(egpg,eyes.EYE_COLOR_OFF)
			break

		# Listen For Command or Natural Language Phrase
		try:
			if cmd_mode:
				print("\n")
				msg = "Listening For A Command"
				print(msg)
				voiceLog.entry(msg)
				eyes.carl_eyes(egpg,eyes.EYE_COLOR_COMMANDABLE)
				vcommand.reset_turn_start()
				try:
					vcmd = vcommand.getVoiceCommand(timeout=10)
				except Exception as e:
					print("Exception: ",str(e))
					traceback.print_exc()
					eyes.carl_eyes(egpg,eyes.EYE_COLOR_REJECTED)
					# print("WAITING 60 SECONDS FOR pyaudio TO CLEAR")
					time.sleep(5)
					# vcommand.reset_turn_start()
					# print("Trying again to launch Vosk command engine")
					# vcmd = vcommand.getVoiceCommand(timeout=10)
					eyes.carl_eyes(egpg,eyes.EYE_COLOR_OFF)
					time.sleep(1)
					break
				if vcommand.isExitRequest(vcmd):
					eyes.carl_eyes(egpg,eyes.EYE_COLOR_REJECTED)
					voiceLog.entry("Heard {}".format(vcmd))
					time.sleep(1)
					break
				elif vcmd == "TimeOut":
					print("Command not heard before turn timeout")
					eyes.carl_eyes(egpg,eyes.EYE_COLOR_REJECTED)
					time.sleep(1)
				elif "natural language" in vcmd:
					voiceLog.entry("Heard {}".format(vcmd))
					msg="Entering Natural Language Mode"
					print(msg)
					voiceLog.entry(msg)
					cmd_mode = False
					eyes.carl_eyes(egpg,eyes.EYE_COLOR_ACCEPTED)
					time.sleep(1)
				else:
					eyes.carl_eyes(egpg,eyes.EYE_COLOR_ACCEPTED)
					try:
						voiceLog.entry("Calling vcommand.doVoiceAction({}) ".format(vcmd))
						vcommand.doVoiceAction(vcmd,egpg)
						if vcmd == "be quiet":
							verbose = False
						elif vcmd == "you can talk now":
							verbose = True
					except KeyboardInterrupt:
						break
					except Exception as e:
						print("Exception in vcommand.doVoiceCommand")
						print(str(e))
						traceback.print_stack()
			try:  # nlu mode
				while cmd_mode == False:
					print("\n")
					msg="Listening For Natural Language"
					print(msg)
					voiceLog.entry(msg)
					eyes.carl_eyes(egpg,eyes.EYE_COLOR_NL)
					vcommand.reset_turn_start()
					vphrase = vcommand.getVoiceNL(timeout=15)
					if vcommand.isExitRequest(vphrase):
						eyes.carl_eyes(egpg,eyes.EYE_COLOR_REJECTED)
						time.sleep(1)
						break
					elif "command mode" in vphrase:
						eyes.carl_eyes(egpg,eyes.EYE_COLOR_ACCEPTED)
						voiceLog.entry("Heard {}".format(vphrase))
						alert = "Returning to COMMAND MODE"
						print(alert)
						voiceLog.entry(alert)
						cmd_mode = True
						if verbose:
							speak.say(alert)

					elif vphrase == "TimeOut":
						print("Nothing heard before turn timeout")
						eyes.carl_eyes(egpg,eyes.EYE_COLOR_REJECTED)
						time.sleep(1)
					else:
						eyes.carl_eyes(egpg,eyes.EYE_COLOR_ACCEPTED)
						try:
							msg="Heard: {}".format(vphrase)
							print(msg)
							voiceLog.entry(msg)
							if verbose:
								speak.say("I heard ")
								time.sleep(0.8)
								speak.say(vphrase)
							voiceLog.entry("Calling vcommand.doVoiceAction({})".format(vphrase))
							vcommand.doVoiceAction(vphrase,egpg)
						except KeyboardInterrupt:
							break
						except Exception as e:
							print("Exception in vcommand.doVoiceAction")
							print(str(e))
							traceback.print_stack()
			except Exception as e:
				print("Exception in natural language mode section")
				print(str(e))
				traceback.print_stack()







		except KeyboardInterrupt:
			eyes.carl_eyes(egpg,eyes.EYE_COLOR_REJECTED)
			time.sleep(1)
			break

	print("Exiting voicecmdr.py")
	eyes.carl_eyes(egpg,eyes.EYE_COLOR_OFF)


if __name__ == '__main__': main()

