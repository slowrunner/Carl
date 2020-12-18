#!/usr/bin/python3
# print GoPiGo3 battery voltage
# Uses the "no init" version of EasyGoPiGo3() class

import sys
sys.path.append('/home/pi/Carl/plib')

import noinit_easygopigo3
from time import sleep
from statistics import mean
import runLog

egpg = noinit_easygopigo3.EasyGoPiGo3(use_mutex=True, noinit=True)

x = []

for i in [1,2,3]:
    sleep(.005)
    x += [egpg.volt()]
out = mean(x)
if out < 7:
    # runlog.logger.info("vBatt low: {} volts".format(out))
    runlog.entry("vBatt low: {} volts".format(out))
print(out)
