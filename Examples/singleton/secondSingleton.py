#!/usr/bin/env python3

import threading
import time
import traceback
import datetime
from singletonClass import Singleton


# MAIN TEST

def main():
    singleton3=Singleton(execPerSec=2)   # create instance and worker thread

    try:
        while True:
            print("Main2: singleton3.execCounter: {}".format(singleton3.execCounter))
            print("Main2: sleeping for 5 seconds")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nMain2: Cntl-C Detected, calling singleton.cancel()")
        singleton3.cancel()
    except SystemExit:
        print("\nMain2: Singleton Class Test: Bye Bye")
        singleton3.cancel()
    except:
        print("Main2: Exeception Raised")
        singleton3.cancel()
        traceback.print_exc()





if __name__ == "__main__":
    main()


