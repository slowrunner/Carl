#!/usr/bin/env python3

# FILE: carl_numbers_file.py

# Recognition from audio file that begins with "carl numbers" 
# using a word list containing '["oh one two three four five six seven eight nine zero", "["carl numbers"]", "[unk]"]'
# Based on https://github.com/alphacep/vosk-api/blob/master/python/example/test_words.py

# USAGE:  ./carl_numbers_file.py <carl_numbers_nnnn.wav>
#         ./carl_numbers_file.py carl_numbers_0123456789oh.wav



from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import json

# Comment out to see logging
SetLogLevel(-1)

if not os.path.exists("model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

word_list = '["oh one two three four five six seven eight nine zero", "carl numbers", "[unk]"]'

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

def printResult(res):
    jres = json.loads(res)
    jresult=jres["result"]
    # print(jresult)

    num_words = len(jresult)
    print("result words:",num_words)

    for i in range(num_words):
        print("{:>5.2f} {:<s}".format(jresult[i]["conf"],jresult[i]["word"]))

model = Model("model")

# You can also specify the possible word or phrase list as JSON list, the order doesn't have to be strict
rec = KaldiRecognizer(model, wf.getframerate(), word_list)

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

fres = rec.FinalResult()
# print(fres)
# print(rec.FinalResult())
printResult(fres)
print("Done")
