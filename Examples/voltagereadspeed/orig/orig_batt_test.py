#!/usr/bin/python3

import sys
from easygopigo3 import EasyGoPiGo3
from time import sleep

mybot = EasyGoPiGo3()

value = 0
count = 0
Reference_Input_Voltage = 12.00

file1 = open("./voltage_test.txt", "a")

def round_up(x, decimal_precision=2):

#  "x" is the value to be rounded using 4/5 rounding rules
#  always rounding away from zero
#
#  "decimal_precision is the number of decimal digits desired
#  after the decimal divider mark.
#
#  It returns the **LESSER** of:
#     (a) The number of digits requested
#     (b) The number of digits in the number if less
#         than the number of decimal digits requested
#     Example:  (Assume decimal_precision = 3)
#         round_up(1.123456, 3) will return 1.123. (4 < 5)
#         round_up(9.876543, 3) will return 9.877. (5 >= 5)
#         round_up(9.87, 3) will return 9.87
#         because there are only two decimal digits and we asked for 3
#
    if decimal_precision < 0:
        decimal_precision = 0

    exp = 10 ** decimal_precision
    x = exp * x

    if x > 0:
        val = (int(x + 0.5) / exp)
    elif x < 0:
        val = (int(x - 0.5) / exp)
    else:
        val = 0
        
    if decimal_precision <= 0:
        return (int(val))
    else:
        return (val)


try:
    while True:
        Measured_Battery_Voltage =  round_up(mybot.get_voltage_battery(), 3)
        Five_v_System_Voltage = round_up(mybot.get_voltage_5v(), 3)
        Measured_voltage_differential =  round_up((Reference_Input_Voltage - Measured_Battery_Voltage),3)
        value = value + Measured_voltage_differential
        count = count+1
        print("Measured Battery Voltage =", Measured_Battery_Voltage)
        print("Measured voltage differential = ", Measured_voltage_differential)
        print("5v system voltage =", Five_v_System_Voltage, "\n")
        print("Total number of measurements so far is ", count)
        sleep(1.00)

except KeyboardInterrupt:
    print("\nThat's All Folks!\n")
    data = ["\nWe took ", str(count), " measurements and the average differential was ", str(round_up(value/count, 3)), "\n(based on an input reference voltage of ", str(Reference_Input_Voltage), ")\n"]
    file1.writelines(data)
    print("We took ", str(count), " measurements and the average differential was ", str(round_up(value/count, 3)), "\n(based on an input reference voltage of ", str(Reference_Input_Voltage), ")\n")
    file1.close()
    sys.exit(0)
