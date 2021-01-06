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


# carl_wake_up.wav
- recorded with Carl on floor
- Spoken toward wall not toward bot

Execution:
```
$ ./test_simple.py carl_wake_up.wav 
LOG (VoskAPI:ReadDataFiles():vosk/model.cc:192) Decoding params beam=10 max-active=3000 lattice-beam=2
LOG (VoskAPI:ReadDataFiles():vosk/model.cc:195) Silence phones 1:2:3:4:5:6:7:8:9:10
LOG (VoskAPI:RemoveOrphanNodes():nnet-nnet.cc:948) Removed 0 orphan nodes.
LOG (VoskAPI:RemoveOrphanComponents():nnet-nnet.cc:847) Removing 0 orphan components.
LOG (VoskAPI:CompileLooped():nnet-compile-looped.cc:345) Spent 0.227804 seconds in looped compilation.
LOG (VoskAPI:ReadDataFiles():vosk/model.cc:219) Loading i-vector extractor from model/ivector/final.ie
LOG (VoskAPI:ComputeDerivedVars():ivector-extractor.cc:183) Computing derived variables for iVector extractor
LOG (VoskAPI:ComputeDerivedVars():ivector-extractor.cc:204) Done.
LOG (VoskAPI:ReadDataFiles():vosk/model.cc:242) Loading HCL and G from model/graph/HCLr.fst model/graph/Gr.fst
LOG (VoskAPI:ReadDataFiles():vosk/model.cc:264) Loading winfo model/graph/phones/word_boundary.int
{
  "partial" : ""
}
{
  "partial" : ""
}
{
  "partial" : ""
}
{
  "partial" : ""
}
{
  "partial" : ""
}
{
  "partial" : ""
}
{
  "partial" : "carl wake"
}
{
  "partial" : "carl wake up"
}
{
  "partial" : "carl wake up"
}
{
  "partial" : "carl wake up"
}
{
  "partial" : "carl wake up"
}
{
  "result" : [{
      "conf" : 0.278673,
      "end" : 1.110000,
      "start" : 0.690000,
      "word" : "carl"
    }, {
      "conf" : 1.000000,
      "end" : 1.410000,
      "start" : 1.110000,
      "word" : "wake"
    }, {
      "conf" : 1.000000,
      "end" : 1.650000,
      "start" : 1.410000,
      "word" : "up"
    }],
  "text" : "carl wake up"
}
```
