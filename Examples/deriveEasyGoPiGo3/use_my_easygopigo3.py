#!/usr/bin/env python3


from my_easygopigo3 import My_EasyGoPiGo3


megpg = My_EasyGoPiGo3(use_mutex=True)              # Intantiate class derived from EasyGoPiGo3 (and GoPiGo3)
ds = megpg.init_distance_sensor()     # EasyGoPiGo3 class method
print("distance sensor: {} cm".format(ds.read()))  # EasyDistanceSensor class method
print("megpg.volt():",megpg.volt())   # EasyGoPiGo3 class method
print("megpg.battery_voltage():",megpg.get_voltage_battery()) # GoPiGo3 class method

#  My_EasyGoPiGo3 class has overloaded forward() method just prints message
megpg.forward()


