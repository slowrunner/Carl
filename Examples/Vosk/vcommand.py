
# FILE: vcommand.py

"""
   getVoiceCommand()
   getVoiceNL()

   Provides Carl programs easy access to the Vosk-API voice recognition engine
   and the downloaded language model in ~/Carl/vosk-api/model
    - Sets pyaudio to use input_device_index=1
    - Sets Initialization Logging off
      (Audio system warnings cannot be surpressed)
    - Sets partial result off
    - Adds CTRL-C handler return "Exit"
    - Keeps track of time since last command, returns "TimeOut" if too long
    - getVoiceCommand() uses word lists
    - getVoiceNL() uses RPI small language model


   isExitRequest(command)

   Provide test if user requested "exit voice command mode" or pressed CTRL-c




   doVoiceAction(action_reqeust, cmd_mode)

   Provides Carl programs a command and natural language action handler




   Usage:
       import sys
        sys.path.index(1,'/home/pi/Carl/plib')  # add plib/ after local and before DI files
        import vcommand

	# voice command loop
	while True:
	        # vcmd = vcommand.getVoiceCommand(printResult=True)  # to print confidence for each word
	        vcmd = vcommand.getVoiceCommand()
		if vcommand.isExitRequest(vcmd):
			break
		else:
			vcommand.doVoiceAction(vcmd)

	# or natural language loop
	while True:
		# phrase = vcommand.getVoiceNL(printResult=True)  # to print confidence for each word
		vphrase = vcommand.getVoiceNL()
		if vcommand.isExitRequest(vphrase):
			break
		else:
			vcommand.doVoiceAction(vphrase)


"""

from vosk import Model, KaldiRecognizer, SetLogLevel
import os
import datetime as dt
import json
import traceback
import ast
import time
import wikipedia

import sys
sys.path.insert(1,"/home/pi/Carl/plib")  # after local, before DI 
import speak
import status
import tiltpan
import carlDataJson as carlData
import myDistSensor


vosk_model_path = "/home/pi/Carl/vosk-api/model"

if not os.path.exists(vosk_model_path):
    print ("Please download a model from https://alphacephei.com/vosk/models and unpack as 'model' in ~/Carl/vosk-api/")
    exit (1)

import pyaudio

def print_w_date_time(alert,event_time=None):
    if event_time is None: event_time = dt.datetime.now()
    str_event_time = event_time.strftime("%Y-%m-%d %H:%M:%S")
    print("{} {}".format(str_event_time,alert))


"""
    printResult(res)

    Pretty print for Vosk results

Result: 3 words
 0.28 carl
 1.00 wake
 1.00 up
Text: carl wake up

Usage:
import vcommand

res = rec.Result()
text = vcommand.printResult(res)

"""

def printResult(res):
    jres = json.loads(res)
    result_text = ""
    if "result" in jres:
        jresult=jres["result"]
        print("printResult: jresult:", jresult)

        num_words = len(jresult)
        print("Result: {} words".format(num_words))

        for i in range(num_words):
            print("{:>5.2f} {:<s}".format(jresult[i]["conf"],jresult[i]["word"]))
        result_text = jres["text"]
        print("Text: {}".format(result_text))
    return result_text

def getText(res):
    jres = json.loads(res)
    result_text = ""
    if "result" in jres:
        jresult=jres["result"]
        result_text = jres["text"]
    return result_text



SetLogLevel(-1)

"""
  VOICE COMMANDS

  Set of interpretable commands
"""
cmd_keywords = '["list commands", \
		"exit voice command mode", \
		"be quiet", \
		"you can talk now", \
		"go to sleep", \
		"wake up", \
		"whats the weather like long quiet", \
		"up time since boot", \
		"charging state", \
		"playtime status", \
		"recharge status", \
		"natural language mode", \
		\
		"battery voltage", \
		"turn around", \
		"nod yes",  \
		"nod no", \
		"nod i dont know", \
		"drive centimeters forward backward backup negative two five ten one hundred", \
		"drive inches forward backward backup negative two six twelve twenty four thirty six", \
		"turn degrees counter clockwise negative fifteen thirty forty five ninety", \
		"distance sensor reading in centimeters inches", \
		"pan left right fifteen thirty forty five sixty ninety to of center degrees", \
		"tilt up down fifteen thirty forty five sixty to level degrees", \
		\
		"[unk]"]'

nlu_actions = [ "look up something",
		"search something"]


# path to the language model (from vosk-model-small-en-us-0.15)
model = Model(vosk_model_path)
vosk_rate = 16000

# doVoice Command or NL or Action State variables

sleeping = False
verbose  = True
override_quiet_time = False
dt_turn_start = None


def reset_turn_start():
	global dt_turn_start
	dt_turn_start = dt.datetime.now()

def seconds_since_turn_start():
	global dt_turn_start
	dtNow = dt.datetime.now()
	ssts = (dtNow-dt_turn_start).total_seconds()
	# print("seconds_since_turn_start(): ",ssts)
	return ssts

# getVoiceCommand()
"""
    get a voice command or ctrl-c

    Returns:
        - voice command string of in vocabulary words recognized
        - "KeyboardInterrupt"
        - "TimeOut" if past timeout parameter [default 60 seconds]
          since last command recognized
"""

def getVoiceCommand(model=model, rate=vosk_rate, commands=cmd_keywords, printResults=False, timeout=60):
	global dt_turn_start
	try:
		rec = KaldiRecognizer(model, vosk_rate, commands)


		p = pyaudio.PyAudio()
		# Carl needs to use input_device_index 1
		stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000, input_device_index = 1)
		stream.start_stream()

		jres = None

		print("\nListening ...")
		while True:
			try:
				data = stream.read(4000,exception_on_overflow=False)
				if len(data) == 0:
					break
				if rec.AcceptWaveform(data):
					res = rec.Result()
					# print(res)
					if printResults:
						printResult(res)
					text = getText(res)
					if text != "": reset_turn_start()
					# print_w_date_time("Keyword Phrase Heard: " + text)
					break
				else:
					# print(rec.PartialResult())
					if dt_turn_start is None:
						reset_turn_start()

					elif (seconds_since_turn_start() > timeout):
						text = "TimeOut"
						break
					pass
			except KeyboardInterrupt:
				res =rec.FinalResult()
				# print("getVoiceCommand: KeyboardInterrupt - FinalResult:",res)
				text = "KeyboardInterrupt"
				break
		stream.stop_stream()
		stream.close()
	except KeyboardInterrupt:
		# print("getVoiceCommand outer try KeyboardInterrupt")
		text = "KeyboardInterrupt"

	# print("getVoiceCommand: Returning",text)
	return text


# getVoiceNL()
"""
    get a phrase using language model or ctrl-c

    Returns:
        - phrase string of words recognized
        - "KeyboardInterrupt"
        - "TimeOut" if past timeout parameter [default 60 seconds]
          since last phrase recognized
"""

def getVoiceNL(model=model, rate=vosk_rate, printResults=False, timeout=60):
	global dt_turn_start
	try:
		rec = KaldiRecognizer(model, vosk_rate)


		p = pyaudio.PyAudio()
		# Carl needs to use input_device_index 1
		stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000, input_device_index = 1)
		stream.start_stream()

		jres = None

		print("\nListening ...")
		while True:
			try:
				data = stream.read(4000,exception_on_overflow=False)
				if len(data) == 0:
					break
				if rec.AcceptWaveform(data):
					res = rec.Result()
					# print(res)
					if printResults:
						printResult(res)
					text = getText(res)
					if text != "": reset_turn_start()
					# print_w_date_time("Keyword Phrase Heard: " + text)
					break
				else:
					# print(rec.PartialResult())
					if dt_turn_start is None:
						reset_turn_start()

					elif (seconds_since_turn_start() > timeout):
						text = "TimeOut"
						break
					pass
			except KeyboardInterrupt:
				res =rec.FinalResult()
				# print("getVoiceNL: KeyboardInterrupt - FinalResult:",res)
				text = "KeyboardInterrupt"
				break
		stream.stop_stream()
		stream.close()
	except KeyboardInterrupt:
		# print("getVoiceNL outer try KeyboardInterrupt")
		text = "KeyboardInterrupt"

	# print("getVoiceNL: Returning",text)
	return text




def isExitRequest(command=""):
	try:
		if ("exit" in command) or ("KeyboardInterrupt" in command):
			return_val = True
		else:
			return_val = False
	except KeyboardInterrupt:
		return_val = True
	return return_val


def print_speak(response,override=override_quiet_time):
	print("\n*** ",end="")
	print(response)
	if verbose:
		speak.say(response,anytime=override)


def doVoiceAction(action_request, egpg=None, cmd_mode=True):
	global sleeping,verbose,override_quiet_time

	try:
		if action_request == "TimeOut":
			print("\n*** doVoiceAction() ignoring TimeOut")
			return

		if action_request == "":
			print("\n*** doVoiceAction() ignoring empty action request")
			return
		else:
			print("\n*** doVoiceAction() processing: [ " + action_request + " ]")


		if sleeping:
			if "wake up" in action_request:
				sleeping = False
				if speak.quietTime():
					override_quiet_time = True
				response = "Terminating Sleep Mode"
				print_speak(response)
				response = "I'm awake now"
				print_speak(response)
				return
			else:
				print("\n*** SLEEPING")
				print("\n*** Ignoring [ " + action_request + " ]")
				return


		# Voice Action Only - No egpg required
		if "go to sleep" in action_request:
			print_speak("Entering Sleep Mode - Listening only for \'Wake Up\' " )
			sleeping = True

		elif "wake up" in action_request:
			print_speak("Already Awake!")

		elif ("up time" in action_request) or \
			("since boot" in action_request):
			value = status.getUptime()  # *** Up 11 day  11 hours 25:12 
							# 19:23:15 up  5:12,  4 users,  load average: 0.28, 0.29, 0.27
			if "day" in value:
				days = value[value.index("up")+2 : value.index("day")-1]
				rest_of_value = value[value.index(",")+1 :]
			else:
				days = 0
				rest_of_value = value[value.index("up")+2 :]
			hours = rest_of_value[:rest_of_value.index(":")]
			minutes = str(int(rest_of_value[rest_of_value.index(":")+1:rest_of_value.index(",")]))

			response = " Up {} days {} hours {} minutes since boot".format(days,hours,minutes)
			print_speak(response)

		elif ("charging state" in action_request):
			charging_state = status.getChargingState()
			response = "Charging State: {}".format(charging_state)
			print_speak(response)

		elif "be quiet" in action_request:
			if verbose:
				response = "Entering Quiet Mode"
				print_speak(response)
				verbose = False
				override_quiet_time = False
			else:
				print("\n*** Already in Quiet Mode")

		elif "you can talk" in action_request:
			if verbose:
				print_speak("I was not in quiet mode")
				if speak.quietTime():
					override_quiet_time = True
					print_speak("but I'll override quiet time")
			else:
				verbose = True
				print_speak("Terminating Quiet Mode")
				if speak.quietTime():
					override_quiet_time = True
					print_speak("Ingoring Quiet Time Limit")
				print_speak("Let's talk shall we?")

		elif ("weather" in action_request) and ("long quiet" in action_request):
			print_speak("oh. I remember you")


		elif ("list commands" in action_request):
			print("Voice Commands")
			for x in ast.literal_eval(cmd_keywords):
				if x != "[unk]": print_speak(x)
			print_speak("The following are only available in natural language mode")
			for x in nlu_actions:
				print_speak(x)

		elif ("playtime" in action_request):
			print_speak("Playtime Status")
			if status.getDockingState() == "Not Docked":
				lastDismountTime = carlData.getCarlData('lastDismountTime')
				dtLastDismountTime = dt.datetime.strptime(lastDismountTime, '%Y-%m-%d %H:%M:%S')
				lastDismountForTTS = dtLastDismountTime.strftime( '%A at %-I %M')
				if lastDismountForTTS[-2] == "0":
					lastDismountForTTS = lastDismountForTTS[:-3] + " oh " + lastDismountForTTS[-1]
				response = "Playtime began {}".format(lastDismountForTTS)
				print_speak(response)
				secondsSinceDismount = (dt.datetime.now() - dtLastDismountTime).total_seconds()
				hoursSinceDismount = secondsSinceDismount/3600
				response = "Current playtime {:.1f} hours so far".format(hoursSinceDismount)
				print_speak(response)
				vBatt = egpg.volt()
				response = "Battery: {:.1f} volts".format(vBatt)
				print_speak(response)
			priorPlaytimeDuration = carlData.getCarlData('lastPlaytimeDuration')
			response = "Prior Playtime was {} hours".format(priorPlaytimeDuration)
			print_speak(response)

		elif ("recharge" in action_request):
			print_speak("Recharge Status")
			if status.getDockingState() == "Docked":
				lastDockingTime = carlData.getCarlData('lastDockingTime')
				dtLastDockingTime = dt.datetime.strptime(lastDockingTime, '%Y-%m-%d %H:%M:%S')
				lastDockingForTTS = dtLastDockingTime.strftime( '%A at %-I %M')
				if lastDockingForTTS[-2] == "0":
					lastDockingForTTS = lastDockingForTTS[:-3] + " oh " + lastDockingForTTS[-1]
				response = "Recharge began {}".format(lastDockingForTTS)
				print_speak(response)
				secondsSinceDocking = (dt.datetime.now() - dtLastDockingTime).total_seconds()
				hoursSinceDocking = secondsSinceDocking/3600
				response = "Recharging {:.1f} hours so far".format(hoursSinceDocking)
				print_speak(response)
				vBatt = egpg.volt()
				response = "Battery: {:.1f} volts".format(vBatt)
				print_speak(response)
			priorRechargeDuration = carlData.getCarlData('lastRechargeDuration')
			response = "Prior Recharge was {} hours".format(priorRechargeDuration)
			print_speak(response)


		# elif ("off dock" in action_request):  # "time off dock"

		# elif ("recharging" in action_request):  # "time recharging"

		# stop processing if request is unknown
		elif (action_request == "[unk]"):
			print("Ignoring unknown command")
			pass

		# ========= NLU ACTIONS, with no robot needed
		elif (("search" in action_request) or \
			("look up" in action_request)):
			if "look up" in action_request:
				query = action_request.partition("look up")[2]
			else:
				query = action_request.partition("search")[2]
			if query:
				print_speak('Searching Wikipedia for {}'.format(query))
				try:
					results = wikipedia.summary(query, sentences=1)
					print_speak("According to Wikipedia")
					print_speak(results)
				except wikipedia.exceptions.DisambiguationError as e:
					for i in range(4):
						print_speak(e.options[i])
				except KeyboardInterrupt:
					pass    # quit reading results
				except:
					print_speak("unknown Wikipedia exception")
			else:
				print_speak("Did not catch what to search for")

		# ========= ROBOT ACTIONS - Need egpg

		elif egpg is None:
			print_speak(" {} requires GoPiGo3, none passed".format(action_request))

		elif "battery voltage" in action_request:
			vBatt = egpg.volt()
			response = "Battery: {:.1f} volts".format(vBatt)
			print_speak(response)

		elif "charging state" in action_request:
			charging_state = status.getChargingState()
			response = "Charging State: {}".format(charging_state)
			print_speak(response)

		elif "turn around" in action_request:
			print_speak("turning 180")
			egpg.turn_degrees(180.0)

		elif "nod yes" in action_request:
			print_speak("nodding yes")
			egpg.tp.nod_yes()

		elif "nod no" in action_request:
			print_speak("nodding no")
			egpg.tp.nod_no()

		elif ("nod" in action_request) and ("i dont know" in action_request):
			print_speak("nodding I Don't Know")
			egpg.tp.nod_IDK()

		# drive centimeters forward backward negative  2 5 10 100
		elif (  ("drive" in action_request) or \
			("backup" in action_request) or \
			("forward" in action_request) ) \
			and ("centimeters" in action_request):
			if "one hundred" in action_request:  # must be before one
				distance = 100
			elif "two" in action_request:
				distance = 2
			elif "five" in action_request:
				distance = 5
			elif "ten" in action_request:
				distance = 10
			else:
				distance = 1
			if ("backward" in action_request) or \
				("negative" in action_request) or \
				("backup" in action_request):
				distance = distance * -1
			print_speak("Preparing to execute drive " + str(distance) + " centimeters")
			egpg.drive_cm(distance)

		# Must be after drive centimeters!
		# drive inches forward backward backup negative two six twelve twenty four thirty six
		elif (  ("drive" in action_request) or \
			("backup" in action_request) or \
			("forward" in action_request) ):
			if "thirty six" in action_request:  # must be before single word distances
				distance = 36
			elif "twenty four" in action_request:
				distance = 24
			elif "twelve" in action_request:
				distance = 12
			elif "six" in action_request:
				distance = 6
			elif "two" in action_request:
				distance = two
			else:
				distance = 1
			if ("backward" in action_request) or \
				("negative" in action_request) or \
				("backup" in action_request):
				distance = distance * -1
			print_speak("Preparing to execute drive " + str(distance) + " inches")
			egpg.drive_inches(distance)


		# "turn degrees counter clockwise negative 15 30 45 90", \
		elif ("turn" in action_request) and ("degrees" in action_request):
			if "fifteen" in action_request:
				angle = 15
			elif "thirty" in action_request:
				angle = 30
			elif "forty five" in action_request:
				angle = 45
			elif "ninety" in action_request:
				angle = 90
			else:
				angle = 5
			if ("counter" in action_request) or ("negative" in action_request):
				angle = angle * -1
			print_speak("Preparing to execute turn " + str(angle) + " degrees")
			egpg.turn_degrees(angle)


		# distance sensor reading in centimeters inches
		elif ("distance" in action_request):
			if "centimeters" in action_request:
				distance = (myDistSensor.adjustReadingInMMForError(egpg.ds.read_mm())) / 10.0
				units = " centimeters "
			else:
				distance = (myDistSensor.adjustReadingInMMForError(egpg.ds.read_mm())) / 25.4
				units = " inches "
			print_speak("distance sensor reading {:.1f} {}".format(distance,units))



		# pan left right fifteen thirty forty five sixty ninety to center degrees
		elif ("pan" in action_request):
			if "forty five" in action_request:  # must be before single word angles
				angle = 45
			elif "thirty" in action_request:
				angle = 30
			elif "ninety" in action_request:
				angle = 90
			elif "sixty" in action_request:
				angle = 60
			elif "fifteen" in action_request:
				angle = 15
			# pan to center, center pan
			elif "center" in action_request:  # must be last to allow for 15 deg left of center
				angle = 0
			else:
				angle = 0
			if ("left" in action_request):
				angle = angle * -1
			# 0 = Left 90= Center 180=Right
			pan_angle = 90 + angle
			if pan_angle == 90:
				print_speak("Panning to center")
			else:
				print_speak("Panning " + str(angle) + " degrees from center")
			egpg.tp.pan(pan_angle)
			time.sleep(1)
			egpg.tp.off()

		# tilt up down fifteen thirty forty five sixty to level degrees
		elif ("tilt" in action_request):
			if "forty five" in action_request:  # must be before single word angles
				angle = 45
			elif "thirty" in action_request:
				angle = 30
			elif "sixty" in action_request:
				angle = 60
			elif "fifteen" in action_request:
				angle = 15
			# tilt to level
			elif "level" in action_request:
				angle = 0
			else:
				angle = 0
			if ("down" in action_request):
				angle = angle * -1
			# -90=Down  0=Level 90=Up
			if angle == 0:
				print_speak("Tilt to level")
			else:
				print_speak("Tilt to " + str(angle) + " degrees")
			egpg.tp.tilt(angle)
			time.sleep(1)
			egpg.tp.off()

		# NO ACTION HANDLER - if natural language say I Heard: xxx
		else:
			print("\n*** doVoiceAction: [ " + action_request + " ] has no action handler")
			if cmd_mode == False:
				print_speak("I heard")
				print_speak(action_request)

		# Return if made it to here
		return

	except Exception:
		traceback.print_stack()
		traceback.print_exc()
