#!/usr/bin/env python
#-*- coding: utf-8 -*-

# ######### plotBattLife.py #########
#
# reads data file passed as parameter e.g. ./plotBattLife.py  battV/csv/battV-YYYYmmdd-HHMM.csv
# output: plot of battery voltage vs up time to ./battV/pic/battLife-YYYYmmdd-HHMM.png
#

from __future__ import print_function

import sys
import matplotlib
matplotlib.use('Agg')
import time
import datetime
import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
import numpy as np
import csv
import os
import math

from matplotlib import rcParams
from datetime import timedelta, date
import matplotlib.patches as mpatches
from matplotlib.ticker import AutoMinorLocator


if (len(sys.argv) == 2):
    inFile = sys.argv[1]
    print("Input File: ",inFile)
else:
    print("Usage:  ./plotBattLife.py battV/csv/battV-YYYYmmdd-HHMM.csv")
    exit()

# uncomment a line to plot data
# dateOfPlot = date.today() - timedelta(days=1)
# dateOfPlot = date.today()


base_folder = "./"
value_folder = "battV/"
#filename_csv = base_folder + value_folder + "csv/" + "battV-" + dateOfPlot.strftime("%Y%m%d") + ".csv"
filename_csv = base_folder + inFile



#i = int(dateOfPlot.strftime("%Y"))
#j = int(dateOfPlot.strftime("%m"))
#k = int(dateOfPlot.strftime("%d"))
#title_date = dateOfPlot.strftime('%d.%m.%Y')
file_date = inFile[-17:inFile.find(".csv")]
#print("file_date",file_date)
dtObj= datetime.datetime.strptime(file_date, '%Y%m%d-%H%M')
#print("dtObj:",dtObj)
title_date = dtObj.strftime('%Y-%m-%d %H:%M')
#print("title_date: ",title_date)
pic_title = dtObj.strftime('battLife-%Y%m%d-%H%M')
#print("pic_title: ",pic_title)


#pic_title = dateOfPlot.strftime('%Y-%m-%d')

#csv
with open(filename_csv) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    #dates, highs, rms = [], [], []
    dates, upTime, value1 = [], [], []
    readingCount = 0

    for row in reader:

        current_date = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        dates.append(current_date)
        #print("row:",row)

        value = float(row[1])
        value1.append(value)

        if readingCount == 0:
            upTime.append(0.0)	
        else:
           dtSinceStart = current_date - dates[0]
           upTimeNow = dtSinceStart.days * 24.0 + dtSinceStart.seconds/3600.0
           upTime.append(upTimeNow)
           #print("upTime: ",upTimeNow)   

        #rms1 =  float(row[2])
        #rms.append(rms1)
        readingCount += 1

# analysis
first_datetime = dates[0]
print("First datetime:",first_datetime)
last_datetime = dates[-1]
print("Last datetime:",last_datetime)

life_datetime = last_datetime - first_datetime
life_hours = life_datetime.seconds/3600
life_minutes = (life_datetime.seconds//60)%60
life = life_datetime.days * 24.0 + life_datetime.seconds/3600.0
print("Total Life: %.2f hours" % life )

#locators for x axis
#rcParams['axes.titlepad'] = 15

fig, ax = plt.subplots()
#hours = mdates.HourLocator(interval = 2)
#h_fmt = mdates.DateFormatter('%H:%M')

#Patches  (this doesn't seem to work in python2.7)
#rms_patch = mpatches.Patch(color='navy', label='no value')
value1_patch = mpatches.Patch(color='red', label='Battery Voltage')
limit_patch = mpatches.Patch(color='green', label='45 Minute Reserve')
shutdown_patch = mpatches.Patch(color='blue', label='60s till Shutdown')
#plt.legend(handles=[peak_patch, rms_patch])
plt.legend(handles=[value1_patch, limit_patch, shutdown_patch] )

#For a scatter plot use this: ax.scatter(dates, value1, color = 'red', linewidth = 0.1, s=4)
ax.plot(upTime, value1, color = 'red', linewidth = 0.5, label='vBatt')  # label added for python2.7
#ax.xaxis.set_major_locator(hours)
#ax.xaxis.set_major_formatter(h_fmt)
ax.grid()

#ax.plot(dates, rms, color = 'navy', linewidth = 0.5)

#minorlocator for quarter of an hour
#minor_locator = AutoMinorLocator(8)
#ax.xaxis.set_minor_locator(minor_locator)
#plt.grid(which='minor', linestyle=':')

#Title,Label
plt.xlabel('Up Time', fontsize=12)
plt.ylabel('Battery Voltage (volts)', fontsize=12)
plt.title('Battery Voltage History Beginning ' + title_date, fontsize=15)
plt.grid(True)

# Mark reserve capacity limit determined from a prior total life discharge
limit_value = 8.5
shutdown_value = 7.5
plt.axhline(y=limit_value, color = 'green', linewidth = 0.8, label="45 Minute Reserve")
plt.axhline(y=shutdown_value, color = 'blue', linewidth = 1.5, label="60s Till Shutdown")


# find maximum value
value1max = max(value1)
value1size =len(value1)
# print("value1max: ",value1max," values: ",value1size)
# check value list
#for y in value1:
#  print("y: ",y)

# find minimum value
value1min = min(value1)
if value1min >= shutdown_value:
   ymin_plot = shutdown_value - 0.5
else:
   ymin_plot = value1min

#y axis
plt.ylim (
    ymin = ymin_plot,
    ymax = math.ceil(value1max)
)



#x axis
plt.xlim(

    #xmin = datetime.datetime(i,j,k,0,0,0),
    xmin = 0,
    #xmax = datetime.datetime(i,j,k,23,59,0)
    xmax = math.ceil(life)
)
# fig.autofmt_xdate()
fig.set_size_inches(14,10)

#plt.legend()   # added for python2.7 ??

# make sure pic folder exists
picfolder = base_folder + value_folder + "pic/"
if not os.path.exists(picfolder):
  os.makedirs(picfolder)
  print(picfolder + " folder created")

#plt.savefig(picfolder + pic_title + '.png', bbox_inches='tight')
pic_file = picfolder + pic_title + '.png'
print("Output Graphic: ",pic_file)
plt.savefig(pic_file)
