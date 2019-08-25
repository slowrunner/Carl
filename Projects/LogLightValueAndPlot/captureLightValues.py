#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# ### captureLightValues.py  Logs date-time and EXIF:Brightness Value to
#                   logfiles/bv-<starting_date>-<starting_time>.csv
#
#
# .csv files are written to ./logfiles
#            (path created if not existing)
#            named bv-YYYYMMDD-HHMM.csv
#            with data format:  YYYY-MM-DD HH:MM:SS, nn.nn
#            nn.nn is from EXIF:Brightness Value
#

from __future__ import print_function

import time
import subprocess
import os
from subprocess import call
import csv
import easygopigo3
import sys
sys.path.append('/home/pi/Carl/plib')
import runLog
import exifread
import camUtils
import datetime as dt
from fractions import Fraction
from decimal import Decimal

# ### Create (protected) instance of EasyGoPiGo3 base class
egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)

dtNow = dt.datetime.now()
strNow = time.strftime("%Y%m%d-%H:%M:%S")
runLog.logger.info("Starting captureLightValues.py")

header_csv = ("Date Time          ", "Brightness Value")

#change folder path here
base_folder = "./"

#change duration between captures here
dur = 57  # seconds - results in 60s loop

# make sure folder for csv files exists (executes once)
csvfolder = base_folder + "logfiles/"
if not os.path.exists(csvfolder):
            os.makedirs(csvfolder)
            print(csvfolder + " folder created")

imagefolder = base_folder + "images/"
if not os.path.exists(imagefolder):
            os.makedirs(imagefolder)
            print(imagefolder + " folder created")

#encode starting date time for filename
filedate = time.strftime("%Y%m%d-%H%M%S")
filename_csv = csvfolder + "bv-" + filedate + ".csv"

BV_EXIF_KEY = 'EXIF BrightnessValue'

try:
    while True:

        jpg_fp = camUtils.snapJPG(fpath=imagefolder)
        print("Captured {}".format(jpg_fp))



        # make current datetime string for this reading
        # reading_datetime_csv  = time.strftime("%Y-%m-%d %H:%M:%S")
        # terminal_time = time.strftime("%H:%M:%S ")

        # print("index('_')",jpg_fp.index('_'))
        jpg_datetime_str = jpg_fp[(jpg_fp.index('_')+1):-4]
        # print("jpg_datetime_str",jpg_datetime_str)
        jpg_datetime = dt.datetime.strptime(jpg_datetime_str, '%Y%m%d-%H%M%S')
        # print("jpg_datetime",jpg_datetime)

        reading_datetime_csv = jpg_datetime.strftime("%Y-%m-%d %H:%M:%S")
        terminal_time = jpg_datetime.strftime("%H:%M:%S ")

        jpg_fptr = open(jpg_fp, 'rb')
        tags = exifread.process_file(jpg_fptr, details=False) # no thumbnail or makernote
        jpg_fptr.close()

        # for tagkey in tags.keys():
        #     print("Key: {}, value {}".format(tagkey, tags[tagkey]))
        """
        bvstr = tags[BV_EXIF_KEY]
        print( "tags[BV_EXIF_KEY: {}".format( bvstr ))
        bvstr = str(bvstr)
        print( "str(bvstr): {}".format(  bvstr ))
        bvstr = Fraction(bvstr)
        print( "Fraction: {}".format(  bvstr ))
        bvstr = float(bvstr)
        print( "float(bvstr): {}".format( bvstr ))
        bvstr = round(bvstr,3)
        print( "round(bvstr,3): {}".format( bvstr ))
        bvstr = str(bvstr)
        print( "str(bvstr): {}".format( bvstr ))
        """
        bvstr = str(round(float(Fraction(str(tags[BV_EXIF_KEY]))),3))
        print( "{} Brightness Value: {}".format( terminal_time, bvstr ))


        #csv
        file_exists = os.path.isfile(filename_csv)
        daten_csv = (reading_datetime_csv, bvstr )
        #with open(filename_csv, 'a', newline='') as f:
        with open(filename_csv, 'a') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(header_csv)
            writer.writerow(daten_csv)

        time.sleep(dur)


except KeyboardInterrupt:
        runLog.logger.info("Exiting  captureLightValue.py")

        print('\n')
        print('End captureLightValue.py')
        print('\n')
