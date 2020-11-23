#!/usr/bin/env python3

# file:  simDataJson.py
#
# Serialize data values to ./simData.json
#
# Methods:
#    saveData(dataname, datavalue, logit=False)   # adds datanaem:datavalue to simData.json file
#    getData(dataname=None)      # either returns dictionary with all values, or just value of passed name
#    delData(dataname)           # delete item from simData.json
#
import sys
import json
import threading
try:
  import sim.simLog as simLog
except:
  import simLog

DEBUG = False

simDataLock = threading.Lock()       # with simDataLock: any operation to make syncronous

sim_simDataDotjson = "sim/simData.json"
simDataDotjson = "simData.json"

def saveData(dataname, datavalue, simDataFile=sim_simDataDotjson, logit=True):


    if DEBUG: print("-- saveData({},{}) called".format(dataname, datavalue))
    with simDataLock:         # prevents two different saveData() at same time
        lsimData = {}

        try:

            lsimData = getData(simDataFile=simDataFile)   # lock assures no one changes this till we are done
            if lsimData == None:
                lsimData = {}
            if DEBUG: print("   simData:", lsimData)
            lsimData[dataname] = datavalue
            if DEBUG: print("   lsimData:",lsimData)

            with open(simDataFile, 'w') as outfile:
                json.dump( lsimData, outfile )
            if DEBUG: print("   simData.json updated")
            if logit: simLog.logger.info("** simData '{}' = {} updated **".format(dataname, datavalue))
        except:
            print("Log:   saveData failed")
            return False

        return True

def delData(dataname, simDataFile=sim_simDataDotjson):
    if DEBUG: print("-- delData('{}') called".format(dataname))

    with simDataLock:
        lsimData = {}
        try:

            lsimData = getData(simDataFile=simDataFile)
            if lsimData == None:
               lsimData = { }
            if DEBUG: print("   lsimData before delete:", lsimData)
            if dataname in lsimData:
                del lsimData[dataname]
                if DEBUG: print("   lsimData after delete:", lsimData)

                with open(simDataFile, 'w') as outfile:
                    json.dump( lsimData, outfile )
                if DEBUG: print("   simData.json updated")
            else:
                if DEBUG: print("   '{}' not found in Data".format(dataname))
        except:
            if DEBUG: print("   delData('{}') failed".dataname)
            return False

        return True


def getData(dataname=None, simDataFile=sim_simDataDotjson):


    if DEBUG: print("-- getData({}) called".format(dataname))
    lsimData = { }
    try:
        with open(simDataFile, 'r') as infile:
            lsimData = json.load(infile)
            if (dataname == None):
                return lsimData
            else:
                return lsimData[dataname]
    except:
        if DEBUG: print("   getData() exception")
        return None

def listData(simDataFile=sim_simDataDotjson):


    if DEBUG: print("-- listData({}) called")
    lsimData = { }
    try:
        with open(simDataFile, 'r') as infile:
            lsimData = json.load(infile)
        for dataname in lsimData:
            print("{}:{}".format(dataname,lsimData[dataname]))
    except:
        if DEBUG: print("   listData() exception")
        return None

def main():

    print("** Starting main()")

    lsimData = getData(simDataFile=simDataDotjson)
    print("   Data: ",lsimData)

    vBatt = 9.6

    if (saveData('vBatt', vBatt, simDataFile=simDataDotjson, logit=True) == True):
        print('   Saved vBatt: {}'.format(vBatt))
    else:
        print("   saveData('vBatt') failed")

    lsimData = getData(simDataFile=simDataDotjson)
    print("   Data: ",lsimData)


    vBatt = float(getData('vBatt',simDataFile=simDataDotjson))
    vBatt -= 0.1

    if (saveData('vBatt', vBatt, simDataFile=simDataDotjson, logit=True) == True):
        print('   Saved vBatt: {}'.format(vBatt))
    else:
        print("   saveData('vBatt') failed")

    lsimData = getData(simDataFile=simDataDotjson)
    print("   Data: ",lsimData)


    if (saveData('nothing',"not important", simDataFile=simDataDotjson,logit=True ) == True):
        print('   Saved nothing: {}'.format("not important"))
    else:
        print("   saveData('nothing') failed")

    lsimData = getData(simDataFile=simDataDotjson)
    print("   Data: ",lsimData)

    if 'nothing' in lsimData:
        print("    nothing entry found in simData - deleting it")
        delData('nothing',simDataFile=simDataDotjson)


    lsimData = getData(simDataFile=simDataDotjson)
    print("   Data: ",lsimData)

    print("Testing listData()")
    listData(simDataFile=simDataDotjson)


if __name__ == "__main__": 
    main()

