#!/usr/bin/env python3

url="http://api.openweathermap.org/data/2.5/weather?zip=33472&units=imperial&wind.direction.name&appid={}"

import os
import requests

# openweathermap.key must exist with API key to aopenweathermap.org
def main():

	with open('/home/pi/Carl/Projects/WeatherAPI/openweathermap.key', 'r')as keyfile:
		key = keyfile.readline()
		key = key.rstrip(os.linesep)   # remove EOL
		# print("key:" + key + ":")
	url_w_key = url.format(key)
	# print("url_w_key:",url_w_key)
	result = requests.get(url_w_key)
	lweather = result.json()
	for i in lweather:
		print("Item - {} : {}".format(i,lweather[i]))
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


if __name__ == "__main__": main()
