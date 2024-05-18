#!/usr/bin/env python3

import gopigo3
import datetime as dt
import time

DT_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
def main():
    try:
        gpg = gopigo3.GoPiGo3()
        lF,lP,lE,lDPS = gpg.get_motor_status(gpg.MOTOR_LEFT)
        rF,rP,rE,rDPS = gpg.get_motor_status(gpg.MOTOR_RIGHT)
        tnow = dt.datetime.now().strftime(DT_FORMAT)
        print_msg="\n{}: lSpeed,rSpeed: ({:.3f},{:.3f}  lEncoder,rEncoder: ({},{})  lPwr,rPwr: ({},{})".format(tnow,lDPS,rDPS,lE,rE,lP,rP)
        print(print_msg)

        while True:
            lF,lP,lE,lDPS = gpg.get_motor_status(gpg.MOTOR_LEFT)
            rF,rP,rE,rDPS = gpg.get_motor_status(gpg.MOTOR_RIGHT)
            tnow = dt.datetime.now().strftime(DT_FORMAT)
            if (abs(rDPS) > 0 or abs(lDPS) > 0):
                print_msg="\n{}: lSpeed,rSpeed: ({:.3f},{:.3f}  lEncoder,rEncoder: ({},{})  lPwr,rPwr: ({},{})".format(tnow,lDPS,rDPS,lE,rE,lP,rP)
                print(print_msg)
                time.sleep(0.01)
                lF,lP,lE,lDPS = gpg.get_motor_status(gpg.MOTOR_LEFT)
                rF,rP,rE,rDPS = gpg.get_motor_status(gpg.MOTOR_RIGHT)
                tnow = dt.datetime.now().strftime(DT_FORMAT)
                print_msg="\n{}: lSpeed,rSpeed: ({:.3f},{:.3f}  lEncoder,rEncoder: ({},{})  lPwr,rPwr: ({},{})".format(tnow,lDPS,rDPS,lE,rE,lP,rP)
                print(print_msg)
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
