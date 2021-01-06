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
```
./record_16k_16bit.sh my_test.sh
```



# test_simple.py
- Performs recognition from 16k 16bit file  
- Record samples with record_16k_16bit.sh <filename.wav>, press CTRL-C to end recording  
- From https://github.com/alphacep/vosk-api/blob/master/python/example/test_simple.py
Usage: 
```
./test_simple.py my_test.wav
```

# carl_test_microphone.py
- Uses audio_device 1  
- Has overflow exceptions turned off (prevented test_microphone.py example from working)  

Usage: 
```
./carl_test_microphone.py
```

# carl_test_file.py  and carl_wake_up.wav
- Recognition from file using entire given language model
- Based on https://github.com/alphacep/vosk-api/blob/master/python/example/test_simple.py
- carl_wake_up.wav 
  - recorded with Carl on floor
  - Spoken toward wall not toward bot
  - Result on RPi3B: 10.5 seconds to decode 2.2 second file 4.8x real-time

Execution:
```
$ time ./carl_test_file.py carl_wake_up.wav 
Starting File Decode
result words: 3
 0.28 carl
 1.00 wake
 1.00 up
Done


real	0m10.482s
user	0m10.170s
sys	0m0.495s
```

# carl_numbers_file.py and carl_numbers_01234567890.wav
- Demonstrates recognition using word lists
- Recognition from audio file containing numbers 
- and optionally beginning with "carl numbers"
- Using the word list '["oh one two three four five six seven eight nine zero", "carl numbers", "[unk]"]'
- Based on https://github.com/alphacep/vosk-api/blob/master/python/example/test_words.py  
- carl_numbers_0123456789.wav 
  - Recorded on Carl "far-field" using record_16k_16bit.sh
  - On Carl's RPi3B 12 second file is decoded in 8.5 seconds or 0.7x real-time
- test_10001_9oh21oh_01803.wav
  - test.wav from https://github.com/alphacep/vosk-api/tree/master/python/example
  - high quality recording
  - On Carl's RPi3B 8 second file is decoded in 7 seconds or 0.89x real-time

Usage:
```
./carl_numbers_file.py <file.wav>
./carl_numbers_file.py carl_numbers_01234567890.wav
./carl_numbers_file.py test_10001_9oh21oh_01803.wav
```  

Execution:
```
time ./carl_numbers_file.py carl_numbers_0123456789oh.wav 
result words: 13
 1.00 carl
 1.00 numbers
 1.00 zero
 1.00 one
 1.00 two
 1.00 three
 1.00 four
 1.00 five
 1.00 six
 1.00 seven
 1.00 eight
 1.00 nine
 1.00 oh
Done

real	0m8.538s
user	0m8.437s
sys	0m0.429s
```


