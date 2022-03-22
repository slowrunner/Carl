#!/usr/bin/env python3


import wallfollowing
import time

# wallfollowing.TALK = False
wallfollowing.say("Hello this is a blocking say test with mm and cm")
wallfollowing.say("Hello this is a non-blocking test",blocking=False)
