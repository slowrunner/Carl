#!/usr/bin/env python3

"""
FILE: kbd_easygopigo3.py
PURPOSE: Keyboard Controlled GoPiGo3 Class w/Servo Support
USAGE: See / run    kbd_egpg3_run_this.py
BASED ON:  Dexter/Projects/BasicRobotControl

MODIFICATIONS:
- Added servo control keys  4:left 12.5 degrees, 5:center + off, 6:right 12.5 degrees
  (based on my TiltPan class)
- Added status line under logo with WheelDia, WheelBaseWidth, Speed, and Voltage
    e.g.    WD: 64.00  WBW: 114.05  SPD: 150  V: 10.7
- Added methods for Arrow Keys
    Up: fwd 30cm, Dn: bwd 15cm, Left: Spin CCW 90, and Right: Spin CW 90
- Changed <F3> to perform forward 90 degree turn (from one wheel revolution)
- Added  <F5> Clockwise 180 degree spin
- Changed color change key from <INSERT> to <BACKSPACE> (Mac has no insert key)

NOTICES:
GoPiGo3 for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
Copyright (C) 2020  Dexter Industries / Modular Robotics

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
"""

import sys
sys.path.append('/home/pi/Carl/plib')
import random
import my_easygopigo3 as easy
import tiltpan
import threading
from time import sleep

class GoPiGo3WithKeyboard(object):
    """
    Class for interfacing with the GoPiGo3.
    It's functionality is to map different keys
    of the keyboard to different commands of the GoPiGo3.
    """

    KEY_DESCRIPTION = 0
    KEY_FUNC_SUFFIX = 1

    left_blinker_on = False
    right_blinker_on = False

    left_eye_on = False
    right_eye_on = False

    # Speed for keyboarded gopigo3
    SPEED_DPS = 150  # safe and accurate speed is 150, DEFAULT_SPEED is 300, NO_LIMIT_SPEED is 1000

    def __init__(self, use_mutex=True):
        """
        Instantiates the key-bindings between the GoPiGo3 and the keyboard's keys.
        Sets the order of the keys in the menu.
        """
        self.gopigo3 = easy.EasyGoPiGo3(use_mutex=use_mutex)

        # change to a slower default speed
        self.gopigo3.set_speed(self.SPEED_DPS)

        # monkey patch the tiltpan object onto the gopigo3kbd instance
        self.gopigo3.tp = tiltpan.TiltPan(self.gopigo3)

        self.keybindings = {
        "w" : ["Move the GoPiGo3 forward", "forward"],
        "s" : ["Move the GoPiGo3 backward", "backward"],
        "a" : ["Turn the GoPiGo3 to the left", "left"],
        "d" : ["Turn the GoPiGo3 to the right", "right"],
        "<SPACE>" : ["Stop the GoPiGo3 from moving", "stop"],

        "<UP>"    : ["Drive forward for 30 cm", "forward30cm"],
        "<DOWN>"  : ["Drive backward for 15cm", "backward15cm"],
        "<LEFT>"  : ["Spin Left/CCW 90 degrees", "spinCCW90"],
        "<RIGHT>" : ["Spin Right/CW 90 degrees", "spinCW90"],

        "<F1>" : ["Drive forward for 10 cm", "forward10cm"],
        "<F2>" : ["Drive forward for 10 inches", "forward10in"],
        "<F3>" : ["Turn Right 90 degrees (only left wheel rotates)", "forwardturn90"],
        "<F5>" : ["Spin Right/CW 180 degrees", "spinCW180"],

        "1" : ["Turn ON/OFF left blinker of the GoPiGo3", "leftblinker"],
        "2" : ["Turn ON/OFF right blinker of the GoPiGo3", "rightblinker"],
        "3" : ["Turn ON/OFF both blinkers of the GoPiGo3", "blinkers"],

        "4" : ["Rotate Servo Left 12.5 degrees", "servoLeft"],
        "5" : ["Center Servo", "servoCenter"],
        "6" : ["Rotate Servo Right 12.5 degrees", "servoRight"],

        "8" : ["Turn ON/OFF left eye of the GoPiGo3", "lefteye"],
        "9" : ["Turn ON/OFF right eye of the GoPiGo3", "righteye"],
        "0" : ["Turn ON/OFF both eyes of the GoPiGo3", "eyes"],

        "<BACKSPACE>" : ["Change the eyes' color on the go", "eyescolor"],

        "<ESC>" : ["Exit", "exit"],
        }
        self.order_of_keys = ["w", "s", "a", "d", "<SPACE>", "<UP>", "<DOWN>", "<LEFT>", "<RIGHT>", "<F1>", "<F2>", "<F3>", "<F5>", "1", "2", "3", "4", "5", "6", "8", "9", "0", "<BACKSPACE>", "<ESC>"]


    def executeKeyboardJob(self, argument):
        """
        Argument can be any of the strings stored in self.keybindings list.

        For instance: if argument is "w", then the algorithm looks inside self.keybinds dict and finds
        the "forward" value, which in turn calls the "_gopigo3_command_forward" method
        for driving the gopigo3 forward.

        The return values are:
        * "nothing" - when no method could be found for the given argument.
        * "moving" - when the robot has to move forward, backward, to the left or to the right for indefinite time.
        * "path" - when the robot has to move in a direction for a certain amount of time/distance.
        * "static" - when the robot doesn't move in any direction, but instead does static things, such as turning the LEDs ON.
        * "exit" - when the key for exiting the program is pressed.
        """
        method_prefix = "_gopigo3_command_"
        try:
            method_suffix = str(self.keybindings[argument][self.KEY_FUNC_SUFFIX])
        except KeyError:
            method_suffix = ""
        method_name = method_prefix + method_suffix

        method = getattr(self, method_name, lambda : "nothing")

        return method()

    def drawLogo(self):
        """
        Draws the name of the GoPiGo3.
        """
        print("   _____       _____ _  _____         ____  ")
        print("  / ____|     |  __ (_)/ ____|       |___ \ ")
        print(" | |  __  ___ | |__) || |  __  ___     __) |")
        print(" | | |_ |/ _ \|  ___/ | | |_ |/ _ \   |__ < ")
        print(" | |__| | (_) | |   | | |__| | (_) |  ___) |")
        print("  \_____|\___/|_|   |_|\_____|\___/  |____/ ")
        print("                                            ")
        print("  WD:{:> 6.2f}  WBW:{:> 7.2f}  SPD:{:> 4.0f}  V:{:> 4.1f}".format(
                self.gopigo3.WHEEL_DIAMETER, self.gopigo3.WHEEL_BASE_WIDTH, self.gopigo3.get_speed(), self.gopigo3.volt()))
        print("                                            ")

    def drawDescription(self):
        """
        Prints details related on how to operate the GoPiGo3.
        """
        print("\nPress the following keys to run the features of the GoPiGo3.")
        print("To move the motors, make sure you have a fresh set of batteries powering the GoPiGo3.\n")

    def drawMenu(self):
        """
        Prints all the key-bindings between the keys and the GoPiGo3's commands on the screen.
        """
        try:
            for key in self.order_of_keys:
                print("\r[key {:8}] :  {}".format(key, self.keybindings[key][self.KEY_DESCRIPTION]))
        except KeyError:
            print("Error: Keys found GoPiGo3WithKeyboard.order_of_keys don't match with those in GoPiGo3WithKeyboard.keybindings.")

    def _gopigo3_command_forward(self):
        self.gopigo3.forward()

        return "moving"

    def _gopigo3_command_backward(self):
        self.gopigo3.backward()

        return "moving"

    def _gopigo3_command_left(self):
        self.gopigo3.left()

        return "moving"

    def _gopigo3_command_right(self):
        self.gopigo3.right()

        return "moving"

    def _gopigo3_command_stop(self):
        self.gopigo3.stop()

        return "moving"

    def _gopigo3_command_forward10cm(self):
        self.gopigo3.drive_cm(10)

        return "path"

    def _gopigo3_command_forward10in(self):
        self.gopigo3.drive_inches(10)

        return "path"

    def _gopigo3_command_forward30cm(self):
        self.gopigo3.drive_cm(30)

        return "path"

    def _gopigo3_command_backward15cm(self):
        self.gopigo3.drive_cm(-15)

        return "path"

    def _gopigo3_command_forwardturn90(self):
        self.gopigo3.orbit(90,self.gopigo3.WHEEL_BASE_WIDTH/20.0)

        return "path"

    def _gopigo3_command_spinCW90(self):
        self.gopigo3.turn_degrees(90)

        return "path"

    def _gopigo3_command_spinCCW90(self):
        self.gopigo3.turn_degrees(-90)

        return "path"

    def _gopigo3_command_spinCW180(self):
        self.gopigo3.turn_degrees(180)

        return "path"

    def _gopigo3_command_leftblinker(self):
        if self.left_blinker_on is False:
            self.gopigo3.led_on(1)
            self.left_blinker_on = True
        else:
            self.gopigo3.led_off(1)
            self.left_blinker_on = False

        return "static"

    def _gopigo3_command_rightblinker(self):
        if self.right_blinker_on is False:
            self.gopigo3.led_on(0)
            self.right_blinker_on = True
        else:
            self.gopigo3.led_off(0)
            self.right_blinker_on = False

        return "static"

    def _gopigo3_command_blinkers(self):
        if self.left_blinker_on is False and self.right_blinker_on is False:
            self.gopigo3.led_on(0)
            self.gopigo3.led_on(1)
            self.left_blinker_on = self.right_blinker_on = True
        else:
            self.gopigo3.led_off(0)
            self.gopigo3.led_off(1)
            self.left_blinker_on = self.right_blinker_on = False

        return "static"


    def _gopigo3_command_servoLeft(self):
        curAngle = self.gopigo3.tp.get_pan_pos()
        newAngle = curAngle - 12.5
        self.gopigo3.tp.pan(newAngle)

        return "static"

    def _gopigo3_command_servoCenter(self):
        self.gopigo3.tp.center()
        self.gopigo3.tp.off()

        return "static"

    def _gopigo3_command_servoRight(self):
        curAngle = self.gopigo3.tp.get_pan_pos()
        newAngle = curAngle + 12.5
        self.gopigo3.tp.pan(newAngle)

        return "static"


    def _gopigo3_command_lefteye(self):
        if self.left_eye_on is False:
            self.gopigo3.open_left_eye()
            self.left_eye_on = True
        else:
            self.gopigo3.close_left_eye()
            self.left_eye_on = False

        return "static"

    def _gopigo3_command_righteye(self):
        if self.right_eye_on is False:
            self.gopigo3.open_right_eye()
            self.right_eye_on = True
        else:
            self.gopigo3.close_right_eye()
            self.right_eye_on = False

        return "static"

    def _gopigo3_command_eyes(self):
        if self.left_eye_on is False and self.right_eye_on is False:
            self.gopigo3.open_eyes()
            self.left_eye_on = self.right_eye_on = True
        else:
            self.gopigo3.close_eyes()
            self.left_eye_on = self.right_eye_on = False

        return "static"

    def _gopigo3_command_eyescolor(self):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)

        self.gopigo3.set_eye_color((red, green, blue))
        if self.left_eye_on is True:
            self.gopigo3.open_left_eye()
        if self.right_eye_on is True:
            self.gopigo3.open_right_eye()

        return "static"

    def _gopigo3_command_exit(self):
        return "exit"
