#!/usr/bin/env python3

# url="http://api.openweathermap.org/data/2.5/weather?zip=33472&units=imperial&wind.direction.name&appid={}"
lat="26.5463162"
lon="-80.152788"
zip="33472"


url="http://api.wunderground.com/api/{}/geolookup/conditions/q/{}.json"

import os
import requests
import datetime as dt
import urllib

# wunderground.key must exist with API key to wunderground.com
def main():

	with open('/home/pi/Carl/Projects/WeatherAPI/wunderground.key', 'r') as keyfile:
		key = keyfile.readline()
		key = key.rstrip(os.linesep)   # remove EOL
		# print("key:" + key + ":")
	url_w_key_zip = url.format(key,zip)
	print("url_w_key_zip:",url_w_key_zip)
	# wx_json = requests.get(url_w_key_zip)
	f = urllib.request.urlopen(url_w_key_zip)
	wx_json = f.read()
	f.close()
	lweather = json.loads(wx_json)
	for i in lweather:
		print("Item - {} : {}".format(i,lweather[i]))

	# today = lweather['daily'][0]['dt']
	# tomorrow = lweather['daily'][1]['dt']
	# print(daily)
	# daily_dt = dt.datetime.fromtimestamp(int(tomorrow))
	# date_str = daily_dt.strftime('%B %d')
	# print(daily_dt)
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
