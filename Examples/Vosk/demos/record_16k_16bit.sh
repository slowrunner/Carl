#!/bin/bash

# FILE: record_16k_16bit.sh

# Purpose: record samples for Vosk engine to transcribe

# USAGE:  ./record_16k_16bit.sh <filename>
echo "Press CTRL-C to stop recording"
arecord  -c 1 -f S16_LE -r 16000 $1

