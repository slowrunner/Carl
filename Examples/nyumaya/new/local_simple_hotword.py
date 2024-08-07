#!/usr/bin/env python3

# FILE:  local_simple_hotword.py

# Demonstrates the simple_hotword.py example  
#   using Carl's local, fixed version of the Nyumaya engine  

import time
import os
import argparse
import sys
import datetime

nyumaya_engine_carl = "/home/pi/Carl/nyumaya_engine_carl"
nyumaya_carl_libpath = nyumaya_engine_carl + '/lib/rpi/armv7/libnyumaya_premium.so'

#sys.path.append('../../python/src')
sys.path.append(nyumaya_engine_carl+'/python/src')

from libnyumaya import AudioRecognition, FeatureExtractor
from auto_platform import AudiostreamSource, play_command,default_libpath

def detectKeywords(libpath):

	audio_stream = AudiostreamSource()
	extractor = FeatureExtractor(libpath)
	detector = AudioRecognition(libpath)

	extactor_gain = 1.0

	# keywordIdFirefox = detector.addModel('../../models/Hotword/firefox_v1.2.0.premium',0.6)
	# keywordIdSheila = detector.addModel('../../models/Hotword/sheila_v1.2.0.premium',0.6)
	# keywordIdMarvin = detector.addModel('../../models/Hotword/marvin_v1.2.0.premium',0.6)
	# keywordIdAlexa = detector.addModel('../../models/Hotword/alexa_v1.2.0.premium',0.6)

	keywordIdMarvin = detector.addModel(nyumaya_engine_carl+'/models/Hotword/marvin_v1.2.0.premium',0.6)
	# keywordIdMarvin = detector.addModel('nyumaya_models_carl/Hotword/hey_carl_v1.2.0.premium',0.6)

	bufsize = detector.getInputDataSize()

	print("Audio Recognition Version: " + detector.getVersionString())

	audio_stream.start()
	try:
		while(True):
			frame = audio_stream.read(bufsize*2,bufsize*2)
			if(not frame):
				time.sleep(0.01)
				continue

			features = extractor.signalToMel(frame,extactor_gain)

			prediction = detector.runDetection(features)
			if(prediction != 0):
				now = datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S")
				# if(prediction == keywordIdFirefox):
					# print("Firefox detected:" + now)
				# elif(prediction == keywordIdSheila):
					# print("Sheila detected:" + now)
				#elif(prediction == keywordIdMarvin):
				if(prediction == keywordIdMarvin):
					print("Marvin detected:" + now)
				# elif(prediction == keywordIdAlexa):
					# print("Alexa detected:" + now)

				# os.system(play_command + " ../resources/ding.wav")

	except KeyboardInterrupt:
		print("Terminating")
		audio_stream.stop()
		sys.exit(0)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument(
		'--libpath', type=str,
		# default=default_libpath,
		default=nyumaya_carl_libpath,
		help='Path to Platform specific nyumaya_lib.')


	FLAGS, unparsed = parser.parse_known_args()
	print("FLAGS:",FLAGS)

	detectKeywords(FLAGS.libpath)
