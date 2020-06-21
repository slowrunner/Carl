#!/usr/bin/env python3
#
# File: easy_square.py
# Results:  The GoPiGo3 will
#    announce moving in 5 seconds
#    move forward for 18 inches, pause 5 seconds
#    turn 90 right, pause 5 seconds
#    drive forward 12 inches, pause 5 seconds
#    turn 90 right, pause 5 seconds
#    drive forward 12 inches, pause 5 seconds
#    turn 90 right, pause 5 seconds
#    drive forward 12 inches, pause 5 seconds
#    turn 90 right, pause 5 seconds
#    drive backward 6 inches
#


# import the time library for the sleep function
import time
import sys
sys.path.append('/home/pi/Carl/plib')

# import the GoPiGo3 drivers
from my_easygopigo3 import EasyGoPiGo3 

# Create an instance of the GoPiGo3 class.
# GPG will be the GoPiGo3 object.
egpg = EasyGoPiGo3(use_mutex=True)
egpg.set_speed(150)

print("SQUARE TEST will begin in 5 seconds")
time.sleep(5)

print("Driving forward 18 inches")
egpg.drive_inches(18.0)
time.sleep(5)

print("Turning Right 90 degrees")
egpg.turn_degrees(90.0)
time.sleep(5)

print("Driving forward 12 inches")
egpg.drive_inches(12.0)
time.sleep(5)

print("Turning Right 90 degrees")
egpg.turn_degrees(90.0)
time.sleep(5)

print("Driving forward 12 inches")
egpg.drive_inches(12.0)
time.sleep(5)

print("Turning Right 90 degrees")
egpg.turn_degrees(90.0)
time.sleep(5)

print("Driving forward 12 inches")
egpg.drive_inches(12.0)
time.sleep(5)

print("Turning Right 90 degrees")
egpg.turn_degrees(90.0)
time.sleep(5)

print("Driving backward 6 inches")
egpg.drive_inches(-6.0)


print("SQUARE TEST: Done!")
