# Carl's Vosk Demos

- vosk-api python examples modified to work  
  - on my Rasbperry Pi 3B based GoPiGo3 robot Carl
  - with Kinobo Mini Akira USB microphone  
    (Sensitivity -47dB +/-4dB)
- utilities
- symlink to small language model for RPi named "model"
```
ln -s ~/Carl/Examples/Vosk/models/vosk-model-small-en-us-0.15 model
```


# record_16k_16bit.sh
- Use to create input files for testing with Vosk
- Convenience for:
```
arecord -c 1 -r 16000 -f S16_LE <filename>
```
- Press CTRL-C to stop recording
Usage:
./record_16k_16bit.sh my_test.sh




# simple_test.py
- Performs recognition from 16k 16bit file
- Record samples with record_16k_16bit.sh <filename.wav>, press CTRL-C to end recording
Usage:
```
./simple_test.py my_test.wav
```

# carl_test_microphone.py
- Uses audio_device 1
- Has overflow exceptions turned off (prevented test_microphone.py example from working)
Usage: 
```
./carl_test_microphone.py
```
