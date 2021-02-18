#!/usr/bin/env python3

# FILE: find_mic_device_number.py

# PURPOSE:  The Vosk engine needs to be told what device number to use for the microphone
#           ./find_mic_device_number.py will print out the device number for device: mic

# For Carl: use device 25 mic (device 2 does not handle rate conversion)

"""
$ ./find_mic_device_number.py
Cannot connect to server socket err = No such file or directory
Cannot connect to server request channel
jack server is not running or cannot be started
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1, skipping unlock
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1, skipping unlock
Cannot connect to server socket err = No such file or directory
Cannot connect to server request channel
jack server is not running or cannot be started
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1, skipping unlock
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1, skipping unlock
ALSA lib pcm_oss.c:377:(_snd_pcm_oss_open) Unknown field port
ALSA lib pcm_oss.c:377:(_snd_pcm_oss_open) Unknown field port
ALSA lib pulse.c:243:(pulse_connect) PulseAudio: Unable to connect: Connection refused

ALSA lib pulse.c:243:(pulse_connect) PulseAudio: Unable to connect: Connection refused

ALSA lib pcm_a52.c:823:(_snd_pcm_a52_open) a52 is only for playback
ALSA lib conf.c:4871:(parse_args) Unknown parameter AES0
ALSA lib conf.c:5031:(snd_config_expand) Parse arguments error: No such file or directory
ALSA lib pcm.c:2565:(snd_pcm_open_noupdate) Unknown PCM iec958:{AES0 0x6 AES1 0x82 AES2 0x0 AES3 0x2  CARD 0}
ALSA lib pcm_usb_stream.c:486:(_snd_pcm_usb_stream_open) Invalid type for card
ALSA lib pcm_usb_stream.c:486:(_snd_pcm_usb_stream_open) Invalid type for card
Cannot connect to server socket err = No such file or directory
Cannot connect to server request channel
jack server is not running or cannot be started
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1, skipping unlock
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1, skipping unlock
Input Device id  2  -  USB Audio Device: - (hw:2,0)
Input Device id  25  -  mic
Input Device id  27  -  default

"""

import pyaudio
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
