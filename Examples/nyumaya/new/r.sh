#!/bin/bash

echo "Sample Record Tool"
if [ "$#" -ne 2 ]; then
    echo "Usage: ./r.sh 'spkrN-micN-<key_word_phrase>' <first file number>"
    exit 2
fi

i="$2" 
phrase="$1" 
# echo "phrase = $phrase"
while :
do
    istr=$(printf "%02d" $i)
    fname="$phrase$()-$istr.wav"
    # echo "fname = $fname"
    echo " "
    read -p "Press Return - Say: $phrase" x
    arecord -d 2 -c 1 -r 16000 -f S16_LE $fname
    echo "Sample $fname written"
    aplay $fname
    ((i++))

done
