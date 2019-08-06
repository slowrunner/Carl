#!/usr/bin/python3

# autoJPG.py     Takes single full resolution image using automatic exposure
#                after 2 sec delay to settle camera
#                writes image to /home/pi/Carl/images/autoexp_YYYYmmdd-HHMMSS.jpg

from datetime import datetime
import sys
sys.path.append("/home/pi/Carl/plib")
import camUtils

filename = "autoexp_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
fn = camUtils.snapJPG(fpath="/home/pi/Carl/images",fname=filename)
print("wrote ",fn)

