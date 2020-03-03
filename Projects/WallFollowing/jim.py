#!/usr/bin/env python3

import easygopigo3
import easysensors
import time

STOP_DISTANCE = 4.0

def follow_wall(egpg):
    #
    print("distance reading: {}".format(egpg.ds.read_inches()))
    while (egpg.ds.read_inches() > STOP_DISTANCE):
        egpg.forward()
        print("distance reading: {}".format(egpg.ds.read_inches()))
        time.sleep(1)
    egpg.stop()


def main():
    egpg = easygopigo3.EasyGoPiGo3()
    egpg.ds = egpg.init_distance_sensor()
    egpg.pan = egpg.init_servo()
    egpg.pan.rotate_servo(90)
    print("OUTA MY WAY! I'm goin' till I can't")
    follow_wall(egpg)
    print("GUESS THAT'S ALL SHE WROTE")


if __name__ == '__main__':
    main()

