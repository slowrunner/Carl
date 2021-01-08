# NYUMAYA HotWord Detection  


# === Get The Repository ===  
```
curl -L0 --output x.zip https://github.com/nyumaya/nyumaya_audio_recognition/archive/master.zip
unzip x.zip
```


# === Test =====  
```
cd nyumaya_audio_recognition/examples/python
python3 simple_hotword.py
```

# === Performance ===
- Processor Load: +0.1 15 minute average (10% of one core)
- Far-field recognition of normal voice and whisper (in quiet room)
- Hotword recognized over background speech  
  (spoken at same volume as background TV news) 
- Occasional false recognition from room conversations  
  * 1-4 per hour with TV news as background
  * 3-38 per hour with normal volume conversations as background
- Onboard TTS does not trigger false hotword detections

# === Record Hotword Samples  r.sh
- Make sample directory for \<speaker\>/\<mic\>
```
mkdir samples
mkdir samples/speaker1
```  

- Record multiple "carl" "hey carl" "carl listen" samples
- Use name format "\<phrase\>" or "\<speaker\>_\<mic\>-\<phrase\>"  
  e.g.  "carl_listen"  or  "s1-m1-carl_listen"  
- If restarting, enter starting sample number instead of 1)

USAGE:  ./r.sh "\<speaker_mic_phrase\>" \<starting_sample_number\>  

EXECUTION:  
``` 
$ ~/Carl/Examples/nyumaya/r.sh "carl" 1     
Sample Record Tool
Press Return - Say: carl
Recording WAVE 'carl_1.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono
Sample carl_1.wav written
Playing WAVE 'carl_1.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono

Press Return - Say: carl
Recording WAVE 'carl_2.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono
Sample carl_2.wav written
Playing WAVE 'carl_2.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono

Press Return - Say: carl
Recording WAVE 'carl_3.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono
Sample carl_3.wav written
Playing WAVE 'carl_3.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono

Press Return - Say: carl^C
```
