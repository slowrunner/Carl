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
  (cost of 0.4 hours playtime or about 20-25mA battery load)
- Far-field recognition of normal voice and whisper (in quiet room)
- Hotword recognized over background speech  
  (spoken at same volume as background TV news) 
- Occasional false recognition from room conversations (Sensitivity 0.6)
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

USAGE:  ./r.sh "\<spkrN-micN-key_word_phrase\>" \<starting_sample_number\>  

EXECUTION:  
``` 
$ ~/Carl/Examples/nyumaya/r.sh "carl" 1     
Sample Record Tool
Press Return - Say: carl
Recording WAVE 'carl-01.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono
Sample carl_1.wav written
Playing WAVE 'carl-01.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono

Press Return - Say: carl
Recording WAVE 'carl-02.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono
Sample carl_2.wav written
Playing WAVE 'carl-02.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono

Press Return - Say: carl
Recording WAVE 'carl-03.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono
Sample carl_3.wav written
Playing WAVE 'carl-03.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono

Press Return - Say: carl^C
```


# ==== Fix Carl's Version ====
- Because models and engine versions must match, Carl must fix his versions
```
cp -r nyumaya_audio_recognition-master ~/Carl/nyumaya_engine_carl
```
- Test local fixed version with local_simple_hotword.py
  ( modified examples/python/simple_hotword.py to use local, fixed version )
```
./local_simple_hotword.py
Say: "Marvin"
...
Say: "Marvin"
...
Press CTRL-C
```

# ==== Setup the local Nyumaya Hotword Engine for Carl programs
```
cp hotword.py ~/Carl/plib
```



# ==== EXAMPLE: carl_hotword.py
- Demonstrates how Carl's programs should be structured:
 
```
#!/usr/bin/env python3

# FILE: carl_hotword.py

# Demonstrates using the Nyumaya Hotword engine
# via ~/Carl/plib/hotword.py


import sys
sys.path.append('/home/pi/Carl/plib')
import hotword
import time

def main():

	while True:
		detected = hotword.detectKeywords()
		if detected == "Exit":
			break
		# Hotword was detected, Do something

		# Since not doing anything in this demo program:
		#   Wait at least 0.1s for AudiostreamSource thread to die off
		#   before calling detectKeywords() again
		time.sleep(0.1)
if __name__ == '__main__': main()
```


# ---- EXAMPLE: carl_hotword_eyes.py

- Demonstrates setting Carl's eyes to display status  
  - light blue: waiting for keyword "Marvin"  
    (later "Carl", "Hey Carl", "Carl Listen" )  
  - bright blue: simulates waiting for voice command mode  
  - light green: simulates performing voice command  
  - light red:   simulates voice command rejected  



