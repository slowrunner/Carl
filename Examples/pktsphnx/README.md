README.md

UPDATE January 2021: PiOS replaced ALSA with PulseAudio as default sound system  
and the following installation instructions fail with:
```
deps/sphinxbase/src/libsphinxad/ad_alsa.c:76:10: fatal error: alsa/asoundlib.h: No such file or directory
     #include <alsa/asoundlib.h>
              ^~~~~~~~~~~~~~~~~~
```
I don't want to mess up my system unknowingly by trying to get the now obsolete pocketsphinx working.

I am investigating Vosk from Alpha Cephai next:

[u][Vosk, is available from Alpha Cephai](https://alphacephei.com/en/#opensource)[/u]


==== Install pocketsphinx-python ===

```
sudo apt-get install swig libpulse-dev
sudo pip install pocketsphinx
```

(USB mic ALSA device 2 with capture set at 81%)


Files in this repo:
carl_wakeup_mic.py   respond to spoken "Carl Wake Up"
example.py           reco from wav file in distribution
from_file.py         reco from passed filename  -f
from_mic_keyword.py  keyword reco from mic
from_mic.py          language model reco from mic
from_mic_w_gram.py   grammar reco from mic

justsophie.py        example used for pyAudio reco from mic
                     (good start_utterance threshold for my setup is around 1000)

live_keyword.py      LiveSpeech example blocked by pulse audio preference, not installed/configured
README.md  
system_info.py  
test16k.wav          sample in my voice mono 16kHz file with wave header
test.wav             attempt at mic default rate of 41kHz
grams/               folder for a corpus, dictionary and jsgf grammar 


==== FIRST TEST ====

download https://github.com/cmusphinx/pocketsphinx-python/blob/master/example.py

edit it to: 
 
``` 
# MODELDIR = "pocketsphinx/model"
MODELDIR = "/usr/local/lib/python3.5/dist-packages/pocketsphinx/model"
# DATADIR = "pocketsphinx/test/data"
DATADIR = "/usr/local/lib/python3.5/dist-packages/pocketsphinx/data"

# Create a decoder with certain model
config = Decoder.default_config()
# config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-hmm', path.join(MODELDIR, 'en-us'))
# config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
config.set_string('-lm', path.join(MODELDIR, 'en-us.lm.bin'))
# config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
config.set_string('-dict', path.join(MODELDIR, 'cmudict-en-us.dict'))
``` 

The program will read the file goforward.raw from DATADIR


python3 example.py
.
.
Best hypothesis segments:  ['<s>', '<sil>', 'go', 'forward', 'ten', 'meters', '</s>']
.

==== CREATE Voice File =====
* find mic device
lsusb
.
Bus 001 Device 004: ID 0c76:160a JMTek, LLC. 
.

arecord -D plughw:1,0 -d 3 -f S16_LE -r 16000 -c 1 test16k.wav

speak a phrase such as "What's the weather like?"

==== TEST from recorded Voice File =====

./from_file.py -f test16k.wav

Best hypothesis segments:  ['<s>', "what's", 'the', 'weather', 'like', '</s>']

==== TEST from mic ====

./from_mic.py



