#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# ### mydetect.py  Monitor loudness, save recording if above A-weighted peak or RMS thresholds
#
# (Use calibrate.py to create equation for peak and RMS A-weighted loudness for selected microphone)
# (Use myplot.py to create (up to) 24 hour plots of peak and RMS results)
#
# This program records a 48kHz 16bit mono wave file for the set duration using arecord,
# then uses "SoundExchange" program sox to extract the peak and rms amplitudes between 0=no sound to 1.0 loudest
# Next the amplitudes are converted to "estimated" standard A-weighted loudness values
#      using a nonlinear 4 parameter logistic regression (single sided sigmoidal equation):
#      y = d + (a - d)/(1 + (x / c)**b)
# If either the peak or RMS A-weighted loudness values are above trigger thresholds,
#      the date-time, Peak and RMS loudness values are appended to a comma-separated-values (csv) file,
#      the wav file is compressed using lame to an mp3 file for later review.
# The wav file is deleted at the end of this loop, or upon cntl-C detection.
#
# .wav and .mp3 files are written to <base_folder>/audio/<date>/  (created if not existing)
# .csv files are written (one per day) to <base_folder>/csv/      (created if not existing)
#
# The basis for this program came from https://github.com/Mob-Barley/noise_level_protocol
#

import time
import subprocess
import os
from subprocess import call
import csv

# dBA Reference (Robot Measurements)
# 20 ~ Threshold of Hearing
# 27 ~ (Carpeted Room With Nobody Home)
# 30 ~ Rustling Leaves
# 37 ~ (Home Office / Computer Fans)
# 40 ~ Quiet Whisper
# 45 ~ (Quiet Whistling)
# 50 ~ Quiet Home
# 51 ~ (Home Office Typing Peaks)
# 60 ~ Quiet Street (Quiet Conversation)
# 65 ~ (Adult Conversation)
# 70 ~ Normal Conversation
# 75 ~ Inside Car
# 80 ~ Loud Singing
# 88 ~ Automobile
# 90 ~ Motorcycle
# 94 ~ Food Blender
# 100 ~ Subway
# 107 ~ Diesel Truck
# 115 ~ Power Lawn Mower
# 120 ~ Chain Saw
# 130 ~ Rock Band

# peaks 55-65 (TV on in Livingroom, Carl in office)
# rms 57-62   (Carl in front of TV, clapping peak 66 dBA)


# trigger values - (save audio if level is greater than or equal to trigger value)
trigger_peak = 45.0
trigger_rms = 40.0
header_csv = ("time", "Loudness Peak(dBA)", "RMS Loudness(dBA)")

#change folder path here
base_folder = "./"

#change duration to detect here
dur = " 30 "  # seconds suggest 10-120

# test your microphone 30-80 dB in 5 dB steps with calibrate.py
# create the function e.g. with mycurvefit.com
# y_dBA = d + (a - d)/(1 + (x_amplitude / c)**b)
# 4PL nonweighted Peak 27-80 dBA
a_peak = -3989824
b_peak = 0.1744041
c_peak = 7.172477 * (10 ** -30)
d_peak = 111.4455

#4PL nonweighted RMS 27-80 dB
a_rms = -9241.244
b_rms = 0.04039854
c_rms = 5.363753 * (10 ** -42)
d_rms = 293.8987

# make sure folder for csv files exists (executes once after clean_dirs or install)
csvfolder = base_folder + "csv/"
if not os.path.exists(csvfolder):
            os.makedirs(csvfolder)
            print(csvfolder + " folder created")

try:
    while True:
        #pkill zombies
        subprocess.call("pkill -9 sox | pkill -9 arecord",shell= True)
        time.sleep( 1 )

        #encode date time for filenames and data
        filedate = time.strftime("%Y%m%d-%H%M%S")
        audiofolder = base_folder + "audio/" + time.strftime("%Y%m%d") + "/"
        basefilename = audiofolder + filedate
        wavfilename = basefilename + ".wav"
        filename_csv = csvfolder + time.strftime("%Y%m%d") + ".csv"
        filedate_csv  = time.strftime("%Y-%m-%d %H:%M:%S")
        terminal_time = time.strftime("%H:%M:%S ")

        # make sure folder for audio exists (executes once each day)
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

        subprocess.call("arecord -D hw:1,0 -d " + dur + " --fatal-errors --buffer-size=192000 -f S16_LE -r48000 -c1 --quiet " + wavfilename,shell= True)

        # SoX sound exchange (swiss knife for audio)
        # sox options:
        #   -n  null output file - throw away output
        #   stat
        # use sox to extract peak and rms amplitude (PCM) values
        sox_peak = subprocess.getoutput("sox " + wavfilename + " -n stat 2>&1 | grep 'Maximum amplitude' | cut -d ':' -f 2")
        sox_rms = subprocess.getoutput("sox " + wavfilename + " -n stat 2>&1 | grep 'RMS.*amplitude' | cut -d ':' -f 2")

        # Longer durations need a little extra time to complete (will lose the Measured values printout for some reason)
        if int(dur) >= 30: time.sleep(1)
        if int(dur) >= 60: time.sleep(1)

        # clear console output so far
        #os.system('clear')

        sox_peak_amplitude = sox_peak.strip()        # strip off spaces
        peak_amplitude = float(sox_peak_amplitude)        # convert string value to float value
        sox_rms_amplitude = sox_rms.strip()
        rms_amplitude = float(sox_rms_amplitude)

        # compute peak dBA from reading using curve fit
        peak_dBA = d_peak + (a_peak - d_peak)/(1 + (peak_amplitude / c_peak)**b_peak)

        rms_dBA = d_rms + (a_rms - d_rms)/(1 + (rms_amplitude / c_rms)**b_rms)

        #round the values to whole number and add db filename extention: peak - rms
        ext_peak = int(round(peak_dBA, 0))
        ext_rms = int(round(rms_dBA, 0))


        #print("Measured values - peak: " + sox_peak_amplitude + " rms: " + sox_rms_amplitude + " == peak: " + str(round(peak_dBA,1)) + " dBA / rms: " + str(round(rms_dBA,1)) + " dBA")
        print("Measured values - peak: " + sox_peak_amplitude + " rms: " + sox_rms_amplitude + " == peak: " + str(ext_peak) + " dBA / rms: " + str(ext_rms) + " dBA")


        #csv
        file_exists = os.path.isfile(filename_csv)
        daten_csv = (filedate_csv, str(round(peak_dBA,1)), str(round(rms_dBA,1)))
        delfilesname = base_folder + "audio/" + time.strftime("%Y%m%d") + "/*.wav"
        with open(filename_csv, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(header_csv)
            writer.writerow(daten_csv)

        if peak_dBA >= trigger_peak or rms_dBA >= trigger_rms:
                    mp3filename = basefilename + "-" + str(ext_peak) + "-" + str(ext_rms) + ".mp3"
                    print(terminal_time + "Sound detected - save compressed audio: " + mp3filename +"\n")
                    # lame (encodes to variable bit rate mp3) options:
                    #   -r input is raw (headerless) PCM  (caused libsnd warning)
                    #   --quiet   no messages to std out
                    #   --preset standard is same as -V 2  VBR Quality  about 200kbps
                    #   (-  read from stdin)
                    #   - m m  mode mono
                    #  (output mp3 encoded data to filename)
                    subprocess.call("lame --quiet -m m "+ wavfilename + " " + mp3filename, shell=True)
                    subprocess.call("rm " + delfilesname, shell=True)
                    #time.sleep( 1 )
                    #os.system('clear')

        else:
            print(terminal_time + "No sound detected, deleting .wav file(s)\n")
            subprocess.call("rm " + delfilesname, shell=True)
            #time.sleep( 1 )
            #os.system('clear')

except KeyboardInterrupt:
        subprocess.call("pkill -9 sox | pkill -9 arecord",shell= True)
        delfilesname = base_folder + "audio/" + time.strftime("%Y%m%d") + "/*.wav"
        subprocess.call("rm " + delfilesname, shell=True)

        print(' End mydetect.py\n')
