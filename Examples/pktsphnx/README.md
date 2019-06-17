README.md

==== Install pocketsphinx-python ===

sudo apt-get install swig libpulse-dev
sudo pip install pocketsphinx


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



