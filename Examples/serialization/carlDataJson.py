#!/usr/bin/env python3

# file:  carlDataJson.py
#
# Serialize a value to a file, and deserialize it the next run
#

import json



try:
    with open('carlData.json', 'r') as infile:
        carlData = json.load(infile)
        chargeCycles = carlData['chargeCycles']
        lastPlayHours = float(carlData['lastPlayHours'])
except:
    chargeCycles = 0
    lastPlayHours = 0

print("chargeCycles:",chargeCycles)
print("lastPlayHours:",lastPlayHours)

chargeCycles += 1
lastPlayHours += 0.1
carlData = {
    'lastPlayHours' : "{:.1f}".format(lastPlayHours),
    'chargeCycles'    : chargeCycles
}


with open('carlData.json', 'w') as outfile:
    json.dump( carlData, outfile )

print("saved chargeCycles:", chargeCycles)
print("saved lastPlayHours:", "{:.1f}".format(lastPlayHours))

