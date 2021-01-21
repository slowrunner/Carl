#!/bin/bash
phrase="Hi.  My name is Carl.  How do you like this voice?"
phrase_w_underscores="Hi_My_name_is_Carl_How_do_you_like_this_voice?"
echo " "
echo "*****"
echo "flite"
time flite -t "f light. Hi. My name is Carl.  How do you like this voice?" -o samples/flite.wav
# pico2wave -w samples/pico.wav -l en-US "pico to wave "$phrase
# espeak -w samples/espeak.wav "e speak "$phrase"
echo " "
echo "*****"
echo "espeak-ng"
time espeak-ng -w samples/espeak-ng.wav "e speak n g"$phrase_w_underscores
echo " "
echo "*****"
echo "cepstral"
time /opt/swift/bin/swift -o samples/cepstral-charlie.wav -p audio/volume=400 "cepstral charlie "$phrase
echo " "
echo "*****"
echo "plib espeak-ng option rate 150 volume 125"
time espeak-ng -w samples/plib_espeak-ng.wav -s150 -ven-us+f5 -a125 "p lib e speak n g"$phrase_w_underscores
