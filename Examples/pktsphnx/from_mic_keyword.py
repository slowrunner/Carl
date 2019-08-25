#!/usr/bin/python3

import sys
sys.path.append('/home/pi/Carl/plib')
import speak
from os import environ, path
import pyaudio
import time
import random

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *


MODELDIR = "/usr/local/lib/python3.5/dist-packages/pocketsphinx/model"
DATADIR = "/usr/local/lib/python3.5/dist-packages/pocketsphinx/data"

# Create a decoder with en-us model
config = Decoder.default_config()

config.set_string('-hmm', path.join(MODELDIR, 'en-us'))
# config.set_string('-lm', path.join(MODELDIR, 'en-us.lm.bin'))
config.set_string('-dict', path.join(MODELDIR, 'cmudict-en-us.dict'))
config.set_string('-logfn', '/dev/null')
config.set_string('-keyphrase', 'carl')
config.set_float('-kws_threshold', 1e-10)  # 12-10 for 1 syllable, 1e-20 for 2 syllable 1e-30 for 3 recommended

WAKEUP_RESPONSES = ["yes", "I m listening", "right here", "go ahead", "you have my undivided attention, sort of.","What can I do for you?", "listening", "I m all ears", "thats me", "your wish is my command"]

decoder = Decoder(config)

p = pyaudio.PyAudio()
samprate = 16000

stream = p.open(format=pyaudio.paInt16, channels=1, rate=int(samprate), input=True, frames_per_buffer=1024)
stream.start_stream() 

in_speech_bf = False

try:
  decoder.start_utt()
  print ('\n\n**** LISTENING ****\n\n')
  while True:
      buf = stream.read(1024, exception_on_overflow = False)
      if buf:
          decoder.process_raw(buf, False, False)
          if decoder.hyp() != None:
              response = random.choice(WAKEUP_RESPONSES) 
              speak.say( response )
              print ([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in decoder.seg()])
              print ("Detected keyphrase, restarting search")
              decoder.end_utt()
              time.sleep(3)
              decoder.start_utt()
              print ('\n\n**** LISTENING ****\n\n')
      else:
         break
except KeyboardInterrupt:
  decoder.end_utt()
  print("\nGoodbye")

