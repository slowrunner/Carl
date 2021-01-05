# Porcupine For GoPiGo3

# Installation
(based on https://github.com/Picovoice/porcupine#try-it-out)

```
 sudo pip3 install pvporcupinedemo
.
.
Successfully installed enum34-1.1.10 pvporcupine-1.9.0 pvporcupinedemo-1.9.0 pyaudio-0.2.11 soundfile-0.10.3.post1

```
# Show audio devices

```
$ porcupine_demo_mic --keywords porcupine --show_audio_devices
.
.
'index': '0', 'name': 'USB Audio Device: - (hw:2,0)', 'defaultSampleRate': '44100.0', 'maxInputChannels': '1'
'index': '1', 'name': 'mic', 'defaultSampleRate': '44100.0', 'maxInputChannels': '128'
```
**Note: Although the mic is showing up on index 0 and 1, only index 1 will provide porcupine with 16kHz sample rate**

# Run Demo
```
porcupine_demo_mic --keywords porcupine --audio_device_index 1

(Ignore warnings ...)
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

(Initialized OK now ...)

Listening {
  porcupine (0.50)
}
[2021-01-04 12:04:47.312002] Detected porcupine
[2021-01-04 12:04:50.480086] Detected porcupine
[2021-01-04 12:04:52.144338] Detected porcupine    <-- WHISPERED FROM ACROSS THE ROOM
[2021-01-04 12:04:53.679995] Detected porcupine    <-- Whispered even quieter
[2021-01-04 12:04:55.280396] Detected porcupine
[2021-01-04 12:04:59.247942] Detected porcupine
^CStopping ...

```
# Run Carl Responding to Porcupine Wake Word

```
./carl_porcupine_mic.py
```

Carl says "Yes. I heard you" when he hears the wake word "porcupine" spoken or whispered.


# To See Default Keywords

```
$ python3
>>> import pvporcupine
>>> print(pvporcupine.KEYWORDS)
{'ok google', 'terminator', 'bumblebee', 'americano', 'picovoice', 'jarvis', 'alexa', 'hey siri', 'computer', 'porcupine', 'grasshopper', 'hey google', 'grapefruit', 'blueberry'}
```

# Power and Processing Result

From an electrical power view, running the PicoVoice Porcupine engine resulted in a "playtime" reduction from 7.9 hours to 7.6 hours - 3% reduction or a 24 hour cost of 37 minutes.  

It did not mess up the smart charger's peak deltaV battery full detection. (Processes which present varying load can trigger false peak detection with the charger switching to trickle charging mode before the batteries are truly full.)

The 15 minute processing load increased by 0.1 which is roughly 10% of one core of the four Raspberry Pi 3B cores  

# Personal Accounts Cannot Create Custom Wake Words

Alas, while the PicoVoice Porcupine Wake Word Engine has exceptional recognition, zero false recognition, with very low processing and electrical footprint, 

**The bottom line is Carl needs a wake word engine that responsds to:**
- Wake Up Carl
- Listen Carl

