# Vosk Speech Recognition Engine For GoPiGo3 Robot Carl

As of January 2020, the CMU pocketsphinx engine does not install on the Raspberry PiOS without modifications,  
so this investigation of new open-source engine for research, called [Vosk, available from Alpha Cephai]

# FIRST TEST MICROPHONE CONFIGURATION  
- run ./find_mic_device_number.py  
  If it doesn't show device 25 is mic - possibly need to configure /home/pi/.asoundrc  (cp ~/Carl/configs/home.pi.dot.asoundrc.PiOS )  
- $ arecord -d 7 -c 1 -f S16 -r 16000 test.wav  
  Recording WAVE 'test.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono  
- $ aplay test.wav  
  Playing WAVE 'test.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono  




# Installation

```
$ pip3 install vosk
.
Successfully installed vosk-0.3.15
```
Alpha Cephai says "Vosk requires libgfortran on some Linux builds which might be missing, you might need to install libgfortran"  
(yes, indeed else get ImportError: libgfortran.so.3: cannot open shared object file: No such file or directory)

```
$ sudo apt-get install libgfortran3
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

- Create symbolic link to model in the example folder

```
$ cd ~/Carl/Examples/Vosk/vosk-api/python/example
$ ln -s ../../../models/vosk-model-small-en-us-0.15/ model
```

- Invoke test_simple.py reco from 8 second test.wav file

```
$ time ./test_simple.py test.wav
.
"text" : "one zero zero zero one"  ( source: "1 0 0 0 1" )
.
 "text" : "nah no to i know"       ( source: "9 oh 2 1 oh" )
.
  "text" : "zero one eight zero three"   (source: "0 1 8 0 3" )

real	0m15.933s
user	0m15.563s
sys	0m0.720s
```


# vcommand.py
# NOTE: wikipedia must be installed with (sudo pip3 install) to allow voicecmdr to be started as root at boot
- doVoiceCommand()  word list mode
- doVoiceNL()       language model mode
- doVoiceAction()   interpret and handle phrases

# Maintenance of vcommand.py
1) ./diff_w_plib.sh   to make sure local matches plib version
2) make changes to local
3) test the local
4) ./release.sh   copies local to plib


