#!/usr/bin/env  python3

import sys
sys.path.insert(1,"/home/pi/Carl/plib")

import carlDataJson

# print("carlDataJson contents:")
# lcarlData = carlDataJson.getCarlData()
# for i in lcarlData:
#     print("  ",i," : ",lcarlData[i])

carlDataJson.printCarlData()
