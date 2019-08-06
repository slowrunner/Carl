#!/usr/bin/python3

# lowlightJPG.py  Takes single full resolution image using auto exposure
#                after 5 sec delay to settle camera, then boosts brightness
#                writes image to /home/pi/Carl/images/lowlight_YYYYmmdd-HHMMSS.jpg

from datetime import datetime
import sys
sys.path.append("/home/pi/Carl/plib")
import camUtils

filename = "lowlight_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
fn = camUtils.snapJPG(fpath="/home/pi/Carl/images",fname=filename,lowlight=True)
print("wrote ",fn)

