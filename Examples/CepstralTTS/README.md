# Cepstral TTS for RPi


# Installation

1) Download voice from 
2) Expand
3) install
```
sudo sh install.sh

Install into what directory? [/opt/swift] 
/opt/swift does not exist.  Create it? ([n]/y) y

Swift will be installed in the following directories:

  Voices in /opt/swift/voices
  Shared libraries in /opt/swift/lib
  Binaries in /opt/swift/bin
  Configuration file in /opt/swift/etc
  Header files in /opt/swift/include
  Examples in /opt/swift/examples
  Sound effects filters in /opt/swift/sfx
  Documentation in /opt/swift/doc

Is this acceptable?  Enter 'yes' to continue: yes


Installing libraries...

***************************************************************************
If you are installing Swift system-wide, you may need to add the following
line to /etc/ld.so.conf and run ldconfig as root:

    /opt/swift/lib

(Otherwise, you will need to add it to the LD_LIBRARY_PATH environment
variable in order to run programs linked against the Swift libraries.)
***************************************************************************

Installing voice David...

Creating configuration...

Installing binaries...
Installing symbolic link to swift...
Installing man page...

Setting permissions...

Kill License Server

Testing the installed swift binary...
/opt/swift/bin/swift -o /dev/null 'hello world'

***************************************************************************
****************** Installation Completed Successfully! *******************
***************************************************************************
```

5) Test
```
cd Cepstral_David_arm-linux_6.1.5
/opt/swift/bin/swift -o ../test_david.wav -p audio/volume=400 'hello from Cepstral David Text To Speech.'
aplay ../test_david.wav
```

6) Install Charlie with same procedure

7) 

8) Use from python
```
import subprocess
subprocess.call(['swift', "text to be spoken"])
```

9)  Testing performance:
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
```
# Result - 5-7 second delay before hearing Cepstral TTS
 
10) To purchase Charlie voice (US$ 31.50)
- sign up for account
- Follow personal->desktop->linux link

11) To uninstall Cepstral TTS

- individual voice, simply delete that voice (for example, /opt/swift/voices/David-8kHz). 
- To remove all Cepstral software & voices, remove the /opt/swift" directory.

- kill the cepstral-licsrv process

sudo kill -9 `ps aux | grep cepstral-licsrv | grep -v grep | awk {'print $2'}`


