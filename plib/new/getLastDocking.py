#!/usr/bin/env python3

# file:  getLastDocking.py
#
# extract last docking log string from /home/pi/Carl/carlData.json
#
import sys
sys.path.append('/home/pi/Carl/plib')

import carlDataJson

print(carlDataJson.getCarlData('lastDocking'))


