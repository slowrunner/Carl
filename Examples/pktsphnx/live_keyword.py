#!/usr/bin/env python3

import os
from pocketsphinx import LiveSpeech, get_model_path
import pyaudio

p = pyaudio.PyAudio()
print ("\n\n****\nget_default_input_device_info:",p.get_default_input_device_info())

for i in range(p.get_device_count()):
    print("\n\nDevice {}:".format(i), p.get_device_info_by_index(i))

print("\n\n*** get_model_path():",get_model_path())
# exit(0)

speech = LiveSpeech(audio_device='2',verbose=True,sampling_rate=16000,lm=False,keyphrase='forward',kws_threshold='le-20')

for phrase in speech:
    print(phrase.segments(detailed=True))


