#!/usr/bin/env python3

# file:  getLastDismount.py
#
# extract last dismount log string from /home/pi/Carl/carlData.json
#
import sys
sys.path.append('/home/pi/Carl/plib')

import carlDataJson

print(carlDataJson.getCarlData('lastDismount'))


