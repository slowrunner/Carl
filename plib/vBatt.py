#!/usr/bin/python3
# print GoPiGo3 battery voltage
import easygopigo3
from time import sleep
from statistics import mean
import myconfig

egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
myconfig.setParameters(egpg)

x = []

for i in [1,2,3]:
    sleep(.005)
    x += [egpg.volt()]
print(mean(x))
