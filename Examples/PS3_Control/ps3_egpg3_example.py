#!/usr/bin/env python3
########################################################################
# This example controls the GoPiGo3 and using a PS3 Dualshock 3 controller
#
# Based On: https://www.dexterindustries.com/GoPiGo/projects/python-examples-for-the-raspberry-pi/raspberry-pi-ps3-control-with-gopigo-robot-example/
# 		for the original GoPiGo robot
#
# http://www.dexterindustries.com/GoPiGo/
# History
# ------------------------------------------------
# Author     	Date      		Comments
# Alan McDonley 10 Feb 20		Adapted for GoPiGo3
# Karan Nayan   11 July 14		Initial Authoring
'''
## License
 GoPiGo3 for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
 Copyright (C) 2020  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''
#
# left,right,up,down to control
# cross to stop
# left joy to turn the camera servo
# l2 to increase speed
# r2 to decrease speed
########################################################################
from ps3 import *		#Import the PS3 library
import easygopigo3		#Import the EasyGoPiGo3 library



# controller simulator for debugging
class sim_ps3():
	up = False
	left = False
	right = False
	down = False
	cross = False
	l2 = False
	r2 = False
	a_joystick_left_x = 0
	sim_press = 0

	def __init__(self):
		print("init sim PS3")

	def update(self):
		# print("sim_ps3.update()")
		self.sim_press += 1
		self.sim_press = self.sim_press % 7  # legal values 0, 1, 2, 3, 4, 5, 6
		print("sim_press: {}".format(self.sim_press))
		time.sleep(1)
		if self.sim_press == 1:
			self.up = True
			self.cross = False
		elif self.sim_press == 2:
			self.up = False
			self.cross = True
		elif self.sim_press == 3:
			self.down = True
			self.cross = False
		elif self.sim_press == 4:
			self.down  = False
			self.cross = True
		elif self.sim_press == 5:
			self.a_joystick_left_x = 1
			self.cross = False
		elif self.sim_press == 6:
			self.a_joystick_left_x = 0
		else:
			self.up = False
			self.down = False
			self.cross = False


print("Initializing")

# Uncomment/Comment one of next two as appropriate
# p=ps3()		#Create a PS3 object
p=sim_ps3()		#Create a simulated PS3 object


egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
servo = egpg.init_servo()

print("Done")


s=150	#Initialize
run=0   # set to 1 to move bot, set to 0 to test joystick
flag=0
while True:
	if run:
		egpg.set_speed(s)	#Update the speed
	p.update()			#Read the ps3 values
	if p.up:			#If UP is pressed move forward
		if run:
			egpg.forward()
		print("f")
	elif p.left:		#If LEFT is pressed turn left
		if run:
			egpg.left()
			flag=1
		print("l")
	elif p.right:		#If RIGHT is pressed move right
		if run:
			egpg.right()
			flag=1
		print("r")
	elif p.down:		#If DOWN is pressed go back
		if run:
			egpg.backward()
		print("b")
	elif p.cross:		#If CROSS is pressed stop
		if run:
			egpg.stop()
		print("s")
	else:
		if flag:		#If LEFT or RIGHT key was last pressed start moving forward again 
			egpg.forward()
			flag=0
	if p.l2:			#Increase the speed if L2 is pressed
		print(s)
		s+=2
		if s>255:
			s=255
	if p.r2:			#Decrease the speed if R2 is pressed
		print(s)
		s-=2
		if s<0:
			s=0
	x=(p.a_joystick_left_x+1)*90
	print("servo: {}\n".format(int(x)))
	if run:
		servo.rotate_servo(int(x))	#Turn servo a/c to left joy movement
	time.sleep(.01)
