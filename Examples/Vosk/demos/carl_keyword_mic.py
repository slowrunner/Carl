#!/usr/bin/env python3

# FILE: carl_test_microphone.py

# Based on https://github.com/alphacep/vosk-api/blob/master/python/example/test_microphone.py
# Modified to tell pyaudio to use input_device_index=1
# Turned Initialization Logging off
# (Audio system warnings cannot be surpressed)
# Turned partial and "Final" results off
# Added pretty printing of result
# Added CTRL-C handler to quit cleanly

from vosk import Model, KaldiRecognizer, SetLogLevel
import os
from voskprint import printResult
import datetime as dt
import json
import sys
sys.path.append("/home/pi/Carl/plib")
import speak

if not os.path.exists("model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

import pyaudio

def print_w_date_time(alert,event_time=None):
    if event_time is None: event_time = dt.datetime.now()
    str_event_time = event_time.strftime("%Y-%m-%d %H:%M:%S")
    print("{} {}".format(str_event_time,alert))



SetLogLevel(-1)

keywords = '["wake up carl","[unk]"]'
model = Model("model")
rec = KaldiRecognizer(model, 16000, keywords)


p = pyaudio.PyAudio()
# Carl needs to use input_device_index 1
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000, input_device_index = 1)
stream.start_stream()

print("Listening ...")
while True:
    try:
        data = stream.read(4000,exception_on_overflow=False)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = rec.Result()
            # print(res)
            text = printResult(res)
            if text == "wake up carl":
                # speak.say("oh kay")
                print_w_date_time("Wake Phrase Heard")
            print("\nListening Again ...")
        else:
            # print(rec.PartialResult())
            pass
    except KeyboardInterrupt:
        # print(rec.FinalResult())
        break
print("\nExiting carl_keyword_mic.py")
