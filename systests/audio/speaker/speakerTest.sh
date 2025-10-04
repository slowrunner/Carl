#!/bin/bash

speaker-test -t wav -c 2 -l 1
sleep 5
aplay /usr/share/scratch/Media/Sounds/Animal/Duck.wav
espeak-ng "If you are hearing this, audio output is correctly set up"
