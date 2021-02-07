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
import datetime as dt

# add Carl's Python library to path
import sys
sys.path.insert(1,"/home/pi/Carl/plib")
import runLog
import lifeLog
import speak
import resetGoPiGo3
import easygopigo3
import di_sensors.easy_mutex
import leds

bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1

DISTANCE_SENSOR_0x2A = 0x2A
SWAP_THRESHOLD = 60  # percent


# Need an egpg for wifi led blinker to indicate high swap usage
try:
	egpg = easygopigo3.EasyGoPiGo3(use_mutex=True, noinit=True)
except Exception as e:
	print("Exception instantiating EasyGoPiGo3()\n",str(e))
	exit(1)

def checkI2C():
	try:
		di_sensors.easy_mutex.ifMutexAcquire(True)
		bus.read_byte(DISTANCE_SENSOR_0x2A)
		i2c_ok = True
	except:
		i2c_ok = False
	finally:
		di_sensors.easy_mutex.ifMutexRelease(True)
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
	print("healthCheck.py: Monitoring I2C and SWAP")

	i2c_was_ok = True  	# presume good at start
	swap_was_ok = True 	# presume good at start
	GoPiGo3_reset = False	# will attempt only once
	delay_before_reset = 60 # see if I2C down is a glitch

	# Blink WiFi LED to indicate startup
	leds.wifi_blinker_on(egpg,color=leds.GREEN)
	time.sleep(5)
	leds.wifi_blinker_off(egpg)

	while True:
		try:
			if checkI2C() == False:
				if i2c_was_ok:
					i2c_was_ok = False
					alert="I2C Bus Failure Detected"
					lifeLog.logger.info(alert)
					print_w_date_time(alert)
					speak.say(alert)
					glitch_delay = delay_before_reset
					alert = "Initiating {} second wait for I2C recovery".format(glitch_delay)
					print_w_date_time(alert)
					speak.say(alert)
					lifeLog.logger.info(alert)
				if (GoPiGo3_reset == False):
					if (glitch_delay <= 0):
						alert="GoPiGo3 reset will be attempted in 30 seconds"
						print_w_date_time(alert)
						speak.say(alert)
						time.sleep(30)
						alert="Attempting GoPiGo3 Board Only reset"
						print_w_date_time(alert)
						speak.say(alert)
						life.logger.info(alert)
						try:
							resetSuccess = resetGoPiGo3.fixI2Cjam()
						except Exception as e:
							alert = "fixI2Cjam Exception: {}".format(str(e))
							print_w_date_time(alert)
							runLog.entry(alert)
							traceback.print_exc()
							resetSuccess = False
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
					else:  # I2C not OK, reset not performed, delay counter not zero yet
						glitch_delay -= 1
				else:	# I2C down, Reset already attempted once unsuccessfully
					pass	# Hope it comes back by magic

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
			swap_ok,usage = checkSwap(SWAP_THRESHOLD)
			if swap_ok == False:
				if swap_was_ok:
					swap_was_ok = False
					alert="Swap usage {:.1f} % exceeds {:.0f} % threshold".format(usage,SWAP_THRESHOLD)
					lifeLog.logger.info(alert)
					print_w_date_time(alert)
					speak.say(alert)
					leds.wifi_blinker_on(egpg,color=leds.ORANGE)
				else:
					pass


			time.sleep(1)
		except KeyboardInterrupt:
			print("\nExiting healthCheck.py")
			leds.wifi_blinker_off(egpg)
			break

if __name__ == '__main__': main()
