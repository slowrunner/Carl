#!/usr/bin/env python3

# file:  getDockCycle.py
#
# extract dockingcycle value from /home/pi/Carl/carlData.json
#
import sys
sys.path.append('/home/pi/Carl/plib')

import json
import threading
import carlDataJson


dock_cycle = carlDataJson.getCarlData('chargeCycles')
print(dock_cycle)


