#!/usr/bin/env python3

# FILE: carl_test_microphone.py

# Modified to tell pyaudio to use input_device_index=1

from vosk import Model, KaldiRecognizer
import os

if not os.path.exists("model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

import pyaudio

model = Model("model")
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
# Carl needs to use input_device_index 1
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000, input_device_index = 1)
stream.start_stream()

while True:
    data = stream.read(4000,exception_on_overflow=False)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())
    else:
        print(rec.PartialResult())

print(rec.FinalResult())
