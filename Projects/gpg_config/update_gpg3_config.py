#!/usr/bin/env python3

# file:  update_gpg3_config.py
#
# save new data values to /home/pi/Dexter/gpg3_config.json
#
# Methods:
#
import sys
import json
import os
import threading


# FN = 'gpg3_config.json'
FN = '/home/pi/Dexter/gpg3_config.json'
gpg3_config_DataLock = threading.Lock()       # with carlDataLock: any operation to make syncronous


def save_gpg3_config(lgpg3_config):


    with gpg3_config_DataLock:         # prevents two different saves at same time
        try:

            with open(FN, 'w') as outfile:
                json.dump( lgpg3_config, outfile )
        except:
            print("*** Save %s failed" % FN)
            return False

        return True

def get_gpg3_config(dataname=None):


    try:
        if os.path.exists(FN):
            with open(FN, 'r') as infile:
                lgpg3_config = json.load(infile)
                if (dataname == None):
                    return lgpg3_config
                else:
                    return lgpg3_config[dataname]
        else:
            return {}

    except Exception as e:
        print("   get_gpg3_config() exception:", e)
        return {}

def print_gpg3_config(lgpg3_config):
    if lgpg3_config == None:
        print("%s contents:" % FN)
        lgpg3_config = get_gpg3_config()
    try:
        for i in lgpg3_config:
            print("  ",i," : ",lgpg3_config[i])
    except:
        print("empty")
    print("\n")



def main():
    try:
        lgpg3_config= get_gpg3_config()
        print_gpg3_config(lgpg3_config)
        try:
            key = "wheel-diameter"
            try:
                print("Current %s: %s" % (key, lgpg3_config[key]))
            except:
                print("Current %s: Does Not Exist yet" % key)
            while True:
                val = input("Enter New Value: ")
                if val == "":
                    val = lgpg3_config[key]
                prompt = "Use value \"{}\" y/n? ".format(val)
                if input(prompt) == "y" : break
            lgpg3_config[key] = float(val)
        except:
            pass

        try:
            key = "wheel-base-width"
            try:
                print("\nCurrent %s: %s" % (key, lgpg3_config[key]))
            except:
                print("Current %s: Does Not Exist yet" % key)
            while True:
                val = input("Enter New Value: ")
                if val == "":
                    val = lgpg3_config[key]
                prompt = "Use value \"{}\" y/n? ".format(val)
                if input(prompt) == "y": break
            lgpg3_config[key] = float(val)
        except:
            pass

        try:
            key = "ticks"
            try:
                print("\nCurrent %s: %s" % (key, lgpg3_config[key]))
            except:
                print("Current %s: Does Not Exist yet" % key)
            while True:
                val = input("Enter New Value: ")
                if val == "":
                    val = lgpg3_config[key]
                prompt = "Use value \"{}\" y/n? ".format(val)
                if input(prompt) == "y": break
            lgpg3_config[key] = int(val)
        except:
           pass

        try:
            key = "motor_gear_ratio"
            try:
                print("\nCurrent %s: %s" % (key, lgpg3_config[key]))
            except:
                print("Current %s: Does Not Exist yet" % key)
            while True:
                val = input("Enter New Value: ")
                if val == "":
                    val = lgpg3_config[key]
                prompt = "Use value \"{}\" y/n? ".format(val)
                if input(prompt) == "y": break
            lgpg3_config[key] = int(val)
        except:
            pass



        print("\n*** New gpg3_config.json values:")
        print_gpg3_config(lgpg3_config)

        if save_gpg3_config(lgpg3_config):
            print("Wrote %s" % FN)
        else:
            print("Did not write %s" % FN)

    except KeyboardInterrupt:
        print("\nExiting")



if __name__ == "__main__":
    main()

