#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#
# clean_dirs.py   delete all audio files and the folder 
#                 delete all .csv files and the folder

import time
import subprocess

base_dir = "./"
audiofolder = base_dir + "audio/"
csv_folder = base_dir + "csv/"

print("Deleting audio/ and csv/")
result = subprocess.Popen("rm -r " + audiofolder, shell=True,  stdout=subprocess.PIPE)
result = subprocess.Popen("rm -r " + csv_folder,   shell=True,  stdout=subprocess.PIPE)
time.sleep(3)

