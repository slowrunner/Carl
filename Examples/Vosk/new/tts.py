#!/usr/bin/env python3

import sys
sys.path.insert(1,'/home/pi/Carl/plib')

import speak

while True:
	try:
		sayit = input("String to Speak: ")
		speak.say(sayit)
	except KeyboardInterrupt:
		print("\n")
		break

