#!/usr/bin/env python3

# file:  getChargingState.py
#
# extract chargingState value from /home/pi/Carl/carlData.json
#
import sys
sys.path.append('/home/pi/Carl/plib')

import json
import threading
import carlDataJson
from juicer import printableCS


print(printableCS[carlDataJson.getCarlData('chargingState')])


