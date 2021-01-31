#!/usr/bin/env python3


# FILE:  healthCheck.py

# PURPOSE:  Check GoPiGo3 health once per second
#		by polling I2C for Distance Sensor on 0x2A
#		if not seen, force a reset of the GoPiGo3 board

import smbus
import time

# add Carl's Python library to path
import sys
sys.path.insert(1,"/home/pi/Carl/plib")
import runLog
import lifeLog
import speak

bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1
DISTANCE_SENSOR_0x2A = 0x2A

@runLog.logRun
def checkI2C():
	try:
		bus.read_byte(DISTANCE_SENSOR_0x2A)
		I2C_OK = True
	except:
		I2C_OK = False
		alert="I2C Bus Failure Detected"
		speak.say(alert)
		lifeLog.logger.info(alert)
	return I2C_OK

def main():
	I2C_WAS_OK = True  # presume good at start
	while True:
		try:
			if checkI2C() == False:
				if I2C_WAS_OK:
					print("I2C Failure Detected")
					I2C_WAS_OK = False
				else:
					pass
			elif I2C_WAS_OK:
				pass	# still good
			else:
				# I2C was down, now good
				alert="I2C Function Restored"
				print(alert)
				speak.say(alert)
				I2C_WAS_OK = True
			time.sleep(1)
		except KeyboardInterrupt:
			print("\nExiting healthCheck.py")
			break

if __name__ == '__main__': main()
