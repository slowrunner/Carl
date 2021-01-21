# systests/audio/tts

```
( using phrase: "<engine-name> Hi.  My name is Carl.  How do you like this voice?" )
$ ./make_tts_samples.sh 
 
*****
flite

real	0m0.565s
user	0m0.122s
sys	0m0.050s
 
*****
espeak-ng

real	0m0.283s
user	0m0.064s
sys	0m0.044s
 
*****
cepstral

real	0m7.479s
user	0m3.727s
sys	0m0.981s
 
*****
plib espeak-ng option rate 150 volume 125

real	0m0.386s
user	0m0.101s
sys	0m0.058s


$ ls -1 samples/
cepstral-charlie.wav
espeak-ng.wav
flite_ssml.wav   <- sample with flite reading a file with SSML (speech synthesis markup language)  
flite.wav
plib_espeak_ng.wav   <- voice I am currently using for Carl -s150 -a125 option


