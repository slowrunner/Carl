#!/usr/bin/env python3

"""
  FILE: test_vcommand_nl.py

  USAGE:
    ./test_vcommand_nl.py
    Say phrase

"""
import datetime as dt
import sys
import time

# Use local, then plib, then system stuff
sys.path.insert(1,"/home/pi/Carl/plib")
import vcommand

def main():

	print("Starting test_vcommand_nl.py")
	while True:
		try:

			text = vcommand.getVoiceNL(printResults=True,timeout=15)  # use to print word confidences
			# text = vcommand.getVoiceNL()                   # normal use
			if text != "":
				vcommand.print_w_date_time("Phrase Heard: " + text)
			if vcommand.isExitRequest(text):
				break
			else:
				print("Phrase Heard: ", text)
				# vcommand.doVoiceNLU(text)
				# Normally would exit and go back to hotword reco, 
				# but reset the turn start time to test timeouts
				if text == "TimeOut":
					vcommand.reset_turn_start()
		except KeyboardInterrupt:
			break
	print("\nExiting test_vcommand_commands.py")


if __name__ == '__main__': main()
