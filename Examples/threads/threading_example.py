#!/usr/bin/env python3

# FILE: threading_example.py

# USAGE: ./thread_example.py

# DOC:  Example creates and starts a single threading class Thing() object
#       The Thing() threading object increments its value2 every time it runs (every 2 seconds)
#       Main() loops reading/printing the thing.value2 every half second
#       If Main() detects a ctrl-c, it tells thread to exit and cleans up
"""
pi@Carl:~/Carl/Examples/threads $ ./threading_example.py 
Thing.__init__ complete
Thing updated value2: 1
Main reading thing - value1: 0 value2: 1
Main reading thing - value1: 0 value2: 1
Main reading thing - value1: 0 value2: 1
Main reading thing - value1: 0 value2: 1
Thing updated value2: 2
Main reading thing - value1: 0 value2: 2
Main reading thing - value1: 0 value2: 2
Main reading thing - value1: 0 value2: 2
Main reading thing - value1: 0 value2: 2
Thing updated value2: 3
Main reading thing - value1: 0 value2: 3
Main reading thing - value1: 0 value2: 3
Main reading thing - value1: 0 value2: 3
^C
ctrl-c detected - telling thing to exit
exitFlag set, stopping thread

"""
import threading
import time


# define a threaded thing class

class Thing (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.value1 = 0
        self.value2 = 0
        self.exitFlag = False
        print("Thing.__init__ complete")

    def run(self):
        while (self.exitFlag is not True):
            self.value2 += 1
            print("Thing updated value2: {}".format(self.value2))
            time.sleep(2)
        print("exitFlag set, stopping thread")


def main():


    # create a thing
    thing = Thing()

    # start the thing
    thing.start()


    while True:
        try:
            print("Main reading thing - value1: {} value2: {}".format(thing.value1, thing.value2))
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nctrl-c detected - telling thing to exit")
            thing.exitFlag = True
            thing.join()
            break

if __name__ == "__main__":
    main()

