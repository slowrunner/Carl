#!/usr/bin/env python

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

import os
import pyaudio
import wave
import audioop
from collections import deque
import time
import math
import sys

"""
Written by Sophie Li, 2016
http://blog.justsophie.com/python-speech-to-text-with-pocketsphinx/
"""

class SpeechDetector:
    def __init__(self,input_dev=0):
        # Microphone stream config.
        # self.CHUNK = 1024  # CHUNKS of bytes to read each time from mic
        self.CHUNK = 3072  # CHUNKS of bytes to read each time from mic
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1

        self.CAPTURE_DEV_INDEX = input_dev

        # Get sample rate from capture device
        p = pyaudio.PyAudio()
        self.RATE = int(p.get_device_info_by_index(self.CAPTURE_DEV_INDEX)['defaultSampleRate'])
        print("\n\n*** Mic sample rate:",self.RATE)

        self.RATE = 16000

        self.SILENCE_LIMIT = 1  # Silence limit in seconds. The max ammount of seconds where
                           # only silence is recorded. When this time passes the
                           # recording finishes and the file is decoded

        self.PREV_AUDIO = 0.5  # Previous audio (in seconds) to prepend. When noise
                          # is detected, how much of previously recorded audio is
                          # prepended. This helps to prevent chopping the beginning
                          # of the phrase.

        # self.THRESHOLD = 4500
        self.THRESHOLD = 2500
        self.num_phrases = -1

        # These will need to be modified according to where the pocketsphinx folder is
        # MODELDIR = "../../tools/pocketsphinx/model"
        # DATADIR = "../../tools/pocketsphinx/test/data"

        # Create a decoder with certain model
        # config = Decoder.default_config()
        # config.set_string('-hmm', os.path.join(MODELDIR, 'en-us/en-us'))
        # config.set_string('-lm', os.path.join(MODELDIR, 'en-us/en-us.lm.bin'))
        # config.set_string('-dict', os.path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))

        MODELDIR = "/usr/local/lib/python3.5/dist-packages/pocketsphinx/model"
        DATADIR = "/usr/local/lib/python3.5/dist-packages/pocketsphinx/data"

        # Create a decoder with en-us model
        config = Decoder.default_config()

        config.set_string('-hmm', os.path.join(MODELDIR, 'en-us'))
        config.set_string('-lm', os.path.join(MODELDIR, 'en-us.lm.bin'))
        config.set_string('-dict', os.path.join(MODELDIR, 'cmudict-en-us.dict'))
        config.set_string('-logfn', 'justsophie2.out')
        config.set_string('-samprate', str(int(self.RATE)))


        # Creaders decoder object for streaming data.
        self.decoder = Decoder(config)

    def setup_mic(self, num_samples=50):
        """ Gets average audio intensity of your mic sound. You can use it to get
            average intensities while you're talking and/or silent. The average
            is the avg of the .2 of the largest intensities recorded.
        """
        print("Getting intensity values from mic.")
        p = pyaudio.PyAudio()

        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        values = [math.sqrt(abs(audioop.avg(stream.read(self.CHUNK), 4)))
                  for x in range(num_samples)]
        values = sorted(values, reverse=True)
        r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
        print(" Finished ")
        print(" Average audio intensity is ", r)
        stream.close()
        p.terminate()

        if r < 3000:
            # self.THRESHOLD = 3500
            self.THRESHOLD = int(r)
        else:
            self.THRESHOLD = int(r + 100)

        print("Audio Threshold set to :",self.THRESHOLD)

    def save_speech(self, data, p):
        """
        Saves mic data to temporary WAV file. Returns filename of saved
        file
        """
        filename = 'output_'+str(int(time.time()))
        # writes data to WAV file
        data = b''.join(data)
        wf = wave.open(filename + '.wav', 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.RATE)  # ALAN - changed to value from setup_mic
        wf.writeframes(data)
        wf.close()
        return filename + '.wav'

    def decode_phrase(self, wav_file):
        self.decoder.start_utt()
        stream = open(wav_file, "rb")
        while True:
          buf = stream.read(1024)
          if buf:
            self.decoder.process_raw(buf, False, False)
          else:
            break
        self.decoder.end_utt()
        words = []
        [words.append(seg.word) for seg in self.decoder.seg()]
        return words

    def run(self):
        """
        Listens to Microphone, extracts phrases from it and calls pocketsphinx
        to decode the sound
        """
        self.setup_mic()

        #Open stream
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        print("* Mic set up and listening. ")

        audio2send = []
        # cur_data = ''  # current chunk of audio data
        cur_data = ""  # current chunk of audio data
        rel = self.RATE/self.CHUNK
        #slid_win = deque(maxlen=self.SILENCE_LIMIT * rel)
        slid_win = deque(maxlen=int(self.SILENCE_LIMIT * rel))
        #Prepend audio from 0.5 seconds before noise was detected
        # prev_audio = deque(maxlen=self.PREV_AUDIO * rel)
        prev_audio = deque(maxlen=int(self.PREV_AUDIO * rel))
        started = False

        while True:
            # cur_data = stream.read(self.CHUNK)
            cur_data = stream.read(self.CHUNK,exception_on_overflow=False)
            slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))

            if sum([x > self.THRESHOLD for x in slid_win]) > 0:
                if started == False:
                    print("Starting recording of phrase")
                    started = True
                audio2send.append(cur_data)

            elif started:
                print("Finished recording, decoding phrase")
                filename = self.save_speech(list(prev_audio) + audio2send, p)
                r = self.decode_phrase(filename)
                print("DETECTED: ", r)

                # Removes temp audio file
                os.remove(filename)
                # Reset all
                started = False
                # slid_win = deque(maxlen=self.SILENCE_LIMIT * rel)
                # prev_audio = deque(maxlen=0.5 * rel)
                slid_win = deque(maxlen=int(self.SILENCE_LIMIT * rel))
                prev_audio = deque(maxlen=int(0.5 * rel))
                audio2send = []
                print("\n\n*** Listening ...")

            else:
                prev_audio.append(cur_data)

        print("* Done listening")
        stream.close()
        p.terminate()

if __name__ == "__main__":

    MY_MIC_ALSA_DEV_INDEX = 2
    sd = SpeechDetector(input_dev=MY_MIC_ALSA_DEV_INDEX)
    try:
        sd.run()
    except (KeyboardInterrupt):
        print('\nGoodbye.')
        sys.exit()
    except Exception as e:
        exc_type, exc_value, exc_tranceback = sys.exe_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2,
                                  file=sys.stdout)
        sys.exit()
