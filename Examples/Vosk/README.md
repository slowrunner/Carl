# Vosk Speech Recognition Engine For GoPiGo3 Robot Carl

As of January 2020, the CMU pocketsphinx engine does not install on the Raspberry PiOS without modifications,  
so this investigation of new open-source engine for research, called [Vosk, available from Alpha Cephai]


# Installation

```
$ pip3 install vosk
.
Successfully installed vosk-0.3.15
```


# Get a language model for RPi

See https://alphacephei.com/vosk/models for all models available

```
$ mkdir models
$ ./get_lm_for_RPi.sh
$ cd models
$ unzip vosk*.zip
```

# Get a Speaker Identification Model 

See https://alphacephei.com/vosk/models

```
$ ./get_speaker_id_model.sh
$ cd models
$ unzip vosk-model-spk*.zip
```

# Get sample programs for Python

See https://github.com/alphacep/vosk-api

```
$ mkdir vosk-api
$ ./get_python_examples.sh
```

# Try out reco from file

- Create symbolic link to model

```
$ cd ~/Carl/Examples/Vosk/vosk-api/python/example
$ ln -s ../../../models/vosk-model-small-en-us-0.15/ model
```

- Invoke test_simple
```
./test_simple.py test.wav
```
