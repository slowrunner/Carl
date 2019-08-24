#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# ######### plotLight.py #############
#
# reads data file passed as parameter e.g. ./plotLight.py logfiles/bv-YYYYmmdd.csv
#         note datafile must be named exactly that format
#
# output: plot of EXIF Brightness Value vs wall clock to ./plots/bv-YYYmmdd-HHMM.png
#

from __future__ import print_function

import sys
import matplotlib
matplotlib.use('Agg')
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import ScalarFormatter
import matplotlib.ticker as ticker
import numpy as np

import csv
import os
import math

from matplotlib import rcParams
from datetime import timedelta, date
import matplotlib.patches as mpatches
from matplotlib.ticker import AutoMinorLocator

if (len(sys.argv) ==2):
    inFile = sys.argv[1]
    print("Input File:       ",inFile)
else:
    print("Usage:  ./plotLight.py logfiles/bv-YYYYmmdd-HHMM.csv")
    exit()

file_date = inFile[(inFile.index('-')+1):inFile.find(".csv")]
#print("file_date",file_date)
dtObj = datetime.datetime.strptime(file_date, '%Y%m%d-%H%M%S')
title_date = dtObj.strftime('%Y-%m-%d %H:%M')
pic_title = dtObj.strftime('bv-%y%m%d-%H%M%S')

#dateOfPlot = date.today()

# 20% capacity voltage limit
#limit_value = 8.1
limit_value = 0

# uncomment next line to plot yesterday's data
#dateOfPlot = date.today() - timedelta(days=1)

dateOfPlot = dtObj.date()
#print("dateOfPlot: ",dateOfPlot)


base_folder = "./"
#value_folder = "logfiles/"
#filename_csv = base_folder + value_folder + "csv/" + "battV-" + dateOfPlot.strftime("%Y%m%d") + ".csv"
filename_csv = base_folder + inFile

i = int(dateOfPlot.strftime("%Y"))
j = int(dateOfPlot.strftime("%m"))
k = int(dateOfPlot.strftime("%d"))
title_date = dtObj.strftime('%d.%m.%Y')
#pic_title = dateOfPlot.strftime('%Y-%m-%d')

#csv
with open(filename_csv) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    #dates, highs, rms = [], [], []
    dates, value1 = [], []

    for row in reader:

        # print("row:",row)
        current_date = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        dates.append(current_date)
        value = float(row[1])
        value1.append(value)

        #rms1 =  float(row[2])
        #rms.append(rms1)

#locators for x axis
#rcParams['axes.titlepad'] = 15

fig, ax = plt.subplots()
plt.yscale('log')
hours = mdates.HourLocator(interval = 2)
h_fmt = mdates.DateFormatter('%H:%M')

ax.yaxis.set_major_formatter(ScalarFormatter())
# ax.yaxis.set_minor_formatter(ScalarFormatter())
# ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
ax.yaxis.set_minor_formatter(ticker.FuncFormatter(lambda y, _: ('{:g}'.format(y))))
#Patches  (this doesn't seem to work in python2.7)
#rms_patch = mpatches.Patch(color='navy', label='no value')
value1_patch = mpatches.Patch(color='red', label='EXIF Brightness Value')
#limit_patch = mpatches.Patch(color='green', label='15% Capacity Limit')

#plt.legend(handles=[peak_patch, rms_patch])
#plt.legend(handles=[value1_patch, limit_patch] )
plt.legend(handles=[value1_patch] )

#For a scatter plot use this: ax.scatter(dates, value1, color = 'red', linewidth = 0.1, s=4)
ax.plot(dates, value1, color = 'red', linewidth = 0.5, label='EXIF Brightness Value')  # label added for python2.7
ax.xaxis.set_major_locator(hours)
ax.xaxis.set_major_formatter(h_fmt)

#ax.plot(dates, rms, color = 'navy', linewidth = 0.5)

#minorlocator for quarter of an hour
minor_locator = AutoMinorLocator(8)
ax.xaxis.set_minor_locator(minor_locator)
plt.grid(which='minor', linestyle=':')

#Title,Label
plt.xlabel('Wall Clock Time', fontsize=12)
plt.ylabel('EXIF Brightness Value', fontsize=12)
plt.title('Brightness Value Curve for ' + title_date, fontsize=15)
plt.grid(True)

# find maximum value
value1max = max(value1)
value1size =len(value1)
# print("value1max: ",value1max," values: ",value1size)
# check value list
#for y in value1:
#  print("y: ",y)

# find minimum value
value1min = min(value1)
if value1min > limit_value:
   ymin_plot = limit_value
else:
   ymin_plot = value1min

#y axis
#plt.ylim (
#    ymin = ymin_plot,
#    ymax = math.ceil(value1max)
#)

#15% capacity limit
#plt.axhline(y=40, color = 'firebrick', linewidth = 0.8)
#plt.axhline(y=limit_value, color = 'green', linewidth = 0.8, label="15% Capacity Shutdown Limit")


#x axis
plt.xlim(

    xmin = datetime.datetime(i,j,k,0,0,0),
    xmax = datetime.datetime(i,j,k,23,59,0)
)
fig.autofmt_xdate()
fig.set_size_inches(14,10)

#plt.legend()   # added for python2.7 ??

# make sure pic folder exists
picfolder = base_folder + "plots/"
if not os.path.exists(picfolder):
  os.makedirs(picfolder)
  print(picfolder + " folder created")

#plt.savefig(picfolder + pic_title + '.png', bbox_inches='tight')
#plt.savefig(picfolder + pic_title + '.png')
pic_file = picfolder + pic_title + '.png'
print("Output Graphic: ",pic_file)
plt.savefig(pic_file)
