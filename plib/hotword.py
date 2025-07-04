#!/usr/bin/env python3

# FILE: hotword.py



import os
import argparse
import sys
import datetime
import time
sys.path.insert(1,"/home/pi/Carl/plib")
import voiceLog

nyumaya_engine_carl = "/home/pi/Carl/nyumaya_engine_carl"
# This is the libpath to pass to detectKeywords(hotword.nyumaya_libpath)
nyumaya_libpath = nyumaya_engine_carl + '/lib/rpi/armv7/libnyumaya_premium.so'

sys.path.append(nyumaya_engine_carl+'/python/src')

from libnyumaya import AudioRecognition, FeatureExtractor
from auto_platform import AudiostreamSource, play_command,default_libpath


# ==== detectKeywords(libpath) ======

def detectKeywords(libpath=nyumaya_libpath):

	audio_stream = AudiostreamSource()
	"""
	# The following was needed before configuring /home/pi/.asoundrc from ~/Carl/configs/home.pi.dot.asoundrc.PiOS
	audio_stream.input_device = 'plughw:2,0'
	audio_stream._cmd = [
			'arecord',
			'-q',
			'-t', 'raw',
			'-D', audio_stream.input_device,
			'-c', str(audio_stream.channels),
			'-f', 's16',
			'-r', str(audio_stream.sample_rate),
		]
	print("arecord cmd:",audio_stream._cmd)
	"""
	extractor = FeatureExtractor(libpath)
	detector = AudioRecognition(libpath)

	extactor_gain = 1.0

	# keywordIdFirefox = detector.addModel('../../models/Hotword/firefox_v1.2.0.premium',0.6)
	# keywordIdSheila = detector.addModel('../../models/Hotword/sheila_v1.2.0.premium',0.6)
	# keywordIdMarvin = detector.addModel('../../models/Hotword/marvin_v1.2.0.premium',0.6)
	# keywordIdAlexa = detector.addModel('../../models/Hotword/alexa_v1.2.0.premium',0.6)

	# keywordIdMarvin = detector.addModel(nyumaya_engine_carl + '/models/Hotword/marvin_v1.2.0.premium',0.6)
	keywordIdHey_Carl = detector.addModel(nyumaya_engine_carl + '/models/Hotword/hey_carl_v1.2.3.premium',0.6)

	bufsize = detector.getInputDataSize()

	# print("Audio Recognition Version: " + detector.getVersionString())

	audio_stream.start()
	detected = None

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
				# if(prediction == keywordIdMarvin):
				# 	print("Marvin detected:" + now)
				# 	detected = "Marvin"
				# 	break
				if(prediction == keywordIdHey_Carl):
					print("Hey Carl detected:" + now)
					detected = "Hey Carl"
					voiceLog.entry("Hey Carl detected")
					break
				# elif(prediction == keywordIdAlexa):
					# print("Alexa detected:" + now)

				# os.system(play_command + " ../resources/ding.wav")

	except KeyboardInterrupt:
		print("\nNo Longer Listening")
		detected = "Exit"

	finally:
		audio_stream.stop()

	print("detectKeywords() returning:",detected)
	return detected



# USAGE:
# 		detected = detectKeywords()

#		if detected == "Exit":
#			exit(0) 
