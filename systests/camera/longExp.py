#!/usr/bin/python3

# longExpJPG.py  Takes single full resolution image using 6s exposure
#             after 30 sec delay to settle camera
#             writes image to ./images/capture_YYYYmmdd-HHMMSS.jpg

from time import sleep
from datetime import datetime
import sys
sys.path.append("/home/pi/Carl/plib")
import camUtils

fn = camUtils.snapJPG(longexp=True)
print("wrote ",fn)

