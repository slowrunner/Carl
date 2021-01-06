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
- I'm using mplayer <audio-file.wav> to get file duration  
  (sudo apt-get install mplayer)


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


# voskprint.py
- Pretty print for Vosk results
```
Result: 3 words
 0.28 carl
 1.00 wake
 1.00 up
Text: carl wake up
```
Usage:
```
from voskprint import printResult

printResult(rec.Result())
printResult(rec.FinalResult())
```


# test_simple.py
- Performs recognition from 16k 16bit file  
- Record samples with record_16k_16bit.sh <filename.wav>, press CTRL-C to end recording  
- From https://github.com/alphacep/vosk-api/blob/master/python/example/test_simple.py
Usage: 
```
./test_simple.py my_test.wav
```

# carl_test_file.py  and carl_wake_up.wav
- Recognition from file using entire given language model
- Based on https://github.com/alphacep/vosk-api/blob/master/python/example/test_simple.py
- carl_wake_up.wav 
  - recorded with Carl on floor
  - Spoken toward wall not toward bot
  - Result on RPi3B: 10.2 seconds to decode 2.2 second file 4.8x real-time

Execution:
```
$ time ./carl_test_file.py carl_wake_up.wav 
Starting File Decode
Result: 3 words
 0.28 carl
 1.00 wake
 1.00 up
Text: carl wake up
Done


real	0m10.230s
user	0m10.157s
sys	0m0.441s
```





# carl_test_microphone.py
- Uses audio_device 1  
- Has overflow exceptions turned off (prevented test_microphone.py example from working)  
- Based on https://github.com/alphacep/vosk-api/blob/master/python/example/test_microphone.py
- Turned Initialization Logging off  
  (Audio system warnings cannot be surpressed)
- Turned partial and "Final" results off
- Added pretty printing of result
- Added CTRL-C handler to quit cleanly
- First phrase recognition is often total garbage

Usage: 
```
./carl_test_microphone.py
```

Exection:
```
$ ./carl_test_microphone.py
.
(ALSA "failed in ...")
.
Listening ...
Result: 1 words
 0.77 oh
Text: oh

Listening Again ...
Result: 5 words
 0.73 how
 1.00 are
 1.00 you
 1.00 listening
 0.39 carl
Text: how are you listening carl

Listening Again ...
Result: 5 words
 1.00 what's
 1.00 the
 1.00 weather
 0.89 looked
 1.00 like
Text: what's the weather looked like

Listening Again ...
^C
Exiting carl_test_microphone.py
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
Result: 13 words
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
Text: carl numbers zero one two three four five six seven eight nine oh
Done

real	0m8.538s
user	0m8.437s
sys	0m0.429s
```


