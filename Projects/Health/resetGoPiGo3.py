#!/usr/bin/env python3

# FILE: resetGoPiGo3.py

# PURPOSE:  Attempt to clear I2C failure by resetting the GoPiGo3 board
#           (I2C failures have been requiring a total shutdown/hard boot)

import RPi.GPIO as GPIO
import time
import traceback
import datetime as dt

# add Carl's Python library to import path
import sys
sys.path.insert(1,"/home/pi/Carl/plib")
import easygopigo3
import tiltpan
from my_safe_inertial_measurement_unit import SafeIMUSensor
import lifeLog
import runLog

BOARD_PIN_12=12  # Physical Board Pin 12 in GPIO.BOARD mode (GPIO18 in GPIO.BCM mode)
			# is GoPiGo3 RPI_RESET connects through level shifter to AT_RESET


def print_w_date_time(alert):
	event_time = dt.datetime.now()
	str_event_time = event_time.strftime("%Y-%m-%d %H:%M:%S")
	print("{} {}".format(str_event_time,alert))


@runLog.logRun
def fixI2Cjam():
	alert="Forcing GoPiGo3 Board Reset Via GPIO18 To Clear I2C Failure"
	lifeLog.logger.info(alert)
	print_w_date_time(alert)
	try:
		GPIO.setmode(GPIO.BOARD)  # use physical pin numbers

		GPIO.setup(BOARD_PIN_12,GPIO.OUT, pull_up_down=GPIO.PUD_UP)
		time.sleep(0.1)  # allow time for setup to complete

		GPIO.output(BOARD_PIN_12,GPIO.HIGH) 	# Start with normal running mode
		time.sleep(1)

		GPIO.output(BOARD_PIN_12,GPIO.LOW)  	# Yank the AT_RESET chain
		time.sleep(1)  				# Keep it low to ensure reset

		GPIO.output(BOARD_PIN_12,GPIO.HIGH)  	# Let GoPiGo3 run again
		time.sleep(0.5)
	except Exception as e:
		alert="GPIO reset exception: {}".format(str(e))
		runLog.logger.info(alert)
		print_w_date_time(alert)
		traceback.print_exc()
		return False  # unable to fixI2Cjam

	try:
		alert="Attempting Test Instantiation of egpg and sensors")
		runLog.entry(alert)
		print_w_date_time(alert)
		egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)  # FULL INIT needed 
		egpg.imu = SafeIMUSensor(port="AD1", use_mutex=True, init=True)  # I think will have to do the full init
		egpg.tp = tiltpan.TiltPan(egpg)
		egpg.ds = egpg.init_distance_sensor("RPI_1")   # HW I2C
		time.sleep(3)
		test=egpg.ds.read_mm()
		time.sleep(3)
		test=egpg.ds.read_mm()
		time.sleep(3)
		test=egpg.ds.read_mm()
		alert="Distance Sensor Read Attempted: {} mm".format(test)
		runLog.logger.info(alert)
		print_w_date_time(alert)

	except Exception as e:
		alert="Reset appears unsuccssful: {}".format(str(e))
		runLog.logger.info(alert)
		print_w_date_time(alert)
		traceback.print_exc()
		return False  # unable to fixI2Cjam

	runLog.logger.info("GoPiGo3 Board Reset to Clear I2C Failure Completed")
	print("Done")
	return True  # I2Cjam fixed

if __name__ == '__main__':  fixI2Cjam()

