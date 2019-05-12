#!/usr/bin/env python3

# from https://github.com/nikhiljohn10/pi-clap

import pyaudio
import sys
import _thread
from time import sleep
from array import array

clap = 0
wait = 2
flag = 0
exitFlag = False


def toggleLight():
	print("Light toggled")
	sleep(1)

def waitForClaps(threadName):
	global clap
	global flag
	global wait
	global exitFlag
	print("Waiting for more claps")
	sleep(wait)
	if clap == 2:
		print("Two claps")
		toggleLight()
	# elif clap == 3:
	# 	print "Three claps"
	elif clap == 4:
		exitFlag = True
	print("Claping Ended")
	clap = 0
	flag = 0

def main():
	global clap
	global flag

	chunk = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	threshold = 3000
	max_value = 0
	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					output=True,
					frames_per_buffer=chunk)
	try:
		print("Clap detection initialized")
		while True:
			data = stream.read(chunk)
			as_ints = array('h', data)
			max_value = max(as_ints)
			if max_value > threshold:
				clap += 1
				print("Clapped")
			if clap == 1 and flag == 0:
				_thread.start_new_thread( waitForClaps, ("waitThread",) )
				flag = 1
			if exitFlag:
				sys.exit(0)
	except (KeyboardInterrupt, SystemExit):
		print("\rExiting")
		stream.stop_stream()
		stream.close()
		p.terminate()

if __name__ == '__main__':
	main()
