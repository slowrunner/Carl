#!/usr/bin/python3

import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
  dev = p.get_device_info_by_index(i)
  print((i, dev['name'], dev['maxInputChannels']))

# stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000, input_device_index = 2)
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000, input_device_index = 2)
p.terminate()
