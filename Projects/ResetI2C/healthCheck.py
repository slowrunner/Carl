#!/usr/bin/env python3


# FILE:  healthCheck.py

# PURPOSE:  Check GoPiGo3 health once per second
#		by polling I2C for Distance Sensor on 0x2A
#		if not seen, force a reset of the GoPiGo3 board
#
#		by checking swap space to be below threshold

import smbus
import time
import psutil

# add Carl's Python library to path
import sys
sys.path.insert(1,"/home/pi/Carl/plib")
import runLog
import lifeLog
import speak
import resetGoPiGo3


bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1
DISTANCE_SENSOR_0x2A = 0x2A

def checkI2C():
	try:
		bus.read_byte(DISTANCE_SENSOR_0x2A)
		i2c_ok = True
	except:
		i2c_ok = False
	return i2c_ok

def checkSwap(threshold=60):
	usage = psutil.swap_memory()[3]
	if usage < threshold:
		swap_ok = True
	else:
		swap_ok = False
	return swap_ok,usage

def print_w_date_time(alert):
	event_time = dt.datetime.now()
	str_event_time = event_time.strftime("%Y-%m-%d %H:%M:%S")
	print("{} {}".format(str_event_time,alert))

@runLog.logRun
def main():
	print("healthCheck.py: Monitoring I2C")

	i2c_was_ok = True  	# presume good at start
	swap_was_ok = True 	# presume good at start
	GoPiGo3_reset = False	# will attempt only once

	while True:
		try:
			if checkI2C() == False:
				if i2c_was_ok:
					i2c_was_ok = False
					alert="I2C Bus Failure Detected"
					lifeLog.logger.info(alert)
					print_w_date_time(alert)
					speak.say(alert)
				if GoPiGo3_reset == False:
					alert="GoPiGo3 reset will be attempted in 30 seconds"
					print_w_date_time(alert)
					speak.say(alert)
					time.sleep(30)
					alert="Attempting GoPiGo3 Board Only reset"
					print_w_date_time(alert)
					speak.say(alert)
					resetSuccess = resetGoPiGo3.fixI2Cjam()
					if resetSuccess:
						alert="Success: GoPiGo3 Board Only Reset"
						print_w_date_time(alert)
						speak.say(alert)
						lifeLog.logger.info(alert)
						# leave GoPiGo3_reset as False
					else:
						alert="Failure: GoPiGo3 Board Only Reset"
						print_w_date_time(alert)
						speak.say(alert)
						lifeLog.logger.info(alert)
						GoPiGo3_reset = True		# only try once if did not fix problem

				else:	# Reset already attempted once
					pass

			elif i2c_was_ok:
				pass	# still good
			else:
				# I2C was down, now good
				alert="I2C Function Restored"
				lifeLog.logger.info(alert)
				print_w_date_time(alert)
				speak.say(alert)
				i2c_was_ok = True

			# SWAP SPACE - need to work out when is good time to reboot - not implemented yet
			swap_ok,usage = checkSwap()
			if swap_ok == False:
				if swap_was_ok:
					swap_was_ok = False
					alert="Swap usage {:.1f} % exceeds {:.0f} % threshold".format(usage,threshold)
					lifeLog.logger.info(alert)
					print_w_date_time(alert)
					speak.say(alert)
				else:
					pass


			time.sleep(1)
		except KeyboardInterrupt:
			print("\nExiting healthCheck.py")
			break

if __name__ == '__main__': main()
