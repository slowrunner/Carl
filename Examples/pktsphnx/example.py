#!/usr/bin/env python
from os import environ, path

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

# MODELDIR = "pocketsphinx/model"
MODELDIR = "/usr/local/lib/python3.5/dist-packages/pocketsphinx/model"
# DATADIR = "pocketsphinx/test/data"
DATADIR = "/usr/local/lib/python3.5/dist-packages/pocketsphinx/data"

# Create a decoder with certain model
config = Decoder.default_config()
# config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-hmm', path.join(MODELDIR, 'en-us'))
# config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
config.set_string('-lm', path.join(MODELDIR, 'en-us.lm.bin'))
# config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
config.set_string('-dict', path.join(MODELDIR, 'cmudict-en-us.dict'))
decoder = Decoder(config)

print ('\n\n**** ')
print("This example reads the sample file goforward.raw (in DATADIR)\n")
print("and should reco the words 'go forward ten meters' ")
print ('**** \n\n')

# Decode streaming data.
decoder = Decoder(config)
decoder.start_utt()
stream = open(path.join(DATADIR, 'goforward.raw'), 'rb')
while True:
  buf = stream.read(1024)
  if buf:
    decoder.process_raw(buf, False, False)
  else:
    break
decoder.end_utt()
print ('\n\n**** ')
print ('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])
print ('**** \n\n')
