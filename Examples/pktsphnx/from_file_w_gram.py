#!/usr/bin/env python3
#
# FILE:  from_file_w_gram.py
#
# Args:  -f <path_to_16k_input_file>  required
#        -g <path_to_jsgf_gram>   optional [./grams/grammar.jsgf]
#
# Note: If passed file with sample rate other than 16K, prints msg and exits
#
from os import environ, path
import argparse
import wave

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

# ARGUMENT PARSER
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True, help="path to 16k input file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
ap.add_argument("-g", "--gram", default="./grams/grammar.jsgf", help="[./grams/grammar.jsgf] grammar")
args = vars(ap.parse_args())
# print("Started with args:",args)

inputFile = args['file']
inputGram = args['gram']
print("Input File: ", inputFile)
print("Input grammar:", inputGram)

f = wave.open(inputFile, "rb")
samprate = f.getframerate()
print("Sample Rate: ", samprate)

if samprate != 16000:
    print("Only works with 16k bps audio files")
    exit(0)


# MODELDIR = "pocketsphinx/model"
MODELDIR = "/usr/local/lib/python3.5/dist-packages/pocketsphinx/model"
# DATADIR = "pocketsphinx/test/data"
DATADIR = "/usr/local/lib/python3.5/dist-packages/pocketsphinx/data"

# GRAMDIR = "/home/pi/Carl/Examples/pktsphnx/grams"
# GRAMDIR = "./grams"


# Create a decoder with certain model
config = Decoder.default_config()
# config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-hmm', path.join(MODELDIR, 'en-us'))

# use language model
# config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
# config.set_string('-lm', path.join(MODELDIR, 'en-us.lm.bin'))

# use grammar
# config.set_string('-jsgf', path.join(GRAMDIR, 'grammar.jsgf'))
config.set_string('-jsgf', inputGram)


# config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
config.set_string('-dict', path.join(MODELDIR, 'cmudict-en-us.dict'))
# config.set_string('-samprate', str(samprate))


# Decode streaming data.
decoder = Decoder(config)
decoder.start_utt()
# stream = open(path.join(DATADIR, 'goforward.raw'), 'rb')
stream = open(inputFile, 'rb')
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
