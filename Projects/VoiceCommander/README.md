# VOICE COMMANDER

Combines ...   
- the Nyumaya Hotword speech recognition engine,  
  * (uses machine learning technology),
  * (extremely low processing load to conserve Carl's battery)
  * Recognizes hotword "Marvin" (soon "Carl", "Hey Carl", or "Carl Listen" )   
with ...
- the Vosk-API general speech recognition engine  
  * (uses machine learning technology),
  * With small language model especially for Raspberry Pi applications
  * Can be further constrained by a list of words
  * Recognizes multi-word commands

# voicecmdr.py

USAGE:  ./voicecmdr.py  

- When SOFT BLUE LIGHT eyes are on, (HOTWORD MODE) say "Marvin"  

- When BRIGHT BLUE LIGHT eyes are on, (COMMAND MODE), say a command:  
  * "quit voice commander" - will exit program   
  * "battery voltage" - will speak battery voltage  
  * "go to sleep" - ignore all commands until "wake up" command heard  
  * "be quiet", or "quiet mode" - only print to console and use eye color responses. Do not use TTS
  * "cancel quiet mode" - resume using TTS in responses
  * (more to come)  

- When SOFT RED LIGHT eyes are on, (SLEEP MODE) say command:  
  * "wake up" - to return to command mode  

- When BRIGHT GREEN LIGHT eyes are on, command accepted

- When BRIGHT RED LIGHT eyes are on, command rejected


EXAMPLE:
``` 
./voicecmdr.py

TTS: "Voice Commander Ready"
(Soft Blue Light)
Say: "Marvin""
(Bright Blue Light)
Say: "go to sleep"
(Bright Green Light)

(Soft Blue Light)
Say: "Marvin"
(Soft Red Light)
Say: "battery voltage"
(Bright Red Light)


(Soft Blue Light)
Say: "Marvin"
(Soft Red Light)
Say: "wake up"
(Bright Green Light)

TTS: Voice Commander Awake
(Soft Blue Light)
```