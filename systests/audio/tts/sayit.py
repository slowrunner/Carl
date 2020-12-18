#!/usr/bin/env python3

# file: sayit.py

# Test Python espeakng bindings

from easygopigo3 import EasyGoPiGo3
try:
    import espeakng
except:
    print("need to install espeakng python bindings")
    print("pip3 install espeakng")
    exit(1)

egpg = EasyGoPiGo3()
tts=espeakng.Speaker()



tts.say("Hello")

