#!/usr/bin/env  python3

import sys
import json


def getgpg3_config(dataname=None):


    try:
        with open('/home/pi/Dexter/gpg3_config.json', 'r') as infile:
            lgpg3_config = json.load(infile)
            if (dataname == None):
                return lgpg3_config
            else:
                return lgpg3_config[dataname]
    except Exception as e:
        print("   getgpg3_config() exception:", e)
        return None

def printgpg3_config():
    print("/home/pi/Dexter/gpg3_config.json contents:")
    lgpg3_config = getgpg3_config()
    for i in lgpg3_config:
        print("  ",i," : ",lgpg3_config[i])

printgpg3_config()
