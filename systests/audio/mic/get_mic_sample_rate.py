#!/usr/bin/env python3


# to install pyaudio
# sudo pip3 install pyaudio

# ignore all the alsa configuration errors - it will work
# had to set exception_on_overflow = False on the read or always got exception


import pyaudio

def main():
	p = pyaudio.PyAudio()

	print("\n\n")
	for i in range(p.get_device_count()):
		dev = p.get_device_info_by_index(i)
		rate = dev['defaultSampleRate']
		print("device: {:>3d} name: {:<35s} channels: {:>3d} defaultSampleRate: {:>10s}".format(i,dev['name'], dev['maxInputChannels'], str(rate)))

if __name__ == '__main__':
	main()
