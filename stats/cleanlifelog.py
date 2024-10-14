#!/usr/bin/env python3
#
# stats/cleanlifelog.py
#
# PURPOSE: Clean/delete extra execution records from entire life.log
# 
# save life.log to life.log.bak
# read ~/Carl/life.log file into list
# starting at next to last line
# loop until END OF LIFE line marking beginning of file
#     loop until "boot logged line" or "END OF LIFE" line marking begining of file
#        if line is an execution log line: delete it
#        else point to previous line
# write out modified file

import datetime
from shutil import copyfile
import argparse


dtNow = datetime.datetime.now()

inFileName = "life.log"
outFileName = "life.log"
bkupFileName = "life.log.b4clean"

# Uncomment these to test in ~/Carl/Projects/CleanLifeLog/
# inFileName = "life.log"
# outFileName = "life.log.new"
# bkupFileName = "life.log.bak"

# ARGUMENT PARSER
# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--file", required=True, help="path to input file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
# ap.add_argument("-p", "--previous", default=False, action='store_true', help="clean previous boot session")
# args = vars(ap.parse_args())
# print("Started with args:",args)
# clean_previous_session = args['previous']



changed = False

with open(inFileName) as fIn:
    lineList = fIn.readlines()
# print("Read in {}".format(inFileName))
lines = len(lineList)
lineIdx = lines - 1
last = -1
print("lines: {}".format(lines))
print("lastline: {}".format(lineList[last]))
bootlogline = "----- boot -----"
executionlogline = "dEmain execution:"
donelogline = "END OF YEAR"



while (donelogline not in lineList[lineIdx]):       # Loop till done all
    # print("Checking lineIdx {}:{}".format(lineIdx, lineList[lineIdx]))

    # Find last execution log line before the last boot log line  - or stop if neither found
    while ((bootlogline not in lineList[lineIdx]) and \
           (executionlogline not in lineList[lineIdx]) and \
           (donelogline not in lineList[lineIdx]) ):
        lineIdx -= 1

    # print("Checking lineIdx {}:{}".format(lineIdx, lineList[lineIdx]))

    # leave the last execution log line
    if (executionlogline in lineList[lineIdx]):
        lineIdx -= 1


    while ( (bootlogline not in lineList[lineIdx]) and \
            (donelogline not in lineList[lineIdx]) ):

        # print("Checking lineIdx {}:{}".format(lineIdx, lineList[lineIdx]))
        if (executionlogline in lineList[lineIdx]):
            print("removing: {}".format(lineList[lineIdx]))
            del lineList[lineIdx]
            changed = True
        lineIdx -= 1
    lineIdx -= 1

if changed == True:
    # backup the original file before rewriting with changes
    copyfile(inFileName, bkupFileName)
    with open(outFileName,'w') as fOut:
        fOut.writelines(lineList)

    print("Wrote cleaned {}".format(outFileName))
    lines = len(lineList)
    print("lines: {}".format(lines))
    print("lastline: {}".format(lineList[last]))
else:
    print("File not changed")
