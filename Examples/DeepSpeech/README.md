# Setup DeepSpeech For GoPiGo3 Robot Carl

# Installation
```
Not Yet:  pip3 install deepspeech-tflite   (no linux_armv7 yet)

pip3 install deepspeech
```

# Latest Release Models, Language Model binary, Scorer, Audio Samples

- Determine Latest:
```
https://github.com/mozilla/DeepSpeech/releases/latest
```
1/2/2021 latest version is 0.9.3

Models:
https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm
https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.tflite

Scorer:
https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer

Audio Files:
https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/audio-0.9.3.tar.gz


# Script to get Models, Language Model Binary, Scorer, Test Audio

./get_deepspeech_big_files.sh


# Manual Method


- Download the models, language model binary and test audio samples.

curl -LO --output <filename> <url>

```
mkdir models
cd models

curl -L0 --output deepspeech-0.9.3-models.pbmm https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm

curl -L0 --output deepspeech-0.9.3-models.tflite https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.tflite

curl -L0 --output deepspeech-0.9.3-models.scorer https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer

```

- Download audio
```
cd ~/Carl/Examples/DeepSpeech

curl -L0 --output audio-0.9.3.tar.gz https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/audio-0.9.3.tar.gz

tar -xvf audio-<version>.tar.gz

tar -xvf audio-0.9.3.tar.gz 

rm *.gz
```





# Example - Transcription 

./transcribe_file_test.sh

or

```
pi@Carl:~/Carl/Examples/DeepSpeech $ deepspeech --model models/deepspeech-0.9.3-models.tflite --scorer models/deepspeech-0.9.3-models.scorer --audio audio/2830-3980-0043.wav 
Loading model from file deepspeech-0.9.3-models.tflite
TensorFlow: v2.3.0-6-g23ad988
DeepSpeech: v0.9.3-0-gf2e9c85
Loaded model in 0.046s.
Loading scorer from files deepspeech-0.9.3-models.scorer
Loaded scorer in 0.0224s.
Running inference.
experience proves this
Inference took 11.949s for 1.975s audio file.
```

# Example - Microphone With Voice Activity Detection (VAD) Streaming

- Bring down example:

```
curl -L0 --output README.rst https://github.com/mozilla/DeepSpeech-examples/blob/r0.8/mic_vad_streaming/README.rst

curl -L0 --output mic_vad_streaming.py https://raw.githubusercontent.com/mozilla/DeepSpeech-examples/r0.8/mic_vad_streaming/mic_vad_streaming.py

curl -L0 --output requirements.txt https://github.com/mozilla/DeepSpeech-examples/blob/r0.8/mic_vad_streaming/requirements.txt
```

- install missing requirements

- create do_it.sh

```
#!/bin/bash

./mic_vad_streaming.py \
  --model $HOME/Carl/Examples/DeepSpeech/models/deepspeech-0.9.3-models.tflite \
  --scorer $HOME/Carl/Examples/DeepSpeech/models/deepspeech-0.9.3-models.scorer \
  ==file  $HOME/Carl/Examples/DeepSpeech/audio/2830-3980-0043.wav
```


