#!/usr/bin/env python3

# FILE: carl_test_file.py

# Recognition from file using entire given language model
# Based on https://github.com/alphacep/vosk-api/blob/master/python/example/test_simple.py


from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
from voskprint import printResult

SetLogLevel(-1)  # set to 0 to see initialization log


if not os.path.exists("model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model("model")
rec = KaldiRecognizer(model, wf.getframerate())

print("Starting File Decode")
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        # print(rec.Result())
        printResult(rec.Result())
    else:
        # print(rec.PartialResult())
        pass

# print(rec.FinalResult())
printResult(rec.FinalResult())
print("Done\n")
