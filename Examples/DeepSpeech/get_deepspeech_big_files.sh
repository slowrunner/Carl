#!/bin/bash

Echo "Download the models, language model binary and test audio samples."

curl -L0 --output deepspeech-0.9.3-models.pbmm https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm

curl -L0 --output deepspeech-0.9.3-models.tflite https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.tflite

curl -L0 --output deepspeech-0.9.3-models.scorer https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer

curl -L0 --output audio-0.9.3.tar.gz https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/audio-0.9.3.tar.gz

tar -xvf audio-0.9.3.tar.gz

echo "Done"

