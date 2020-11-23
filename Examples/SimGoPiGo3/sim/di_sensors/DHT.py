#!/usr/bin/env bash
def dht(sensor_type=0):
	try:
		import Adafruit_DHT
		if sensor_type==0: #blue sensor
			sensor = Adafruit_DHT.DHT11
		elif sensor_type==1: #white sensor
			sensor = Adafruit_DHT.DHT22
		pin = 15 #connected to the serial port on the GoPiGo, RX pin
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin,retries=3,delay_seconds=.1)
		if humidity is not None and temperature is not None:
			return [temperature,humidity]
		else:
			return [-2.0,-2.0]
	except RuntimeError:
		return [-3.0,-3.0]
		
