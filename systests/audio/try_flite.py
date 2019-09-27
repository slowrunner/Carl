#!/usr/bin/env python3
'''
#
# Usage:  ./try_flite.py
#          plays flite_ssml.txt

'''

import os


#Calls the flite TTS Engine to read aloud
os.system("flite -ssml flite_ssml.txt -o samples/flite_ssml.wav")
os.system("aplay samples/flite_ssml.wav 2>/dev/null")
