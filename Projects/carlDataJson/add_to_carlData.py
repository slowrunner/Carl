#!/usr/bin/env python3

# file:  carlDataJson.py
#
# Serialize data values to /home/pi/Carl/carlData.json
#
# Methods:
#    saveCarlData(dataname, datavalue, logit=False)   # adds datanaem:datavalue to carlData.json file
#    getCarlData(dataname=None)      # either returns dictionary with all values, or just value of passed name
#    delCarlData(dataname)           # delete item from carlData.json
#
import sys
sys.path.insert(1,'/home/pi/Carl/plib')
import carlDataJson

def main():
    try:
        print("** add (or update) a value in carlData.json")

        carlDataJson.printCarlData()
        while True:
            key = input("Enter Key: ")
            prompt = "Use key \"{}\" y/n? ".format(key)
            if input(prompt) == "y": break

        while True:
            val = input("Enter Value: ")
            prompt = "Use value \"{}\" y/n? ".format(val)
            if input(prompt) == "y": break


        if (carlDataJson.saveCarlData(key, val) == True):
            print('   Saved {}: {}'.format(key,val))
        else:
            print("   saveCarlData({}) failed".format(key))

        print("\n")
        carlDataJson.printCarlData()

    except KeyboardInterrupt:
        print("\nExiting")



if __name__ == "__main__": 
    main()

