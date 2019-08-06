#!/usr/bin/python3

# longexpJPG.py  Takes single full resolution image using 6s exposure
#                after 30 sec delay to settle camera
#                writes image to ./images/longExp_YYYYmmdd-HHMMSS.jpg

from datetime import datetime
import sys
sys.path.append("/home/pi/Carl/plib")
import camUtils

filename = "longExp_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
fn = camUtils.snapJPG(fpath="/home/pi/Carl/images",fname=filename,longexp=True)
print("wrote ",fn)

