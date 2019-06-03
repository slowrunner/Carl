#!/usr/bin/env python3

# file:  carlDataJson.py
#
# Serialize data values to /home/pi/Carl/carlData.json
#
# Methods:
#    saveCarlData(dataname, datavalue)   # adds datanaem:datavalue to carlData.json file
#    getCarlData(dataname = None)    # either returns dictionary with all values, or just value of passed name
#
import sys
sys.path.append('/home/pi/Carl/plib')

import json
import threading
import lifeLog

carlDataLock = threading.Lock()       # with carlDataLock: any operation to make syncronous

def saveCarlData(dataname, datavalue):


    # print("-- saveCarlData({},{}) called".format(dataname, datavalue))
    with carlDataLock:         # prevents two different saveCarlData() at same time
        lcarlData = {}

        try:

            lcarlData = getCarlData()   # lock assures no one changes this till we are done
            if lcarlData == None:
                lcarlData = {}
            # print("   carlData:", lcarlData)
            lcarlData[dataname] = datavalue
            # print("   lcarlData:",lcarlData)

            with open('/home/pi/Carl/carlData.json', 'w') as outfile:
                json.dump( lcarlData, outfile )
            # print("   carlData.json updated")
            lifeLog.logger.info("** carlData '{}' = {} updated **".format(dataname, datavalue))
        except:
            # print("   saveCarlData failed")
            return False

        return True

def delCarlData(dataname):
    # print("-- delCarlData({}) called".format(dataname))

    with carlDataLock:
        lcarlData = {}
        try:

            lcarlData = getCarlData()
            if lcarlData == None:
               lcarlData = ()
            # print("   carlData:", lcarlData)
            if dataname in lcarlData: 
                del lcarlData[dataname]
                # print("   lcarlData:", lcarlData)

                with open('/home/pi/Carl/carlData.json', 'w') as outfile:
                    json.dump( lcarlData, outfile )
                # print("   carlData.json updated")
            # else:   print("   {} not found in carlData".format(dataname))
        except:
            # print("   delCarlData{} failed".dataname)
            return False

        return True


def getCarlData(dataname=None):


    # print("-- getCarlData({}) called".format(dataname))

    try:
        with open('/home/pi/Carl/carlData.json', 'r') as infile:
            lcarlData = json.load(infile)
            if (dataname == None):
                return lcarlData
            else:
                return lcarlData[dataname]
    except:
        # print("   getCarlData() except")
        return None

def main():

    print("** Starting main()")

    lcarlData = getCarlData()
    print("   carlData: ",lcarlData)

    chargeCycles = 1

    if (saveCarlData('chargeCycles', chargeCycles) == True):
        print('   Saved chargeCycles: {}'.format(chargeCycles))
    else:
        print("   saveCarlData('chargeCycles') failed")

    lcarlData = getCarlData()
    print("   carlData: ",lcarlData)


    chargeCycles = int(getCarlData('chargeCycles'))
    chargeCycles += 1

    if (saveCarlData('chargeCycles', chargeCycles) == True):
        print('   Saved chargeCycles: {}'.format(chargeCycles))
    else:
        print("   saveCarlData('chargeCycles') failed")


    if 'nothing' in lcarlData:
        delCarlData('nothing')

    if (saveCarlData('nothing',"not important" ) == True):
        print('   Saved nothing: {}'.format("not important"))
    else:
        print("   saveCarlData('nothing') failed")

    lcarlData = getCarlData()
    print("   carlData: ",lcarlData)


if __name__ == "__main__": 
    main()

