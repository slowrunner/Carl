#!/usr/bin/env python3

# FILE: carl_hotword.py

# Demonstrates using the Nyumaya Hotword engine
# via ~/Carl/plib/hotword.py


import sys
sys.path.append('/home/pi/Carl/plib')
import hotword
import time

def main():

	while True:
		detected = hotword.detectKeywords()
		if detected == "Exit":
			break
		# Hotword was detected, Do something

		# Since not doing anything in this demo program:
		#   Wait at least 0.1s for AudiostreamSource thread to die off
		#   before calling detectKeywords() again
		time.sleep(0.1)
if __name__ == '__main__': main()
