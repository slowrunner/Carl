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


# === Record Hotword Samples
- Make sample directory for <speaker>/<mic>
```
mkdir samples
mkdir samples/alan
mkdir samples/alan/mic_kinobo_akira
cd samples/alan/mic_kinobo_akira
```  

- Record multiple "carl" "hey carl" "carl listen" samples
  (if restarting, enter starting sample number instead of 1)
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
