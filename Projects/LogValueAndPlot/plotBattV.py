#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function

import matplotlib
matplotlib.use('Agg')
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
import os

from matplotlib import rcParams
from datetime import timedelta, date
import matplotlib.patches as mpatches
from matplotlib.ticker import AutoMinorLocator


dateOfPlot = date.today()

# uncomment next line to plot yesterday's data
#dateOfPlot = date.today() - timedelta(days=1)

base_folder = "./"
value_folder = "battV/"
filename_csv = base_folder + value_folder + "csv/" + "battV-" + dateOfPlot.strftime("%Y%m%d") + ".csv"

i = int(dateOfPlot.strftime("%Y"))
j = int(dateOfPlot.strftime("%m"))
k = int(dateOfPlot.strftime("%d"))
title_date = dateOfPlot.strftime('%d.%m.%Y')
pic_title = dateOfPlot.strftime('%Y-%m-%d')

#csv
with open(filename_csv) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    #dates, highs, rms = [], [], []
    dates, value1 = [], []

    for row in reader:

        current_date = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        dates.append(current_date)

        value = float(row[1])
        value1.append(value)

        #rms1 =  float(row[2])
        #rms.append(rms1)

#locators for x axis
#rcParams['axes.titlepad'] = 15

fig, ax = plt.subplots()
hours = mdates.HourLocator(interval = 2)
h_fmt = mdates.DateFormatter('%H:%M')

#Patches  (this doesn't seem to work in python2.7)
value1_patch = mpatches.Patch(color='red', label='Battery Voltage')
#rms_patch = mpatches.Patch(color='navy', label='no value')

#plt.legend(handles=[peak_patch, rms_patch])
plt.legend(handles=[value1_patch] )

#For a scatter plot use this: ax.scatter(dates, value1, color = 'red', linewidth = 0.1, s=4)
ax.plot(dates, value1, color = 'red', linewidth = 0.5, label='vBatt')  # label added for python2.7
ax.xaxis.set_major_locator(hours)
ax.xaxis.set_major_formatter(h_fmt)

#ax.plot(dates, rms, color = 'navy', linewidth = 0.5)

#minorlocator for quarter of an hour
minor_locator = AutoMinorLocator(8)
ax.xaxis.set_minor_locator(minor_locator)
plt.grid(which='minor', linestyle=':')

#Title,Label
plt.xlabel('Wall Clock Time', fontsize=12)
plt.ylabel('Battery Voltage (volts)', fontsize=12)
plt.title('Battery Discharge Curve for ' + title_date, fontsize=15)
plt.grid(True)

#y axis
plt.ylim (
    ymin = 6,
    ymax = 15
)

#noise limit
#plt.axhline(y=40, color = 'firebrick', linewidth = 0.8)
plt.axhline(y=8.5, color = 'green', linewidth = 0.8, label="15% Capacity Shutdown Limit")


#x axis
plt.xlim(

    xmin = datetime.datetime(i,j,k,0,0,0),
    xmax = datetime.datetime(i,j,k,23,59,0)
)
fig.autofmt_xdate()
fig.set_size_inches(14,10)

plt.legend()   # added for python2.7 ??

# make sure pic folder exists
picfolder = base_folder + value_folder + "pic/"
if not os.path.exists(picfolder):
  os.makedirs(picfolder)
  print(picfolder + " folder created")

#plt.savefig(picfolder + pic_title + '.png', bbox_inches='tight')
plt.savefig(picfolder + pic_title + '.png')