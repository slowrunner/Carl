#!/usr/bin/env python3
'''
#
# Usage:  ./try_espeak-ng.py
#         Enter the Text: (enter line of text (with or without quotes - no printed char restrictions)

'''

import os

text = input("Enter the Text: ")
print(text)

#Replacing ' ' with '_' to identify words in the text entered
#text = text.replace(' ', '_')
text = text.replace("'","")
text = text.replace('"',' quote ')

#Calls the espeak TTS Engine to read aloud a Text
os.system("espeak-ng -w samples/espeak-ng.wav \""+text+"\"")
os.system("aplay samples/espeak-ng.wav 2>/dev/null")
