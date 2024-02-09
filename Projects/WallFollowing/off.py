#!/usr/bin/env python3


import wallfollowing
import time

egpg=wallfollowing.init_robot()
wallfollowing.stop(egpg)
wallfollowing.ps_off(egpg)
wallfollowing.say("Servo off and motors stopped")
