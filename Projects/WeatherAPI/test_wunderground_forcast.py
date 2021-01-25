#!/usr/bin/env python3

# FILE: test_wunderground_forecast.py

lat="26.5463162"
lon="-80.152788"
zip="33472"

# https://api.weather.com/v3/wx/forecast/daily/5day?geocode=33.74,-84.39&format=json&units=e&language=en-US&apiKey=yourApiKey
url="https://api.weather.com/v3/wx/forecast/daily/5day?geocode={},{}&format=json&units=e&language=en-US&apiKey={}"

import os
import requests
import datetime as dt
import urllib
import json

# wunderground.key must exist with API key to wunderground.com
def main():

	with open('/home/pi/Carl/Projects/WeatherAPI/wunderground.key', 'r') as keyfile:
		key = keyfile.readline()
		key = key.rstrip(os.linesep)   # remove EOL
	url_w_params = url.format(lat,lon,key)
	f = urllib.request.urlopen(url_w_params)
	wx_json = f.read()
	f.close()
	lweather = json.loads(wx_json)
	for i in lweather:
		print("Item - {} : {}".format(i,lweather[i]))


	print("\n****")
	today = lweather['narrative'][0]
	tomorrow = lweather['narrative'][1]
	print("Today: {}".format(today))
	print("Tomorrow: {}".format(tomorrow))
	today1 = today[:today.index('and lows')]
	print("Today1: {}".format(today1))
	today1_test = today1[:today.index('and lows')]
	print("Today1_test: {}".format(today1_test))
"""
	weather_main = lweather['weather'] [0] ['main']
	print("weather_main:",weather_main)
	weather_description = lweather['weather'] [0] ['description']
	print("weather_description:",weather_description)

	main_temp = round(lweather['main']['temp'],0)
	print("main_temp: {:.0f}".format(main_temp))
	main_humidity = lweather['main']['humidity']
	print("main_humidity: {} %".format(main_humidity))
	main_temp_max = round(lweather['main']['temp_max'],0)
	print("High Today: {:.0f}".format(main_temp_max))
	wind_speed = round(lweather['wind']['speed'])
	wind_dir = lweather['wind']['deg']
	wind_gust = lweather['wind']['gust']
	print("Wind {:.0f} from {} degrees, gusts {:.0f}".format(wind_speed,wind_dir,wind_gust))
"""

if __name__ == "__main__": main()
