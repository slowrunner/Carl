#!/bin/bash

./mic_vad_streaming.py \
  --model $HOME/Carl/Examples/DeepSpeech/models/deepspeech-0.9.3-models.tflite \
  --scorer $HOME/Carl/Examples/DeepSpeech/models/deepspeech-0.9.3-models.scorer \
  ==file  $HOME/Carl/Examples/DeepSpeech/audio/2830-3980-0043.wav

