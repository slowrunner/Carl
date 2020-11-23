#!/usr/bin/env python3


# Uncomment import of sim_easygopigo3 or easygopigo3 as appropriate
import sim.easygopigo3 as easygopigo3
# import easygopigo3
from time import sleep
import traceback

def testEachMethod(egpg):

    print("Log: set_robot_constants(66.4)")
    egpg.set_robot_constants(66.6, 116.6)

    print("Log: save_robot_constants()")
    egpg.save_robot_constants()

    print("Log: load_robot_constants()")
    egpg.load_robot_constants()

    print("Log: volt() returns {}v".format(egpg.volt()))

    print("Log: set_speed(150)")
    egpg.set_speed(150)

    print("Log: get_speed() returns {} DPS".format(egpg.get_speed()))

    print("Log: reset_speed()")
    egpg.reset_speed()
    print("Log: get_speed() after reset returns {} DPS".format(egpg.get_speed()))

    print("Log: forward() for 2 seconds")
    egpg.forward()

    sleep(2)

    print("Log: stop()")
    egpg.stop()

    print("Log: egpg.ds.read_mm() returned {} mm".format(egpg.ds.read_mm()))

    print("Log: drive_cm(10.16)")
    egpg.drive_cm(10)

    print("Log: egpg.ds.read_mm() returned {} mm".format(egpg.ds.read_mm()))
    print("Log: egpg.ds.read_inches() returned {} inches".format(egpg.ds.read_inches()))

    print("Log: drive_inches(-4.0)")
    egpg.drive_inches(-4.0)

    print("Log: egpg.ds.read_inches() returned {} inches".format(egpg.ds.read_inches()))


def main():

    print("Log: Starting myRobot.py main()")

    try:
        print("Log: Instantiate EasyGoPiGo3 object")
        egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
        print("Log: Instantiate distance sensor object")
        egpg.ds = egpg.init_distance_sensor()
    except Exception as e:
        print("Log: {}".format(str(e)))
        exit(1)

    try:
        testEachMethod(egpg)
    except Exception as e:
        print("Log: {}".format(str(e)))
        traceback.print_exc()
        exit(1)

    print("Log: End myRobot.py main()")



if __name__ == "__main__":
    main()
