#!/usr/bin/env python3

import gopigo3
import datetime as dt
import time

DT_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
def main():
    try:
        gpg = gopigo3.GoPiGo3()
        tnow = dt.datetime.now().strftime(DT_FORMAT)
        print("{}: resetting encoders".format(tnow))
        gpg.reset_motor_encoder(gpg.MOTOR_LEFT + gpg.MOTOR_RIGHT)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
