#!/usr/bin/env python3
#
# cleanlifelog.py
#
# save life.log to life.log.timestamp
# read ~/Carl/life.log file into list
# starting at next to last line
# loop until "boot logged line"
#    if line is an execution log line: delete it
#    else point to previous line
# write out modified file

import datetime
from shutil import copyfile

dtNow = datetime.datetime.now()

inFileName = "/home/pi/Carl/life.log"
outFileName = "/home/pi/Carl/life.log"
bkupFileName = "/home/pi/Carl/life.log.bkup_"+dtNow.strftime("%Y%m%d_%H%M%S")

# inFileName = "life.log.test"
# outFileName = "life.log.new"
# bkupFileName = "life.log.bkup_"+dtNow.strftime("%Y%m%d_%H%M%S")

copyfile(inFileName, bkupFileName)
changed = False

with open(inFileName) as fIn:
    lineList = fIn.readlines()
print("Read in {}".format(inFileName))
lines = len(lineList)
lineIdx = lines - 1
last = -1
print("lines: {}".format(lines))
print("lastline: {}".format(lineList[last]))
bootlogline = "----- boot -----"
executionlogline = "lifelog.dEmain execution:"

# Find last execution log line before the last boot log line
while ((bootlogline not in lineList[lineIdx]) and (executionlogline not in lineList[lineIdx])):
    lineIdx -= 1

# leave the last execution log line
if (executionlogline in lineList[lineIdx]):
    lineIdx -= 1

while (bootlogline not in lineList[lineIdx]):
    # print("Checking line {}".format(lineIdx+1))
    if (executionlogline in lineList[lineIdx]):
        print("removing: {}".format(lineList[lineIdx]))
        del lineList[lineIdx]
        changed = True
    lineIdx -= 1

if changed == True:
    with open(outFileName,'w') as fOut:
        fOut.writelines(lineList)

    print("Wrote cleaned {}".format(outFileName))
    lines = len(lineList)
    print("lines: {}".format(lines))
    print("lastline: {}".format(lineList[last]))
else:
    print("File not changed")
