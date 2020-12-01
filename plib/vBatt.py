#!/usr/bin/python3
# print GoPiGo3 battery voltage
import easygopigo3
from time import sleep
from statistics import mean
import myconfig
import sys
import runLog

egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
myconfig.setParameters(egpg)

x = []

for i in [1,2,3]:
    sleep(.005)
    x += [egpg.volt()]
out = mean(x)
if out < 7:
    # runlog.logger.info("vBatt low: {} volts".format(out))
    runlog.entry("vBatt low: {} volts".format(out))
print(out)
