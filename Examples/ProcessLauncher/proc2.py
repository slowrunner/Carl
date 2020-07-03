#!/usr/bin/env python3

import signal
from time import sleep

def handleSIGTERM(*argv):
    raise SystemExit()
    return

# MAIN

def main():

    signal.signal(signal.SIGTERM,handleSIGTERM)

    try:
        # Do Somthing in a Loop
        keepLooping = True

        while keepLooping:
            # do something
            print("[proc2] executing")
            sleep(1)



    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        print("\n[proc2]*** Ctrl-C detected - Finishing up")
        pass
    except SystemExit:
        # this will get executed after handleSIGTERM
        pass
    finally:
        print("\n[proc2]Finally Executed")


if (__name__ == '__main__'): main()
