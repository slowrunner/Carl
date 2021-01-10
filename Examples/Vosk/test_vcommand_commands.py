#!/usr/bin/env python3

"""
  FILE: test_vcommand_commands.py

  USAGE:
    ./test_vcommand_commands.py
    Say one of
    - battery voltage
    - exit voice command mode
    - be quiet
    - you can talk now
    - go to sleep
    - wake up

"""
import datetime as dt
import sys
import time

sys.path.append("/home/pi/Carl/plib")
import vcommand

def main():

	print("Starting test_vcommand_commands.py")
	while True:
		try:

			text = vcommand.getVoiceCommand(printResults=True)  # use to print word confidences
			# text = vcommand.getVoiceCommand()                   # normal use
			if text != "":
				vcommand.print_w_date_time("Voice Command: " + text)
			if vcommand.isExitRequest(text):
				break
			else:
				vcommand.doVoiceCommand(text)

		except KeyboardInterrupt:
			break
	print("\nExiting test_vcommand_commands.py")


if __name__ == '__main__': main()
