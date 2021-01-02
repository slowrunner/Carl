# Test of Google Cloud Speech On The Raspberry Pi (no GoPiGo3 calls)


- See Mac External Drive//PiStuff/GoogleCloudSpeech/Install_google.cloud.speech.txt


The complicated part is setting up a service account for project, and downloading credentials file


1) Record some sample audio using record_samples.sh

```
pi@Carl:~/Carl/Examples/GoogleCloud/GoogleCloudSpeechToText $ ./record_samples.sh 
Testing Speaker First

speaker-test 1.1.8

Playback device is default
Stream parameters are 48000Hz, S16_LE, 2 channels
WAV file(s)
Rate set to 48000Hz (requested 48000Hz)
Buffer size range from 480 to 32768
Period size range from 480 to 32768
Using max buffer size 32768
Periods = 4
was set period_size = 8192
was set buffer_size = 32768
 0 - Front Left
 1 - Front Right
Time per period = 2.413342
Say 'This is seven seconds of 8k 8bit unsigned mono audio'
Recording WAVE 'test8k8bitUnsignedMono.wav' : Unsigned 8 bit, Rate 8000 Hz, Mono
sleep 10
Say 'This is 10 seconds of signed 16 bit little endian 48k mono audio'
Recording WAVE 'test48k16bitLittleEndianMono.wav' : Signed 16 bit Little Endian, Rate 48000 Hz, Mono
sleep 10
Say 'This is 10 seconds of signed 16 bit little endian 44.1k mono audio'
Recording WAVE 'test44k16bitLittleEndianMono.wav' : Signed 16 bit Little Endian, Rate 44100 Hz, Mono
sleep 10
Say 'This is 10 seconds of signed 16 bit little endian 16k mono audio'
Recording WAVE 'test16k16bitLittleEndianMono.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono
sleep 5
Playing WAVE 'test8k8bitUnsignedMono.wav' : Unsigned 8 bit, Rate 8000 Hz, Mono
Playing WAVE 'test48k16bitLittleEndianMono.wav' : Signed 16 bit Little Endian, Rate 48000 Hz, Mono
Playing WAVE 'test44k16bitLittleEndianMono.wav' : Signed 16 bit Little Endian, Rate 44100 Hz, Mono
Playing WAVE 'test16k16bitLittleEndianMono.wav' : Signed 16 bit Little Endian, Rate 16000 Hz, Mono
```
2) Test file transcription:  ./carl_transcribe_file.py test16k16bitLittleEndianMono.wav
  - Change env to python3, file: snippets/transcribe.py
```
pi@Carl:~/Carl/Examples/GoogleCloud/GoogleCloudSpeechToText $ ./carl_transcribe_file.py test16k16bitLittleEndianMono.wav 
Transcript: this is 10 seconds of signed 16 bit little endian 16k mono audio
```

3) Test streaming recognition:  ./carl_transcribe_streaming_mic.py
  - (File: samples/microphone/transcribe_streaming_mic.py)
  - changed env to python3, sample rate to 44100 default for my microphone  

```
pi@Carl:~/Carl/Examples/GoogleCloud/GoogleCloudSpeechToText $ ./carl_transcribe_streaming_mic.py 

Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Expression 'alsa_snd_pcm_hw_params_set_period_size_near( pcm, hwParams, &alsaPeriodFrames, &dir )' failed in 'src/hostapi/alsa/pa_linux_alsa.c', line: 924
Cannot connect to server socket err = No such file or directory
Cannot connect to server request channel
jack server is not running or cannot be started
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1, skipping unlock
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for -1, skipping unlock



hello Carl
what you doing
goodbye


^C
Traceback (most recent call last):
  File "./carl_transcribe_streaming_mic.py", line 197, in <module>
    main()
  File "./carl_transcribe_streaming_mic.py", line 193, in main
    listen_print_loop(responses)
  File "./carl_transcribe_streaming_mic.py", line 128, in listen_print_loop
    for response in responses:
  File "/home/pi/.local/lib/python3.7/site-packages/google/api_core/grpc_helpers.py", line 97, in next
    return six.next(self._wrapped)
  File "/home/pi/.local/lib/python3.7/site-packages/grpc/_channel.py", line 416, in __next__
    return self._next()
  File "/home/pi/.local/lib/python3.7/site-packages/grpc/_channel.py", line 794, in _next
    _common.wait(self._state.condition.wait, _response_ready)
  File "/home/pi/.local/lib/python3.7/site-packages/grpc/_common.py", line 141, in wait
    _wait_once(wait_fn, MAXIMUM_WAIT_TIMEOUT, spin_cb)
  File "/home/pi/.local/lib/python3.7/site-packages/grpc/_common.py", line 106, in _wait_once
    wait_fn(timeout=timeout)
  File "/usr/lib/python3.7/threading.py", line 300, in wait
    gotit = waiter.acquire(True, timeout)
KeyboardInterrupt
```

