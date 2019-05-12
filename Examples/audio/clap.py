#!/usr/bin/env python3

# from https://github.com/nikhiljohn10/pi-clap

# to install pyaudio
# sudo pip install portaudio19-dev
# sudo pip install pyaudio

# ignore all the alsa configuration errors - it will work
# had to set exception_on_overflow = False on the read or always got exception


import pyaudio
import sys
import _thread
from time import sleep
from array import array

try:
	sys.path.append('/home/pi/Carl/plibx')
	import speak
	Carl = True
except:
	Carl = False

clap = 0
wait = 2
flag = 0
exitFlag = False


def toggleLight():
	print("Light toggled")
	if Carl:
		speak.say("Yes master, I heard you.")
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
	elif clap == 3:
	 	print("Three claps")
	elif clap == 4:
		print("Four claps")
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
	print("mic sample rate:",p.get_device_info_by_index(0)['defaultSampleRate'])
	try:
		print("Clap detection initialized")
		while True:
			data = stream.read(chunk, exception_on_overflow = False)
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
