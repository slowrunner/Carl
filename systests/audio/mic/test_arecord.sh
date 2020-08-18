#!/bin/bash

echo "Testing Speaker First"
speaker-test -t wav -c 2 -l 1
sleep 5
echo "Say 'This is seven seconds of 8k 8bit unsigned mono audio'"
sleep 1
arecord -d 7 -c 1 test8k8bitUnsignedMono.wav
sleep 10
echo "Say 'This is seven seconds of signed 16 bit little endian 48k mono audio'"
sleep 1
arecord -d 7 -c 1 -f S16_LE -r 48000 test48k16bitLittleEndianMono.wav
sleep 5
aplay test8k8bitUnsignedMono.wav
sleep 5
aplay test48k16bitLittleEndianMono.wav

