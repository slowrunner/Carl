#!/usr/bin/env python3
#
# File: colors.py
#
# USAGE:
#
#  ./colors.py LEARN	to learn color set
#
#  ./colors.py		to identify known colors
#
# Originally created by CleoQc of Dexter Industries
# https://github.com/CleoQc/GoPiGoColorDetection

from __future__ import print_function
from __future__ import division
from builtins import input

from PIL import Image
import sys
import math
import pprint
from io import BytesIO
from subprocess import call
from time import sleep
from picamera import PiCamera
import atexit
import csv
import os

colors=[]
knowncolors="knowncolors.csv"
tmp_img_name = "tmp.jpg"
small_img_name = "small.jpg"

@atexit.register
def cleanup():
	'''
	cleanup done upon exiting this program
	'''
	camera.close()  # we want the gopigo to stop
	print ("\nGood bye!")

def savecolors(data=colors,path=knowncolors):
	"""
	Write data to a CSV file path
	"""
	with open(path, "w") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		for line in data:
			writer.writerow(line)

def readcolors(data=colors,path=knowncolors):
	'''
	read color definition from CSV file
	'''
	try:
		with open(path,"r") as csv_file:
			reader = csv.reader(csv_file,delimiter=',')
			for row in reader:
				colors.append([row[0],eval(row[1]),eval(row[2])])
	except:
		print("knowncolors.csv not found - creating new empty file.")
		savecolors()

def setupCamera():
	'''
	Setting up camera for use with stream object. Called only once on startup
	'''
	global camera, cmd_beg, cmd_end
	tmp_img_name = "tmp.jpg"
	camera = PiCamera()
	# camera.shutter_speed=3000

	# For dark rooms: uncomment brightness, contrast
	camera.brightness = 70
	camera.contrast = 60

	# For home lighting uncomment awb_mode
	camera.awb_mode = 'incandescent'

	camera.resolution=(1280,720)
	# camera.start_preview()
	saystr=cmd_beg+"Warming_up_the_camera"+cmd_end
	call([saystr], shell=True)
	sleep(5)

def takephoto():
	camera.capture(tmp_img_name)
	im = Image.open(tmp_img_name)
	return (im)

def setupSpeak():
	'''
	setting up espeak-ng. Called once on startup
	'''
	global cmd_beg, cmd_end
	cmd_beg= 'espeak-ng -ven+f1 '
	cmd_end= ' 2>/dev/null' # dumps the std errors to /dev/null

def distance2color(incolor,basecolor):
	'''
	calculate the distance between one rgb tuple and another one
	'''
	return math.sqrt((incolor[0] - basecolor[0])**2 + (incolor[1] - basecolor[1])**2 + (incolor[2] - basecolor[2])**2)

def distance2hsv(incolor,basecolor):
	'''
	calculate the distance between one hue and another hue
	'''
	diff = abs( (incolor[0] - basecolor[0]) )

	# print ("hue difference is {}".format(diff))
	return (diff)

def getrbg(channel):
	'''
	channel is a tuple containing each band.
	Average each band and return as a tuple
	Averages are cast into int as we don't need to be that precise
	'''
	rgb=[]
	avgrgb=[] #average rgb
	for i in range(3):
		rgb.append(list(channel[i].getdata()))
		avgrgb.append(int(sum(rgb[i])/len(rgb[i])))
		# print ("avg rgb:{}".format(avgrgb[i]))
	return (avgrgb[0],avgrgb[1],avgrgb[2])

def gethsv(channel):

	hsv=[]
	avghsv=[] #average hsv
	for i in range(3):
		hsv.append(list(channel[i].getdata()))
		avghsv.append(sum(hsv[i])/(255.0*len(hsv[i])))
		# print ("avg hsv: {}".format(avghsv[i]))
	return ((avghsv[0],avghsv[1],avghsv[2]))

def extract_color(im):
	'''
	extract both average RGB and average HSV from the center of an image.
	1. crop image and only keep center
	2. split image into its bands
	3. average each band through a call to getrgb or gethsv
	4. do the same in HSV format
	'''
	# take the central part which avoids lots of noise
	local_im = im.crop((im.size[0]//4,
				im.size[1]//4,
				im.size[0]*3//4,
				im.size[1]*3//4))

	local_im.save(small_img_name)

	# split into three images, one for each R, G and B
	rgb_channels = local_im.split()

	# split into HSV
	hsv_channels = local_im.convert('HSV').split()

	return(getrbg(rgb_channels),gethsv(hsv_channels))

def addnewcolor(innewcolor):
	'''
	add a new color entry into the colors array
	'''
	colors.append(innewcolor)

def learncolors():
	'''
	1. take a photo
	2. average the color in the middle section of the photo
	3. asks for a name for this color
	4. save new color to color file
	Infinite loop, only way out is Ctrl-C which will call cleanup()
	'''
	readcolors()
	while True:
		try:
			saystr=cmd_beg+"Hold_color_sample_and_Press_enter_key"+cmd_end
			call([saystr], shell=True)
			go = input("Press the Enter key when ready:")
			im = takephoto()
			avgrgb,avghsv = extract_color(im)
			print("I am seeing: ")
			print("RGB: {} and ".format(avgrgb))
			print("Hue: {0[0]:.2f} or {1:.2f}, Saturation: {0[1]:.2f} Value: {0[2]:.2f}. \n".format(avghsv,avghsv[0]*360))

			saystr=cmd_beg+"What_color_was_that?"+cmd_end
			call([saystr], shell=True)
			colorname = input("What name should go with that color? ")
			addnewcolor([colorname.upper(),avgrgb,avghsv])
			savecolors()
			color_img_name = colorname.upper()+'.jpg'
			os.rename(small_img_name, color_img_name)
		except KeyboardInterrupt:
			exit(0)

def identifyrgbname(incolor):
	'''
	return a string containing the name of the color, based on RGB average
	incolor is an rgb tuple
	'''

	studycolor = []  # list of all distances from known colors
	for color in colors:
		rgbBeingEvaluated = color[1]   # rgb tuple
		studycolor.append(distance2color(incolor,rgbBeingEvaluated))

	# print("min rgb distance is {}".format(min(studycolor)))

	return (colors[studycolor.index(min(studycolor))][0])

def identifyhsvname(inhsv):
	'''
	returns a string of the color based on hue, ignoring saturation and value
	inhsv is a HSV tuple
	'''
	studyhsv = []

	# do the average of the Hue band
	for color in colors:
		studyhsv.append(distance2hsv(inhsv,color[2]))

	# print("min hue distance is {}".format(min(studyhsv)))

	return colors[studyhsv.index(min(studyhsv))][0]

def identify_color(im):
	'''
	given a specific image, figure out the average color in that image
	return strings of the color name,
		one for rgb identification
		one for hsv identification (using only the hue)
	'''

	extractedrgb,extractedhsv = extract_color(im)

	rgb_color = identifyrgbname(extractedrgb)
	hsv_color = identifyhsvname(extractedhsv)
	print("RGB:{} HSV:{}".format(rgb_color, hsv_color))
	return (rgb_color, hsv_color)


def findaveragecolor():
	readcolors()
	if colors:
		print ("I know the following colors:")
		for color in colors:
			print (color[0].upper())
	else:
		print("I don't know any colors yet.")
		print("Please teach me some colors by running:")
		print("    python3 colors.py LEARN")
		exit(0)

	lastKnownRgbColor=""
	lastKnownHSVColor=""
	try:
		while True:
			saystr=cmd_beg+"Looking"+cmd_end
			call([saystr], shell=True)
			im = takephoto()
			rgbstr,hsvstr= identify_color(im)
			if rgbstr == hsvstr:
				if hsvstr != lastKnownHSVColor:
					saystr=cmd_beg+"I_see_"+hsvstr.lower()+cmd_end
					print(saystr)
					call([saystr], shell=True)
			else:
				if rgbstr != lastKnownRgbColor or hsvstr != lastKnownHSVColor:
					saystr=cmd_beg+"I_think_it_is_"+hsvstr.lower()+cmd_end
					print(saystr)
					call([saystr], shell=True)
			sleep(3)
			lastKnownRgbColor = rgbstr
			lastKnownHSVColor = hsvstr
	except KeyboardInterrupt:
		exit(0)

if __name__ == '__main__':
	setupSpeak()
	setupCamera()

	if len(sys.argv) == 2 and sys.argv[1].upper() == "LEARN":
		learncolors()
	elif len(sys.argv)==1:
		findaveragecolor()
	else:
		print("Invalid commands")
