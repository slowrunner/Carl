#!/usr/bin/env python3

"""
## License
 GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
 Copyright (C) 2020  Dexter Industries
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
"""

import queue
import signal
import threading
from math import *
from statistics import mean
from time import sleep
import numpy as np
from curtsies import Input

from my_safe_inertial_measurement_unit import SafeIMUSensor
import myBNO055 as BNO055

from easygopigo3 import *

MINIMUM_VOLTAGE = 8.5
MOTORS_SPEED = 150 # 250 see documentation
PORT = "AD1"  # Use "AD1" or "AD2" for clock-stretching software I2C
ACCEPTED_MINIMUM_BY_DRIVERS = 2.5  # that will move the robot, compass bot used 6 deg
ACCEPTABLE_ERROR = 1.0  # in degrees.  Compass bot used 8 percent not fixed degrees.
ROTATIONAL_FACTOR = 0.30  # amount of heading error to turn before checking again
verbose = False  # set to True for insight into the IMU calls
DEBUG = False    # set to True for debug print messages

def my_turn_degrees(egpg, degrees, blocking=True, timeout = 60):
        """
        TURN_DEGREES with TIMEOUT

        Makes the `GoPiGo3`_ robot turn at a specific angle while staying in the same spot
        :param float degrees: The angle in degress at which the `GoPiGo3`_ has to turn. For rotating the robot to the left, ``degrees`` has to negative, and make it turn to the right, ``degrees`` has to be positive.
        :param boolean blocking = True: Set it as a blocking or non-blocking method.
        ``blocking`` parameter can take the following values:
             * ``True`` so that the method will wait for the `GoPiGo3`_ robot to finish moving.
             * ``False`` so that the method will exit immediately while the `GoPiGo3`_ robot will continue moving.
        :param integer timeout: If blocking is True, and target is not reached after timeout (60) seconds, method will be forced to exit

        In order to better understand what does this method do, let's take a look at the following graphical representation.
        .. image:: ../images/gpg3_robot.svg
        In the image, we have multiple identifiers:
             * The "*heading*": it represents the robot's heading. By default, "rotating" the robot by 0 degrees is going to make the robot stay in place.
             * The "*wheel circle circumference*": this is the circle that's described by the 2 motors moving in opposite direction.
             * The "*GoPiGo3*": the robot we're playing with. The robot's body isn't draw in this representation as it's not the main focus here.
             * The "*wheels*": these are just the `GoPiGo3`_'s wheels - selfexplanatory.

        The effect of this class method is that the `GoPiGo3`_ will rotate in the same spot (depending on ``degrees`` parameter), while the wheels will be describing a perfect circle.
        So, in order to calculate how much the motors have to spin, we divide the *angle* (at which we want to rotate the robot) by 360 degrees and we get a float number between 0 and 1 (think of it as a percentage).
        We then multiply this value with the *wheel circle circumference* (which is the circumference of the circle the robot's wheels describe when rotating in the same place).
        At the end we get the distance each wheel has to travel in order to rotate the robot by ``degrees`` degrees.
        """
        # this is the method to use if you want the robot to turn 90 degrees
        # or any other amount. This method is based on robot orientation
        # and not wheel rotation
        # the distance in mm that each wheel needs to travel
        WheelTravelDistance = ((egpg.WHEEL_BASE_CIRCUMFERENCE * degrees) / 360)

        # the number of degrees each wheel needs to turn
        WheelTurnDegrees = ((WheelTravelDistance / egpg.WHEEL_CIRCUMFERENCE) *
                            360)

        # get the starting position of each motor
        StartPositionLeft = egpg.get_motor_encoder(egpg.MOTOR_LEFT)
        StartPositionRight = egpg.get_motor_encoder(egpg.MOTOR_RIGHT)

        # Set each motor target
        egpg.set_motor_position(egpg.MOTOR_LEFT,
                                (StartPositionLeft + WheelTurnDegrees))
        egpg.set_motor_position(egpg.MOTOR_RIGHT,
                                (StartPositionRight - WheelTurnDegrees))

        if blocking:
            start_time = time.time()
            blocked_duration = 0
            while (blocked_duration < timeout) and egpg.target_reached(
                    StartPositionLeft + WheelTurnDegrees,
                    StartPositionRight - WheelTurnDegrees) is False:
                time.sleep(0.1)
                blocked_duration += time.time() - start_time
                if (DEBUG is True) and (blocked_duration > timeout):
                    print("\n**my_turn_degrees() timeout occurred**")



def orientate(trigger, simultaneous_launcher, sensor_queue):
    """
    Thread-launched function for reading the compass data off of the IMU sensor. The data is then
    interpreted and then it's loaded in a queue.

    :param trigger: CTRL-C event. When it's set, it means CTRL-C was pressed and the thread needs to stop.
    :param simultaneous_launcher: It's a barrier used for synchronizing all threads together.
    :param sensor_queue: Queue where the processed data of the compass is put in.
    :return: Nothing.

    """

    time_to_put_in_queue = 0.2 # measured in seconds
    time_to_wait_after_error = 0.5 # measured in seconds

    # try instantiating an InertialMeasurementUnit object
    # try instantiating a SafeIMUSensor object
    # in the Fusion IMUPLUS operation mode
    #  (Fusion processing using Gyros and Accelerometers only, no mags)

    try:
        # imu = inertial_measurement_unit.InertialMeasurementUnit(bus = "GPG3_AD1")
        print("\nInitializing BNO055 IMU in IMUPLUS mode")
        # Instantiate and Initialize Hardware in IMUPLUS mode
        imu = SafeIMUSensor(port = PORT, mode=BNO055.OPERATION_MODE_IMUPLUS, verbose=verbose)
        print("Resetting IMU for current heading to be 0 degrees\n")
        # resets heading zero direction to current position of the GoPiGo3 bot
        imu.safe_resetBNO055(verbose=verbose)
        imu.safe_axis_remap(verbose=verbose)


    except Exception as msg:
        print(str(msg))
        simultaneous_launcher.abort()

    # The IMU will auto calibrate in the Fusion IMUPLUS operation mode
    # Leaving the NDOF mode calibration here for possible use in an NDOF mode heading_robot
    """
    # start the calibrating process of the compass
    print("Rotate the GoPiGo3 robot with your hand until it's fully calibrated")
    try:
        compass = imu.BNO055.get_calibration_status()[3]
    except Exception as msg:
        compass = 0
    values_already_printed = []
    max_conseq_errors = 3

    while compass != 3 and not trigger.is_set() and max_conseq_errors > 0:
        state = ""
        if compass == 0:
            state = "not yet calibrated"
        elif compass == 1:
            state = "partially calibrated"
        elif compass == 2:
            state = "almost calibrated"

        if not compass in values_already_printed:
            print("The GoPiGo3 is " + state)
        values_already_printed.append(compass)

        try:
            compass = imu.BNO055.get_calibration_status()[3]
        except Exception as msg:
            max_conseq_errors -= 1
            sleep(time_to_wait_after_error)
            continue

    # if CTRL-C was triggered or if the calibration failed
    # then abort everything
    if trigger.is_set() or max_conseq_errors == 0:
        print("IMU sensor is not reacheable or kill event was triggered")
        simultaneous_launcher.abort()
    else:
        # state = "fully calibrated"
        state = "in an auto calibrating mode"
        print("The GoPiGo3 is " + state)
    """


    # point of synchronizing all threads together (including main)
    # it fails if abort method was called
    try:
        simultaneous_launcher.wait()
    except threading.BrokenBarrierError as msg:
        print("[orientate] thread couldn't fully start up")

    # while CTRl-C is not pressed and while the synchronization went fine
    while not (trigger.is_set() or simultaneous_launcher.broken):
        max_conseq_errors = 3
        # Get current heading
        # extract a couple of values before going to the next procedure

        while max_conseq_errors > 0:
            try:
                heading = imu.safe_read_euler()[0]
                print("heading: {:5.1f}".format(heading), end='\r')
                break
            except Exception as msg:
                if DEBUG is True: print("Exception: {}".format(str(msg)))
                max_conseq_errors -= 1
                sleep(time_to_wait_after_error)
                continue

        if max_conseq_errors == 0:
            print("Too many IMU soft errors")
            trigger.set()
            break


        # and then try to put it in the queue
        # if the queue is full, then just go to the next iteration of the while loop
        try:
            sensor_queue.put(heading, timeout = time_to_put_in_queue)
        except queue.Full:
            if DEBUG is True:
                print("Sensor Queue content {}".format(sensor_queue.queue))
            pass


def robotControl(trigger, simultaneous_launcher, motor_command_queue, sensor_queue):
    """
    Thread-launched function for orientating the robot around. It gets commands from the keyboard as well
    as data from the sensor through the sensor_queue queue.

    :param trigger: CTRL-C event. When it's set, it means CTRL-C was pressed and the thread needs to stop.
    :param simultaneous_launcher: It's a barrier used for synchronizing all threads together.
    :param motor_command_queue: Queue containing commands from the keyboard. The commands are read from within main.
    :param sensor_queue: Processed data off of the IMU. The queue is intended to be read.
    :return: Nothing.

    """

    time_to_wait_in_queue = 0.1 # measured in

    # try to connect to the GoPiGo3
    try:
        egpg3_robot = EasyGoPiGo3(use_mutex=True)

        if DEBUG is True:
            print("EasyGoPiGo3.WHEEL_DIAMETER: {} mm,  WHEEL_BASE_WIDTH: {} mm".format(egpg3_robot.WHEEL_DIAMETER, egpg3_robot.WHEEL_BASE_WIDTH))
    except IOError:
        print("GoPiGo3 robot not detected")
        simultaneous_launcher.abort()
    except gopigo3.FirmwareVersionError:
        print("GoPiGo3 board needs to be updated")
        simultaneous_launcher.abort()
    except Exception:
        print("Unknown error occurred while instantiating GoPiGo3")
        simultaneous_launcher.abort()

    # synchronizing point between all threads
    # if abort method was called, then the synch will fail
    try:
        simultaneous_launcher.wait()
    except threading.BrokenBarrierError as msg:
        print("[robotControl] thread couldn't be launched")

    # if threads were successfully synchronized
    # then set the GoPiGo3 appropriately
    if not simultaneous_launcher.broken:
        egpg3_robot.stop()
        egpg3_robot.set_speed(MOTORS_SPEED)

    direction_degrees = None
    move = False
    acceptable_error = ACCEPTABLE_ERROR
    command = "stop"
    rotational_factor = ROTATIONAL_FACTOR
    accepted_minimum_by_drivers = ACCEPTED_MINIMUM_BY_DRIVERS
    last_command = command


    # while CTRL-C is not pressed, the synchronization between threads didn't fail and while the batteries' voltage isn't too low
    while not (trigger.is_set() or simultaneous_launcher.broken or egpg3_robot.volt() <= MINIMUM_VOLTAGE):
        # read from the queue of the keyboard
        try:
            command = motor_command_queue.get(timeout = time_to_wait_in_queue)
            motor_command_queue.task_done()
        except queue.Empty:
            pass

        if (DEBUG is True):
                print("                                                                                     ** RobotComand()  Command: {}".format(command))
                if command != last_command:
                    last_command = command

        # make some selection depending on what every command represents
        if command == "stop":
            move = False
            egpg3_robot.stop()
        # elif command == "move":
        elif command == "fwd":
            move = True
        if command == "270":
            # direction_degrees = -90.0
            direction_degrees = 270.0
        elif command == "90":
            direction_degrees = 90.0
        elif command == "0":
            direction_degrees = 0.0
        elif command == "180":
            direction_degrees = 180.0
        elif  command.isnumeric():
            direction_degrees = int(command)

        # if direction_degrees is set turn toward that heading
        if (move is not True) and (direction_degrees is not None):
            # read data and calculate orientation
            heading = sensor_queue.get()
            heading_diff = direction_degrees - heading
            if (heading_diff > 180):
                heading_diff -= 360.0
            elif (heading_diff < -180):
                heading_diff += 360.0
            # else no correction needed
            error = heading_diff    # will always be -180 to +180
            how_much_to_rotate = heading_diff * rotational_factor

            if (DEBUG is True) and (abs(error) >= acceptable_error):
                print("direction_degrees {:<3.0f} heading {:<3.0f} error {:<3.1f}".format(direction_degrees, heading, error))

            # check if the heading isn't so far from the desired orientation
            # if it needs correction, then rotate the robot
            if abs(error) >= acceptable_error:
                if abs(error) <= (2.0 * accepted_minimum_by_drivers):
                    if DEBUG is True:
                        print("Changing how_much_to_rotate: {} to full error value: {}".format(how_much_to_rotate, error))
                    how_much_to_rotate = error
                if abs(how_much_to_rotate) >= accepted_minimum_by_drivers:
                    if DEBUG is True:
                        print("Turning {:.1f} degrees".format(how_much_to_rotate))
                    my_turn_degrees(egpg3_robot, how_much_to_rotate, blocking = True, timeout = 15)
                else:
                    if DEBUG is True:
                        print("abs(how_much_to_rotate: {}) < accepted_minimum_by_drivers: {}".format(how_much_to_rotate, accepted_minimum_by_drivers))
                        print("Changing how_much_to_rotate to +/- accepted_minimum_by_drivers")
                    how_much_to_rotate = (-1 if how_much_to_rotate < 0 else 1) * accepted_minimum_by_drivers
                    if DEBUG is True:
                        print("Turning {:.1f} degrees".format(how_much_to_rotate))
                    my_turn_degrees(egpg3_robot, how_much_to_rotate, blocking = True, timeout = 5)
            else:
                if DEBUG is True:
                    print("                           ** RobotControl() heading: {} error: {}".format(heading,error),end='\r')

        # command for making the robot move forward or stop
        if move is False:
            egpg3_robot.stop()
        else:
            egpg3_robot.forward()

        sleep(0.001)

    # if the synchronization wasn't broken
    # then stop the motors in case they were running
    if not simultaneous_launcher.broken:
        egpg3_robot.stop()
        if DEBUG is True:
            print("                                    ** RobotControl()  stop() called at end of method")

def Main(trigger):
    """
    Main thread where the other 2 threads are started, where the keyboard is being read and
    where everything is brought together.

    :param trigger: CTRL-C event. When it's set, it means CTRL-C was pressed and all threads are ended.
    :return: Nothing.

    """
    simultaneous_launcher = threading.Barrier(3) # synchronization object
    motor_command_queue = queue.Queue(maxsize = 2) # queue for the keyboard commands
    sensor_queue = queue.Queue(maxsize = 1) # queue for the IMU sensor
    keyboard_refresh_rate = 20.0 # how many times a second the keyboard should update
    available_commands = {"<LEFT>": "270",
                          "<RIGHT>": "90",
                          "<UP>": "0",
                          "<DOWN>": "180",
                          "<SPACE>": "stop",
                          "f": "fwd"} # the selectable options within the menu

    menu_order = ["<LEFT>", "<RIGHT>", "<UP>", "<DOWN>", "<SPACE>", "f"] # and the order of these options

    print("   _____       _____ _  _____         ____  ")
    print("  / ____|     |  __ (_)/ ____|       |___ \ ")
    print(" | |  __  ___ | |__) || |  __  ___     __) |")
    print(" | | |_ |/ _ \|  ___/ | | |_ |/ _ \   |__ < ")
    print(" | |__| | (_) | |   | | |__| | (_) |  ___) |")
    print("  \_____|\___/|_|   |_|\_____|\___/  |____/ ")
    print("                                            ")
    print("   HEADING ROBOT uses BNO055 IMUPLUS mode   ")
    print("        Acceptable Heading Error: {}        ".format(ACCEPTABLE_ERROR))
    print("                                            ")

    # starting the workers/threads
    orientate_thread = threading.Thread(target = orientate, args = (trigger, simultaneous_launcher, sensor_queue))
    robotcontrol_thread = threading.Thread(target = robotControl, args = (trigger, simultaneous_launcher, motor_command_queue, sensor_queue))
    orientate_thread.start()
    robotcontrol_thread.start()

    # if the threads couldn't be launched, then don't display anything else
    try:
        simultaneous_launcher.wait()

        print("Enter a heading and press return")
        print("  or ")
        print("Press the following keys for moving/orientating the robot")
        print("(Press control-c to quit)")

        for menu_command in menu_order:
            print("{:8} - {}".format(menu_command, available_commands[menu_command]))
    except threading.BrokenBarrierError:
        if DEBUG is True:
            print("                         ** main() BrokenBarrierError **")
        pass

    # read the keyboard as long as the synchronization between threads wasn't broken
    # and while CTRL-C wasn't pressed
    build_heading = ""
    building_heading = False
    with Input(keynames = "curtsies") as input_generator:
        while not (trigger.is_set() or simultaneous_launcher.broken):
            period = 1 / keyboard_refresh_rate
            key = input_generator.send(period)
            if DEBUG is True:
                print("                                         [main] key: {}".format(key))
            try:
                if (key != None) and (str(key).isdigit()):
                    building_heading = True
                    build_heading += key
                    print("           Building_heading: {} Press Return to send to robot".format(build_heading),end='\n')
                elif (key != None) and building_heading:
                    # any non-digit signals done building a heading
                    if DEBUG is True: print("build_heading: {}".format(build_heading))
                    if int(str(build_heading)) > 360:
                       print("          built_heading > 360 .. DISCARDING")
                    else:
                        heading_cmd = build_heading
                        print("          Turning to built_heading: {}".format(heading_cmd))
                        try:
                            motor_command_queue.put_nowait(heading_cmd)
                        except queue.Full:
                            pass

                    building_heading = False
                    build_heading = ""
                elif key in available_commands:
                    try:
                        motor_command_queue.put_nowait(available_commands[key])
                    except queue.Full:
                        pass
                # else ignore non-valid key

            except Exception as e:
                print("Building command exception: {}".format(str(e)))
                build_heading = ""
                building_heading = False

    # exit codes depending on the issue
    if simultaneous_launcher.broken:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    trigger = threading.Event() # event used when CTRL-C is pressed
    signal.signal(signal.SIGINT, lambda signum, frame : trigger.set()) # SIGINT (CTRL-C) signal handler
    Main(trigger)
