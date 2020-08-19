#!/bin/bash

echo "Mic Comparison Tool"
# speaker-test -t wav -c 2 -l 1
sleep 5
echo "Begin Playing Test Phrase"
sleep 1
arecord -d 30 -c 1 -f S16_LE -r 48000 compare_48k16bitLE.wav
sleep 5
aplay compare_48k16bitLE.wav

