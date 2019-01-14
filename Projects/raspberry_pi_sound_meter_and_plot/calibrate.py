#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import time
import subprocess
import os
from subprocess import call
import csv


#change folder path here
base_folder = "./"

#change duration to detect here
dur = " 10 "  # or 120

try:
    while True:
        #pkill because sometimes my microphone was busy
        subprocess.call("pkill -9 sox | pkill -9 arecord",shell= True)
        time.sleep( 1 )

        #time
        filedate = time.strftime("%Y%m%d-%H%M%S")
        audiofolder = base_folder + "audio/" + time.strftime("%Y%m%d") + "/"
        basefilename = base_folder + "audio/" + time.strftime("%Y%m%d") + "/" + filedate
        wavfilename = basefilename + ".wav"
        filename_csv = base_folder + "csv/" + time.strftime("%Y%m%d") + ".csv"
        filedate_csv  = time.strftime("%Y-%m-%d %H:%M")
        terminal_time = time.strftime("%H:%M ")

        # make sure folder for audio exists (executes once)
        if not os.path.exists(audiofolder):
          os.makedirs(audiofolder)
          print(audiofolder + " folder created")


        #record for duration
        print("Listening for " + dur + " seconds...")
        # arecord options:
        #   original -f dat =  (16 bit little endian, 48000, stereo) [-f S16_LE -c2 -r48000]
        #   -v verbose list input parameters and configuration values
        #   --quiet  suppress messages
        #   --buffer-size=192ms (interrupts at 4x buffersize giving 4 times sampling for 48kHz
        #   -t raw   output file type: raw = PCM data no header  (dropped to get rid of lame libsnd warning)
        #   --fatal-errors  disables recovery attempts on errors

        # lame (encodes to variable bit rate mp3) options:
        #   -r input is raw (headerless) PCM  (caused libsnd warning)
        #   --quiet   no messages to std out
        #   --preset standard is same as -V 2  VBR Quality  about 200kbps
        #   -  read from stdin
        #   - m m  stereo mode mono
        #  (output mp3 encoded data to filename)
        # subprocess.call("arecord -D hw:1,0 -d " + dur + " -v --fatal-errors --buffer-size=192000 -f dat -t raw --quiet | lame -r --quiet --preset standard - " + filename,shell= True)
        # subprocess.call("arecord -D hw:1,0 -d " + dur + " --fatal-errors --buffer-size=192000 -f S16_LE -r48000 -c1 -t raw --quiet | lame --verbose -r -m m --bitwidth 16 -s 48 --preset standard - " + filename,shell= True)
        subprocess.call("arecord -D hw:1,0 -d " + dur + " --fatal-errors --buffer-size=192000 -f S16_LE -r48000 -c1 --quiet " + wavfilename,shell= True)

        # SoX sound exchange (swiss knife for audio)
        # sox options:
        #   -n  null output file - throw away output
        #   stat 
        # use sox to extract peak and rms amplitude (PCM) values
        #proc = subprocess.getoutput("sox " + filename + " -n stat 2>&1 | grep 'Maximum amplitude' | cut -d ':' -f 2")
        #proc_rms = subprocess.getoutput("sox " + filename + " -n stat 2>&1 | grep 'RMS.*amplitude' | cut -d ':' -f 2")
        proc = subprocess.getoutput("sox " + wavfilename + " -n stat 2>&1 | grep 'Maximum amplitude' | cut -d ':' -f 2")
        proc_rms = subprocess.getoutput("sox " + wavfilename + " -n stat 2>&1 | grep 'RMS.*amplitude' | cut -d ':' -f 2")

        # clear console output so far
        #os.system('clear')

        proc1 = proc.strip()        # strip off spaces
        proc1 = float(proc1)        # convert string value to float value
        proc_rms = proc_rms.strip()
        proc_rms = float(proc_rms)


        print("Measured values - peak: " + str(proc1) + " rms: " + str(proc_rms) + "\n")


        delfilesname = base_folder + "audio/" + time.strftime("%Y%m%d") + "/*.wav"
        subprocess.call("rm " + delfilesname, shell=True)

except KeyboardInterrupt:
        subprocess.call("pkill -9 sox | pkill -9 arecord",shell= True)
        delfilesname = base_folder + "audio/" + time.strftime("%Y%m%d") + "/*.wav"
        subprocess.call("rm " + delfilesname, shell=True)

        print(' End calibrate.py\n')
