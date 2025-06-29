#!/usr/bin/env python3

import easygopigo3
import datetime as dt
import time

DT_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
def main():
    try:
        egpg = easygopigo3.EasyGoPiGo3()
        tnow = dt.datetime.now().strftime(DT_FORMAT)
        print("{}: resetting encoders".format(tnow))
        egpg.reset_encoders()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
