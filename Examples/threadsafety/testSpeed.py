#!/usr/bin/python3
# test multi-instance affects
import easygopigo3
from time import sleep

egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
egpg.set_speed(150)

while True:
   print("egpg speed: ",egpg.get_speed())
   sleep(10)


