#!/usr/bin/env python3

# FILE: weather.py

import os
import requests
import urllib
import json

lat="26.5463162"
lon="-80.152788"
zip="33472"


# openweathermap.key must exist with API key to aopenweathermap.org
current_url="http://api.openweathermap.org/data/2.5/weather?zip=33472&units=imperial&wind.direction.name&appid={}"

# wunderground.key must exist with API key to wunderground.com
current_and_forecast_url="https://api.weather.com/v3/wx/forecast/daily/5day?geocode={},{}&format=json&units=e&language=en-US&apiKey={}"


def forecast():
	result = []
	with open('/home/pi/Carl/Projects/WeatherAPI/wunderground.key', 'r') as keyfile:
		key = keyfile.readline()
		key = key.rstrip(os.linesep)   # remove EOL
	url_w_params = current_and_forecast_url.format(lat,lon,key)
	f = urllib.request.urlopen(url_w_params)
	wx_json = f.read()
	f.close()
	lweather = json.loads(wx_json)

	# print("\n****")
	today = lweather['narrative'][0]
	tomorrow = lweather['narrative'][1]
	# print("Today: {}".format(today))
	# print("Tomorrow: {}".format(tomorrow))
	if 'and lows' in today:
		today = today[:today.index('and lows')]
	if 'and lows' in tomorrow:
		tomorrow = tomorrow[:tomorrow.index('and lows')]
	today_TTS = "Today: {}".format(today)
	# print(today_TTS)
	result.append(today_TTS)

	tomorrow_TTS = "Tomorrow: {}".format(tomorrow)
	# print(tomorrow_TTS)
	result.append(tomorrow_TTS)
	return result

def current():
	result = []
	with open('/home/pi/Carl/Projects/WeatherAPI/openweathermap.key', 'r')as keyfile:
		key = keyfile.readline()
		key = key.rstrip(os.linesep)   # remove EOL
                # print("key:" + key + ":")
	url_w_key = current_url.format(key)
	# print("url_w_key:",url_w_key)
	response = requests.get(url_w_key)
	lweather = response.json()
	# for i in lweather:
	#	print("Item - {} : {}".format(i,lweather[i]))
	weather_header = "Weather Report for {}".format(lweather['name'])
	# print(weather_header)
	result.append(weather_header)

	# weather_main = "Temperature: {:.0f}".format(lweather['weather'] [0] ['main'])
	# print(weather_main)
	# result.append([weather_main])

	weather_description = lweather['weather'] [0] ['description']
	# print(weather_description)
	result.append(weather_description)

	main_temp = "Temperature: {:.0f}".format(round(lweather['main']['temp'],0))
	# print(main_temp)
	result.append(main_temp)

	main_humidity = "Humidity: {} %".format(lweather['main']['humidity'])
	# print(main_humidity)
	result.append(main_humidity)

	wind_speed = round(lweather['wind']['speed'])
	wind_dir = lweather['wind']['deg']
	if 'gust' in lweather['wind']:
		wind_gust = lweather['wind']['gust']
		wind_TTS = "Wind: {:.0f} from {} degrees, gusts: {:.0f}".format(wind_speed,wind_dir,wind_gust)
	else:
		wind_TTS = "Wind: {:.0f} from {} degrees".format(wind_speed,wind_dir)
	# print(wind_TTS)
	result.append(wind_TTS)
	return result



if __name__ == '__main__':
	print("TEST main() weather.py")
	wx_current = current()
	print("weather.current(): ",wx_current)
	wx_forecast = forecast()
	print("weather.forcast(): ",wx_forecast)
