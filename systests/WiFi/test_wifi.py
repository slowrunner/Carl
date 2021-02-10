#!/usr/bin/env python3

# FILE:  test_wifi.py

# pings Router and Google Name Server


import subprocess as sp
import time
import datetime as dt
import sys
sys.path.insert(1,"/home/pi/Carl/plib")
import healthCheck


def main():
	while True:
		dtNow = dt.datetime.now()
		print("\n{}".format(dtNow.strftime("%Y-%M-%D %H:%M:%S")))

		ip2check = healthCheck.ROUTER_IP
		print("Checking WiFi Router at {}".format(ip2check))
		r=healthCheck.checkIP(ip2check,verbose=True)
		# print("r: {}".format(r))

		ip2check = "8.8.8.8"
		print("Checking Internet at {}".format(ip2check))
		r=healthCheck.checkIP(ip2check,verbose=True)

		time.sleep(15)


	"""
	ip2check = "10.0.0.99"
	print("Checking not reachable {}".format(ip2check))
	r=healthCheck.checkIP(ip2check)
	# print("r: {}".format(r))
	"""
if __name__ == '__main__': main()
