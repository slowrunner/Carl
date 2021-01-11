
# FILE: vcommand.py

"""
   getVoiceCommand()

   Provides Carl programs easy access to the Vosk-API voice recognition engine
   and the downloaded language model in ~/Carl/vosk-api/model
    - Sets pyaudio to use input_device_index=1
    - Sets Initialization Logging off
      (Audio system warnings cannot be surpressed)
    - Sets partial result off
    - Adds CTRL-C handler return "Exit"
    - Keeps track of time since last command, returns "TimeOut" if too long



   isExitRequest(command)

   Provide test if user requested "exit voice command mode" or pressed CTRL-c




   doVoiceCommand()

   Provides Carl programs a command interpreter





   Usage:
       import sys
        sys.path.append('/home/pi/Carl/plib')
        import vcommand
	while True:
	        # vcmd = vcommand.getVoiceCommand(printResult=True)  # to print confidence for each word
	        vcmd = vcommand.getVoiceCommand()
		if vcommand.isExitRequest(vcmd):
			break
		else:
			vcommand.doVoiceCommand(vcmd)


"""

from vosk import Model, KaldiRecognizer, SetLogLevel
import os
import datetime as dt
import json
import sys
sys.path.append("/home/pi/Carl/plib")
import speak

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
cmd_keywords = '["battery voltage", \
		"exit voice command mode", \
		"be quiet", \
		"you can talk now", \
		"go to sleep", \
		"wake up", \
		"whats the weather like long quiet", \
		"[unk]"]'

# path to the language model (from vosk-model-small-en-us-0.15)
model = Model(vosk_model_path)
vosk_rate = 16000

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


def isExitRequest(command=""):
	try:
		if (command == "exit voice command mode") or (command == "KeyboardInterrupt"):
			return_val = True
		else:
			return_val = False
	except KeyboardInterrupt:
		return_val = True
	return return_val

# Voice Command State variables

sleeping = False
verbose  = True

"""
    doVoiceCommand(command_string)

    processes voice commands
    - performs action if handler exists
    - ignores actions with no handlers
"""

def doVoiceCommand(command=""):
		global sleeping, verbose
		try:

			if command != "": 
				print_w_date_time("doVoiceCommand: " + command)

			if sleeping:
				if command == "wake up":
					print("\n*** Terminating Sleep Mode")
					sleeping = False
					if verbose:
						speak.say("I'm awake now")
				else:
					print("\n*** SLEEPING")
			elif command == "battery voltage":
				print("\n*** Command " + command + " not implemented yet")

			elif isExitRequest(command):
				print("\n*** Command: " + command + "has no action programmed")

			elif command == "be quiet":
				if verbose:
					print("\n*** Entering Quiet Mode")
					verbose = False
				else:
					print("\n*** Already in Quiet Mode")

			elif command == "you can talk now":
				if verbose:
					print("\n*** Not in Quiet Mode")
					speak.say("I was not in quiet mode")
				else:
					print("\n*** Terminating Quiet Mode")
					speak.say("Let's talk shall we?")
					verbose = True

			elif command == "go to sleep":
				print("\n*** Entering Sleep Mode - (Listening only for \"Wake Up\)" )
				sleeping = True

			elif command == "wake up":
				print("\n*** Was not sleeping." )

			elif command == "whats the weather like long quiet":
				print("\n*** oh. I remember you")
				if verbose:
					speak.say("oh. I remember you")

			elif command == "":
				pass
			else:
				print("\n*** Command: " + command + " has no action programmed")
				pass
		except KeyboardInterrupt:
			pass

