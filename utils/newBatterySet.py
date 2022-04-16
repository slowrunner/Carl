#!/usr/bin/env python3

# FILE:  newBatterySet.py

# PURPOSE: Update carlData.json when battery set is changed

# VALUES AFFECTED:
#   newBatterySetDate  :  2020-08-21
#   newBatterySetAtDocking  :  1454
#   newBatterySetAtLifeHours  :  11870
#   newBatterySetDesc  :  8x Eneloop White 2000 mAh NiMH AA cells




import sys
sys.path.insert(1,'/home/pi/Carl/plib')
import carlDataJson

def main():
    try:
        keys = ["newBatterySetDate", "newBatterySetAtDocking", "newBatterySetAtLifeHours", "newBatterySetDesc"]
        print("New Battery Set Util For carlData.json")

        for key in keys:
            carlDataJson.printCarlData()
            print("\n")
            while True:
                prompt = "Enter new \"{}\" : ".format(key)
                val = input(prompt)
                if val == "":
                    val = carlDataJson.getCarlData(key)
                prompt = "Use value \"{}\" y/n? ".format(val)
                if input(prompt) == "y": break


            if (carlDataJson.saveCarlData(key, val) == True):
                print('   Saved {}: {}'.format(key,val))
            else:
                print("   saveCarlData({}) failed".format(key))

            print("\n")


    except KeyboardInterrupt:
        print("\nExiting")

    finally:
        carlDataJson.printCarlData()


if __name__ == "__main__":
    main()
