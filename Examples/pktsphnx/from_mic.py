#!/usr/bin/python3

import sys
sys.path.append('/home/pi/Carl/plib')
import speak
from os import environ, path
import pyaudio
import time

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

# MODELDIR = "../../../model"

# config = Decoder.default_config()
# config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
# config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
# config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))

MODELDIR = "/usr/local/lib/python3.5/dist-packages/pocketsphinx/model"
DATADIR = "/usr/local/lib/python3.5/dist-packages/pocketsphinx/data"

# Create a decoder with en-us model
config = Decoder.default_config()

config.set_string('-hmm', path.join(MODELDIR, 'en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us.lm.bin'))
config.set_string('-dict', path.join(MODELDIR, 'cmudict-en-us.dict'))
config.set_string('-logfn', '/dev/null')

# config.set_string('-samprate', '44100')

decoder = Decoder(config)

p = pyaudio.PyAudio()
samprate = p.get_device_info_by_index(0)['defaultSampleRate']
print("default mic sample rate:",samprate)
samprate = 16000
frames = 4096  # 1024

stream = p.open(format=pyaudio.paInt16, channels=1, rate=int(samprate), input=True, frames_per_buffer=frames)
stream.start_stream() 

in_speech_bf = False


decoder.start_utt()
print ('\n\n**** LISTENING ****\n\n')
while True:
    buf = stream.read(frames, exception_on_overflow = False)
    if buf:
        decoder.process_raw(buf, False, False)
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                result = decoder.hyp().hypstr
                print ('Result:', result)
                # speak.say("I heard, "+result)
                time.sleep(0.5)
                decoder.start_utt()
                print ('\n\n**** LISTENING ****\n\n')
    else:
        break
decoder.end_utt()
