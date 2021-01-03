#/bin/bash

deepspeech \
   --model models/deepspeech-0.9.3-models.tflite \
   --scorer models/deepspeech-0.9.3-models.scorer \
   --audio audio/2830-3980-0043.wav
