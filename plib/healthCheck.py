#!/usr/bin/env python3


# FILE:  healthCheck.py

# PURPOSE:  Check GoPiGo3 health once per second
#		by polling I2C for Distance Sensor on 0x2A
#		if not seen after 1 minute, flash yellow LED
#
#		by checking free memory to be below threshold

import smbus
import time
import psutil
import datetime as dt
import subprocess as sp

# add Carl's Python library to path
import sys
sys.path.insert(1,"/home/pi/Carl/plib")
import runLog
import lifeLog
import speak
# import resetGoPiGo3
import easygopigo3
import di_sensors.easy_mutex
import leds

bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1

DISTANCE_SENSOR_0x2A = 0x2A
MEM_THRESHOLD = 85  # percent
ROUTER_IP = "10.0.0.1"
DELAY_FOR_I2C_RECOVERY = 300

# Need an egpg for wifi led blinker to indicate high mem usage
try:
	egpg = easygopigo3.EasyGoPiGo3(use_mutex=True, noinit=True)
except Exception as e:
	print("Exception instantiating EasyGoPiGo3()\n",str(e))
	exit(1)


# returns 0 if ping succeeds, 1 is ping fails
# default is to check Internet access using the Google name server
def checkIP(ip="8.8.8.8", verbose=False):
	# check once, wait only one second
	status, result = sp.getstatusoutput("ping -c1 -w2 " + ip)
	if verbose:
		if status == 0:
			print_w_date_time("System at {} is Up".format(ip))
		else:
			print_w_date_time("System at {} is Down".format(ip))
	return status


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

def checkMem(threshold=85):
	totalMem = psutil.virtual_memory().total
	freeMem = psutil.virtual_memory().available * 100 / totalMem
	usage = 100 - freeMem
	if usage < threshold:
		mem_ok = True
	else:
		mem_ok = False
	return mem_ok, usage

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
	print_w_date_time("healthCheck.py: Monitoring I2C, Memory, and WiFi")

	i2c_was_ok = checkI2C()  # throw away first check of distance sensor address check
	print_w_date_time("Initial checkI2C() returned {}".format(i2c_was_ok))

	i2c_was_ok = True  	# presume good at start
	mem_was_ok = True 	# presume good at start
	router_was_ok = True	# presume good at start
	verbose = False

	# Blink WiFi LED to indicate startup
	leds.wifi_blinker_on(egpg,color=leds.GREEN)
	time.sleep(5)
	leds.wifi_blinker_off(egpg)
	blinker_cnt = 0		# start with no issue using blinking led

	while True:
		try:
			if checkI2C() == False:
				if i2c_was_ok:
					i2c_was_ok = False
					alert="I2C Bus Failure Detected"
					lifeLog.logger.info(alert)
					print_w_date_time(alert)
					# speak.say(alert)
					glitch_delay = DELAY_FOR_I2C_RECOVERY
					alert = "Initiating {} second watch for I2C recovery".format(glitch_delay)
					print_w_date_time(alert)
					# speak.say(alert)
					lifeLog.logger.info(alert)

				else:	# I2C still down
					if (glitch_delay <= 0):
						alert="I2C not recovered after {} seconds".format(DELAY_FOR_I2C_RECOVERY)
						print_w_date_time(alert)
						lifeLog.logger.info(alert)
						speak.say(alert)
						glitch_delay = DELAY_FOR_I2C_RECOVERY  # start another wait for recovery
						leds.wifi_blinker_on(egpg,color=leds.YELLOW_GREEN)
						blinker_cnt += 1

					else:  # I2C not OK, delay counter not zero yet
						glitch_delay -= 1

			elif i2c_was_ok:
				pass	# still good
			else:
				# I2C was down, now good
				alert="I2C Function Restored"
				lifeLog.logger.info(alert)
				print_w_date_time(alert)
				speak.say(alert)
				i2c_was_ok = True
				blinker_cnt -=1
				if blinker_cnt <= 0: leds.wifi_blinker_off(egpg)

			# mem SPACE - need to work out when is good time to reboot - not implemented yet
			mem_ok,usage = checkMem(MEM_THRESHOLD)
			if mem_ok == False:
				if mem_was_ok:
					mem_was_ok = False
					alert="mem usage {:.1f} % exceeds {:.0f} % threshold".format(usage,MEM_THRESHOLD)
					lifeLog.logger.info(alert)
					print_w_date_time(alert)
					speak.say(alert)
					blinker_cnt +=1
					leds.wifi_blinker_on(egpg,color=leds.ORANGE)
				else:
					pass
			elif mem_was_ok:	# is ok
				pass		# is ok and was ok

			else:   # is ok now but was not ok before
				# Mem was over threshold, now better
				alert="Memory usage {:.0f} % again below {:.0f} % threshold".format(usage,MEM_THRESHOLD)
				lifeLog.logger.info(alert)
				print_w_date_time(alert)
				speak.say(alert)
				mem_was_ok=True
				blinker_cnt -=1
				if blinker_cnt <= 0: leds.wifi_blinker_off(egpg)


			# WiFi - Test if router is visible (don't care about Internet per se) 
			router_not_ok = checkIP(ROUTER_IP,verbose)
			if router_not_ok:  # returns 1 if not reachable
				verbose = True
				if router_was_ok:
					alert="WiFi Router not responding ({})".format(ROUTER_IP)
					lifeLog.logger.info(alert)
					print_w_date_time(alert)

					# Double check
					time.sleep(1)
					router_not_ok = checkIP(ROUTER_IP,verbose)
					if router_not_ok:
						speak.say(alert)
						leds.wifi_blinker_on(egpg,color=leds.TURQUOISE)
						router_was_ok = False
						blinker_cnt += 1
					else:  # already resolved
						verbose = False
				else:  # already alerted - continues
					pass
			elif router_was_ok:
				pass	# still good
			else:
				# Wifi was down, now restored
				verbose = False
				alert="WiFi Router again reachable"
				lifeLog.logger.info(alert)
				print_w_date_time(alert)
				speak.say(alert)
				router_was_ok=True
				blinker_cnt -=1
				if blinker_cnt <= 0: leds.wifi_blinker_off(egpg)

			time.sleep(1)
		except KeyboardInterrupt:
			print("\nExiting healthCheck.py")
			leds.wifi_blinker_off(egpg)
			break

if __name__ == '__main__': main()
