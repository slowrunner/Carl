#!/usr/bin/python3
# print GoPiGo3 battery voltage
import easygopigo3

egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
print(egpg.volt())

