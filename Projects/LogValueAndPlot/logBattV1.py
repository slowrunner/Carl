#!/usr/bin/env python
#-*- coding: utf-8 -*-

# ### logBattV.py  Logs date-time and battery voltage to 
#                  <base_dir>/battV/csv/battV-<starting_date>.csv
#
# (Use plotBattV.py or plotBattLife.py to create visual plot of result)
#
# .csv files are written to <base_folder>/battV/csv/battV-<starting_date>.csv
#            (path created if not existing)
#            with format:  YYYY-MM-DD HH:MM:SS, nn.nn
#            (nn.nn in volts)
#
# The logged value is the gopigo3 reported battery voltage, 
#   which is 0.6v lower than the actual battery pack voltage
#   due to the reverse polarity protection diode between the pack and gopigo3
#

from __future__ import print_function

import time
import subprocess
import os
from subprocess import call
import csv
import easygopigo3

# ### Create (protected) instance of EasyGoPiGo3 base class
egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)

header_csv = ("Date Time          ", "Battery Voltage")

#change folder path here
base_folder = "./"

#change duration between measurements here
dur = 12  # seconds

# make sure folder for csv files exists (executes once)
csvfolder = base_folder + "battV/csv/"
if not os.path.exists(csvfolder):
            os.makedirs(csvfolder)
            print(csvfolder + " folder created")

#encode starting date time for filename
        filedate = time.strftime("%Y%m%d")
        filename_csv = csvfolder + "battV-" + filedate + ".csv"


try:
    while True:

        # make current datetime string for this reading
        reading_datetime_csv  = time.strftime("%Y-%m-%d %H:%M:%S")
        terminal_time = time.strftime("%H:%M:%S ")

        battV = egpg.volt()

        print( "logBattV: ", terminal_time, str(round(battV,2)) )


        #csv
        file_exists = os.path.isfile(filename_csv)
        daten_csv = (reading_datetime_csv, str(round(battV,2)) )
        #with open(filename_csv, 'a', newline='') as f:
        with open(filename_csv, 'a') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(header_csv)
            writer.writerow(daten_csv)

        time.sleep(dur)


except KeyboardInterrupt:

        print('\n')
        print('End logBattV.py')
        print('\n')
