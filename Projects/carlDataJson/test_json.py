#!/usr/bin/env  python3

import sys
sys.path.insert(1,"/home/pi/Carl/plib")

import json
import datetime as dt

# using current time
print("Using current time")
dtNow = dt.datetime.now()
dtNowStr = dtNow.strftime("%Y-%m-%d %H:%M:%S")
print("dtNowStr: {}".format(dtNowStr))
dlist = {}
dlist ["dtNowStr"] = dtNowStr
print("dlist: {}".format(dlist))
with open('test.json', 'w') as outfile:
	json.dump( dlist, outfile)

with open('test.json', 'r') as infile:
	dlist_from_file = json.load(infile)
print("dlist_from_file {}".format(dlist_from_file))
print("dlist_from_file[ \"dtNowStr\" ]:{}".format(dlist_from_file['dtNowStr']))

# using 24 hour time
print("Using a 24 hour time")
dtNow = dt.datetime.strptime("2021-01-16 16:30:01", "%Y-%m-%d %H:%M:%S")
dtNowStr = dtNow.strftime("%Y-%m-%d %H:%M:%S")
print("dtNowStr: {}".format(dtNowStr))
dlist = {}
dlist ["dtNowStr"] = dtNowStr
print("dlist: {}".format(dlist))
with open('test.json', 'w') as outfile:
	json.dump( dlist, outfile)

with open('test.json', 'r') as infile:
	dlist_from_file = json.load(infile)
print("dlist_from_file {}".format(dlist_from_file))
print("dlist_from_file[ \"dtNowStr\" ]:{}".format(dlist_from_file['dtNowStr']))
