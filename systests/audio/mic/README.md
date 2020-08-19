Microphone Selection For Robot Carl
(Raspberry Pi 3B on GoPiGo3 robot)

- Using Raspbian For Robots (Stretch)

- Movo MA200GY Omni directional Electret Condenser 
  Sensitivity: -30dB +/-3dB / 1kHz 0dB=1V/Pa, S/N: 74dB SPL, 
- Kinobo Mini Akira: 
  Sensitivity -47dB +/-4dB

- Recorded phrase "What Time Is It Carl" on iPhone10 voice memos
- Played back phrase four times at max voluume at 32 inches from mics
- Recorded test at 48k 16bit Little Endian (16_SLE) with 
  arecord -c1 -d 30 -f 16_SLE compare_48k16bitLE.wav

- Used DB-Pro app on iPhone10 laying on floor next to robot
  (robot has MonkMakes speaker mounted facing floor)

- Results:
  Movo MA2000GY: 66.0 dBA
  Kinobo Akira : 64.7 dBA

- from_mic_w_gram.py test
  Movo   average silence level 4250
  Kinobo average silence level 1000

- from_file.py (language model test) neither mic in 16k or 48k gave good reco

- from_file_w_gram.py -g test_files/carl.jsgf -f test_files/
  - 48k files do not reco with pktsphinx
  - 16k files: Both mics result in perfect reco for all phrases tested.

- Need to test progressive distance reco


