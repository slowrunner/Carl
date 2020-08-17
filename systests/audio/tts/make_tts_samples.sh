#!/bin/bash

flite -o sample_flite.wav "Hello.  This is a sample of f light text to speech."
pico2wave -w sample_pico.wav -l en-US "Hello.  This is a sample of pico to wave text to speech."
espeak -w sample_espeak.wav "Hello.  This is a sample of e speak text to speech"
espeak-ng -w sample_espeak-ng.wav "Hello.  This is a sample of e speak n g text to speech"
