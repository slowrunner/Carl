#!/usr/bin/env python3

"""
FILE: subsumption.py

PURPOSE: Implement MR:I2I "Lewis And Clark Program" p314 style
         of [Brooks 84/85/86] Subsumption Architecture For A Mobile Robot

REFERENCES:
    "Mobile Robots: Inspiration To Implementation", Jones, Flynn, Seiger
    https://en.wikipedia.org/wiki/Subsumption_architecture
    https://people.csail.mit.edu/brooks/papers/how-to-build.pdf

ADAPTATIONS:
    The RugWarrior Pro robot had sensors:

    - front located "45 degree cross eyed" IR obstacle detector
      left
      front (left and right)
      right

    - 360 degree bumper that detected contact from
      left
      front (left and right)
      right
      right rear (right and rear)
      rear
      left rear  (left and rear)

   On the GoPiGo3 a single pan servo mounted IR distance sensor
   continuously scans 5 directions:
   - Sets Obstacle Detected:
      left front  (135 degree pan and Distance < 20 cm)
      front       ( 90 degree pan and Distance < 14 cm)
      right front ( 45 degree pan and Distance < 20 cm)

   - Sets "Bumper/Contact" when:
      left        ( 180 degree pan and distance < 5 cm)
      left front  ( 135 degree pan and distance < 5 cm)
      front       (  90 degree pan and distance < 5 cm)
      right front (  45 degree pan and distance < 5 cm)
      right       (   0 degree pan and distance < 5 cm)
"""

import easygopigo3
import easysensors
import time
import sys
import logging
import subprocess
import threading
import numpy
import traceback


SAFE_TURNING_CIRCLE_RADIUS = 20    # cm - safe for GoPiGo3 to turn away if no object within this distance
MIN_TURNING_CIRCLE_RADIUS  =  5    # cm - safe for GoPiGo3 to turn toward objects farther than this distance

BUMP_DISTANCES =     { "front":  5, "right front":  7, "right":  5, "left front":   7, "left":   5 }
OBSTACLE_DISTANCES = { "front": 20, "right front": 28, "right": 20, "left front":  28, "left":  20 }
PAN_ANGLES =         { "front": 90, "right": 0, "right front":  45, "left front": 135, "left": 180 }

TALK = True

CW = 1
CCW = -1


obstacles =         { "front": False, "right front": False, "right":  False, "left front": False, "left": False }
bumps     =         { "front": False, "right front": False, "right":  False, "left front": False, "left": False }

egpg = None   # The EasyGoPiGo3 robot object

tScan = None  # Scan Behavior Thread Object
scan_behavior_active = False
inhibit_scan = False

tMotors = None  # Motor Control Thread Object
motors_behavior_active = False
inhibit_drive = False
mot_trans = 0     # motor translation command
mot_rot = 0    # motor rotation command
MOTORS_RATE = 20

tArbitrate = None  # Motor Arbitration Thread Object
arbitrate_behavior_active = False
inhibit_arbitrate = False
ARBITRATE_RATE = 10    # 50 times per second

tEscape = None  #               Escape Behavior Thread Object
escape_behavior_active = False  # flag indicating escape behavior is active/needed
inhibit_escape = False          # Set true to ignore very close scan readings
escape_trans = 0                # escape active trans percent
escape_rot = 0                  # escape active rotation percent
escape_default_trans = 100      # trans velocity percent
escape_default_rot = 50         # spin velocity percent
escape_trans_time = 1        # forward/backward time
escape_rot_time = 1          # spin in place time
escape_stop_time = 1          # stop duration before any escape maneuver
ESCAPE_RATE = 10		# Check for escape needed roughly 10 times per second


tAvoid = None  #               Avoid Behavior Thread Object
avoid_behavior_active = False  # flag indicating avoid behavior is active/needed
inhibit_avoid = False          # Set true to ignore very close scan readings
avoid_trans = 0                # avoid active trans percent
avoid_rot = 0                  # avoid active rotation percent
avoid_default_trans = 50       # slow a little when avoiding - trans velocity percent
avoid_default_rot = 25         # spin velocity percent
AVOID_RATE = 10		# Check for avoid needed roughly 10 times per second


tCruise = None  #               Cruise Behavior Thread Object
cruise_behavior_active = False  # flag indicating cruise behavior is active/needed
inhibit_cruise = False          # Set true to ignore very close scan readings
cruise_trans = 0                # cruise active trans percent
cruise_rot = 0                  # cruise active rotation percent
cruise_default_trans = 50       # trans velocity percent
CRUISE_RATE = 5		# Check for cruise needed roughly 10 times per second



# ==== UTILITY FUNCTIONS ====

def if_obstacle():
    obstacle_list = []
    for key, value in obstacles.items():
        if value:  obstacle_list += [key]
    return obstacle_list

def if_bump():
    bump_list = []
    for key, value in bumps.items():
        if value:  bump_list += [key]
    return bump_list

def init_robot(ds_port="RPI_1",pan_port="SERVO1"):
    global egpg
    try:
        egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
        egpg.ds = egpg.init_distance_sensor(port=ds_port)
        egpg.pan = egpg.init_servo(port=pan_port)
        msg="Created EasyGoPiGo3 with Distance Sensor on Pan Servo"
        logging.info(msg)
        msg="Created Easy Go Pi Go 3 with Distance Sensor on Pan Servo"
        say(msg)
        return egpg
    except:
        logging.info("Initialization Failure - Cannot Proceed")
        sys.exit(1)

def ps_off():          # turn pan servo off
    global egpg
    # set PWM freq to 0 to stop holding position
    egpg.pan.disable_servo()
    logging.info("Pan Servo Off")

def ps_center():
    global egpg

    egpg.pan.rotate_servo(PAN_ANGLES["front"])
    logging.info("Pan Servo Centered")
    time.sleep(1)

def emergency_stop():
    global egpg

    inhibit_drive = True
    egpg.stop()
    msg="Emergency Stop Requested"
    logging.info(msg)
    say(msg)

def say(phrase,blocking=True):
    if TALK:
        volume="-a{}".format(str(125))  # result "-a125"
        phrase = str(phrase)
        phrase = phrase.replace(' mm', ' millimeters ')
        phrase = phrase.replace(' cm', ' centimeters ')
        # logging.info("Starting say")
        # subprocess.Popen(["/usr/bin/espeak-ng", phrase])
        if blocking:
            subprocess.run(["/usr/bin/espeak-ng","-s150","-ven+f5",volume, phrase])
        else:
            subprocess.Popen(["/usr/bin/espeak-ng","-s150","-ven+f5",volume, phrase])
        # logging.info("Completed say")

def evaluate_scan_reading(direction,distance_reading_cm):
    global obstacles, bumps

    if distance_reading_cm > OBSTACLE_DISTANCES[direction]:
        if obstacles[direction]:
            msg="{} obstacle cleared".format(direction)
            logging.info(msg)
            # say(msg,blocking=False)
            obstacles[direction] = False
        if bumps[direction]:
            msg="{} bump cleared".format(direction)
            logging.info(msg)
            # say(msg,blocking=False)
            bumps[direction] = False
    elif distance_reading_cm > BUMP_DISTANCES[direction]:
        if obstacles[direction] is not True:
            msg="{} obstacle set".format(direction)
            logging.info(msg)
            # say(msg,blocking=False)
            obstacles[direction] = True
        if bumps[direction] is True:
            msg="{} bump cleared".format(direction)
            logging.info(msg)
            bumps[direction] = False
    elif bumps[direction] is not True:
            msg="{} bump set".format(direction)
            logging.info(msg)
            # say(msg,blocking=False)
            bumps[direction] = True
            if obstacles[direction] is not True:
                msg="{} obstacle set".format(direction)
                logging.info(msg)
                obstacles[direction] = True

# Return cw (1), ccw (-1)
def ccw_or_cw(obstacle_list):
    if obstacle_list:
        if ("front left" in obstacle_list) or ("left" in obstacle_list):
            spin = CW
        else:
            spin = CCW
    else:   # empty list
        spin = CCW
    return spin





# ===== BEHAVIORS =======

# BASE BEHAVIOR CLASS

class Behavior(threading.Thread):

    def __init__(self,thread_func):
        threading.Thread.__init__(self)
        self.exitFlag = False               # used to signal behavior to exit
        self.threadFunction = thread_func
        self.exe = None

    def run(self):
        self.exc = None  # var to hold any exception
        self.name = threading.current_thread().name
        try:
            logging.info("Running %s",self.name)
            while (self.exitFlag is not True):
                self.threadFunction()
            logging.info("%s: thread told to exit",self.name)
        except Exception as e:
            logging.info("%s: Printing traceback in the thread exception handler",self.name)
            traceback.print_exc()
            self.exc = e      # save exception for later re-raising to the main

    def join(self):
        threading.Thread.join(self)
        if self.exc:  # re-raise the exception in main
            name = threading.current_thread().name
            logging.info("%s: re-raising exception in thread.join()", name)
            raise self.exc

# END class Behavior

# SCAN BEHAVIOR

# pan servo object is assumed to be at egpg.pan

# For five directions: 1.4s total at 0.05s, 1.5s total at 0.1s dwell, 2s total at 0.2s dwell
SCAN_DWELL = 0.2

def scan_behavior():
        global scan_behavior_active

        try:
            msg="Starting scan behavior"
            logging.info(msg)

            egpg.pan.rotate_servo(PAN_ANGLES["front"])
        except Exception as e:
            msg="Could not center pan servo"
            logging.info(msg)
            say(msg)
            logging.info("Exception {}".format(str(e)))
            tScan.exc = e

        scan_behavior_active = True
        while scan_behavior_active:
            if tScan.exitFlag:
                scan_behavior_active = False
                break

            if inhibit_scan:
                time.sleep(SCAN_DWELL)
                continue

            for direction in PAN_ANGLES:
                angle = PAN_ANGLES[direction]
                try:
                    egpg.pan.rotate_servo(angle)
                except Exception as e:
                    msg="Cound not pan to {} degrees".format(angle)
                    logging.info(msg)
                    logging.info("Exception {}".format(str(e)))
                    scan_behavior_active = False
                    tScan.exc = e

                try:
                    time.sleep(SCAN_DWELL)
                    dist_reading_cm = egpg.ds.read_mm()/10.0  # read() returns whole centimeters so use read_mm()/10.0
                    msg="distance {:>5.0f} cm looking {:<11s} at {:>3d} degrees".format(dist_reading_cm,direction,angle)
                    logging.info(msg)
                    evaluate_scan_reading(direction,dist_reading_cm)


                except Exception as e:
                    msg="Exception reading distance sensor"
                    logging.info(msg)
                    logging.info("Exception {}".format(str(e)))
                    scan_behavior_active = False
                    tScan.exc = e


# END SCAN BEHAVIOR

# MOTORS BEHAVIOR

# inputs:
#   - mot_trans   -100 to +100 percentage of set_speed
#   - mot_rot     -100 (CCW) to +100 (CW) percent of set_speed
def motors_behavior():
        global motors_behavior_active

        motors_behavior_active = True
        current_trans = 0
        current_rot = 0

        logging.info("Starting motors behavior")
        while tMotors.exitFlag is not True:
            time.sleep(1.0/MOTORS_RATE)
            if (mot_trans != current_trans) or (mot_rot != current_rot):
                if mot_rot == 0:
                    right_pct = mot_trans
                    left_pct  = right_pct
                elif mot_trans == 0:
                    right_pct = -1.0 * mot_rot
                    left_pct = mot_rot
                elif numpy.sign(mot_trans) > 0:   # motor_trans is not zero so have to mix,
                    if numpy.sign(mot_rot) > 0:            # mot_trans positive, rotate clockwise
                        right_pct = (mot_trans - mot_rot)
                        left_pct  = mot_trans
                    else:                                  # mot_trans positive, rotate counter-clockwise
                        left_pct = mot_trans - abs(mot_rot)
                        right_pct  = mot_trans
                else:       # mot_trans is not zero and not positive, have to mix
                    if numpy.sign(mot_rot) > 0:            # mot_trans positive, rotate clockwise
                        right_pct = (mot_trans + mot_rot)
                        left_pct  = mot_trans
                    else:                                  # mot_trans positive, rotate counter-clockwise
                        left_pct = mot_trans + abs(mot_rot)
                        right_pct  = mot_trans

                msg="Motors Behavior Interpretation - translate: {}  rotate: {} left: {}% right: {}%".format(mot_trans, mot_rot, left_pct, right_pct)
                logging.info(msg)

                current_trans = mot_trans
                current_rot   = mot_rot

                if inhibit_drive is not True:
                    spd = egpg.get_speed()
                    left_spd = left_pct/100.0 * spd
                    right_spd = right_pct/100.0 * spd
                    egpg.set_motor_dps( egpg.MOTOR_LEFT, left_spd )
                    egpg.set_motor_dps( egpg.MOTOR_RIGHT , right_spd)
                    msg="Motors set - left: {} DPS right: {} DPS".format(left_spd, right_spd)
                    logging.info(msg)
                    motors_behavior_active = (left_pct + right_pct) >  1.0   # if left and right wheel drive is less than 1% no need to be active
                else:
                    logging.info("inhibit_drive True - ignoring command")

        egpg.stop()
        msg="Motors Behavior Exit Flag Detected"
        logging.info(msg)
        say(msg)
        motors_behavior_active = False

# END MOTOR CONTROL BEHAVIOR



# ESCAPE BEHAVIOR


def escape_behavior():
    global escape_behavior_active, escape_trans, escape_rot

    try:
        msg="Starting Escape Behavior Thread"
        logging.info(msg)


        while (tEscape.exitFlag is not True):

            time.sleep(1.0/ESCAPE_RATE)
            if inhibit_escape:
                continue


            bumps_now = if_bump()
            if "front" in bumps_now:           # bumped in front
                escape_behavior_active = True  # alert escape behavior actively needed

                escape_trans = 0               # stop forward motion
                escape_rot = 0                 # stop any rotation

                msg="Requesting Escape From Front Bump"
                logging.info(msg)
                say(msg)

                time.sleep(escape_stop_time)   # wait for stop to occur

                msg="Escape Backup"
                logging.info(msg)
                say(msg)

                escape_trans = -escape_default_trans   # backup up
                escape_rot = 0
                time.sleep(escape_trans_time)  # backup for set time

                msg="Escape Spin"
                logging.info(msg)
                say(msg)

                escape_trans = 0
                obstacles_now = if_obstacle()  # get obstacle list
                # choose clockwise (+1) or counterclockwise (-1) based on obstacle list
                escape_rot = ccw_or_cw(obstacles_now) * escape_default_rot
                time.sleep(escape_rot_time)    # spin for set time

                escape_rot = 0                 # stop spinning
                time.sleep(escape_stop_time)

                escape_trans = escape_default_trans  # drive a little to escape away
                escape_rot = 0
                msg="Escape Forward"
                logging.info(msg)
                say(msg)

                time.sleep(escape_trans_time)

                escape_trans = 0                 # stop escape motion
                escape_behavior_active = False   # we're done escape behavior for now
                msg="Escape From Front Bump Complete"
                logging.info(msg)
                say(msg)



    except Exception as e:
        msg="Exception in escape_behavior"
        logging.info(msg)
        logging.info("Exception {}".format(str(e)))
        escape_behavior_active = False
        tEscape.exc = e

# END ESCAPE BEHAVIOR



# AVOID BEHAVIOR


def avoid_behavior():
    global avoid_behavior_active, avoid_trans, avoid_rot

    try:
        msg="Starting Avoid Behavior Thread"
        logging.info(msg)
        say(msg)


        while (tAvoid.exitFlag is not True):

            time.sleep(1.0/AVOID_RATE)
            if inhibit_avoid:
                continue


            obstacles_now = if_obstacle()
            if obstacles_now:           # something nearing
                avoid_behavior_active = True  # alert avoid behavior actively needed
                avoid_trans = avoid_default_trans
                # choose clockwise (+1) or counterclockwise (-1) based on obstacle list
                avoid_rot = ccw_or_cw(obstacles_now) * avoid_default_rot
                if avoid_rot > 0:
                    msg="avoid left"
                elif avoid_rot < 0:
                    msg="avoid right"
                else: # weird
                    msg="avoid_rot is zero???"
                logging.info(msg)
                say(msg)


            elif avoid_behavior_active:       # no obstacles right now, turn off avoid if active
                avoid_behavior_active = False
                avoid_rot = 0

                msg="avoid done"
                logging.info(msg)
                say(msg)


    except Exception as e:
        msg="Exception in avoid_behavior"
        logging.info(msg)
        logging.info("Exception {}".format(str(e)))
        avoid_behavior_active = False
        tAvoid.exc = e

# END AVOID BEHAVIOR


# CRUISE BEHAVIOR

def cruise_behavior():
    global cruise_behavior_active, cruise_trans, cruise_rot

    try:
        msg="Starting Cruise Behavior Thread"
        logging.info(msg)


        while (tCruise.exitFlag is not True):

            time.sleep(1.0/CRUISE_RATE)
            if inhibit_cruise:
                continue


            cruise_behavior_active = True
            cruise_trans = cruise_default_trans
            cruise_rot = 0

    except Exception as e:
        msg="Exception in cruise_behavior"
        logging.info(msg)
        logging.info("Exception {}".format(str(e)))
        cruise_behavior_active = False
        inhibit_cruse = True
        tCruise.exc = e

# END CRUISE BEHAVIOR


# ARBITRATE BEHAVIOR

def arbitrate_behavior():
    global arbitrate_behavior_active, mot_trans, mot_rot

    try:
        msg="Starting Arbitrate Behavior Thread"
        logging.info(msg)


        while (tArbitrate.exitFlag is not True):
            time.sleep(1.0/ARBITRATE_RATE)

            if inhibit_arbitrate:
                continue


            if escape_behavior_active:
                # logging.info("Setting Escape Commands")
                mot_trans = escape_trans
                mot_rot   = escape_rot
            elif avoid_behavior_active:
                # logging.info("Setting Avoid Commands")
                mot_trans  = avoid_trans
                mot_rot    = avoid_rot
            elif cruise_behavior_active:
                # logging.info("Setting Cruise Commands")
                mot_trans   = cruise_trans
                mot_rot     = cruise_rot
            else:
                # logging.info("Stopping - No Commands")
                mot_trans  = 0
                mot_rot    = 0


    except Exception as e:
        msg="Exception in arbitrate_behavior"
        logging.info(msg)
        logging.info("Exception {}".format(str(e)))
        arbitrate_behavior_active = False
        tArbitrate.exc = e

# END ARBITRATE BEHAVIOR







# SETUP AND TEAR DOWN BEHAVIOR

def setup():
    global egpg, tScan, tMotors, tEscape, tArbitrate, tAvoid, tCruise

    try:
        egpg = init_robot(ds_port="RPI_1", pan_port="SERVO1")

        msg="Subsumption Architecture Setup Initiated"
        logging.info(msg)
        say(msg)

        tScan = Behavior(scan_behavior)
        tScan.start()

        tMotors = Behavior(motors_behavior)
        tMotors.start()

        tArbitrate = Behavior(arbitrate_behavior)
        tArbitrate.start()

        tEscape = Behavior(escape_behavior)
        tEscape.start()

        tAvoid = Behavior(avoid_behavior)
        tAvoid.start()

        tCruise = Behavior(cruise_behavior)
        tCruise.start()

        # wait for everything to initialize and be running
        time.sleep(1)
        msg="Setup complete"
        logging.info(msg)
        say(msg)

    except KeyboardInterrupt:
        logging.info("Keyboard Interrupt in setup")
        raise KeyboardInterrupt

    except Exception as e:
        logging.info("Setup exception: %s",e)


def teardown():
    global tScan
    msg="Tear Down Process Initiated"
    logging.info(msg)
    say(msg)

    try:
        logging.info("Telling scan behavior thread to exit (if still running)")
        tScan.exitFlag = True
        logging.info("Waiting for scan thread to exit")
        tScan.join()
    except Exception as e:
        logging.info("Got exception set in scan thread: %s", e)

    try:
        logging.info("Telling motors behavior thread to exit (if still running)")
        tMotors.exitFlag = True
        logging.info("Waiting for motors thread to exit")
        tMotors.join()
    except Exception as e:
        logging.info("Got exception set in motors thread: %s", e)

    try:
        logging.info("Telling arbitrate behavior thread to exit (if still running)")
        tArbitrate.exitFlag = True
        logging.info("Waiting for arbitrate thread to exit")
        tArbitrate.join()
    except Exception as e:
        logging.info("Got exception set in arbitrate thread: %s", e)

    try:
        logging.info("Telling escape behavior thread to exit (if still running)")
        tEscape.exitFlag = True
        logging.info("Waiting for escape thread to exit")
        tEscape.join()
    except Exception as e:
        logging.info("Got exception set in escape thread: %s", e)

    try:
        logging.info("Telling avoid behavior thread to exit (if still running)")
        tAvoid.exitFlag = True
        logging.info("Waiting for avoid thread to exit")
        tAvoid.join()
    except Exception as e:
        logging.info("Got exception set in avoid thread: %s", e)

    try:
        logging.info("Telling Cruise behavior thread to exit (if still running)")
        tCruise.exitFlag = True
        logging.info("Waiting for Cruise thread to exit")
        tCruise.join()
    except Exception as e:
        logging.info("Got exception set in Cruise thread: %s", e)


    ps_center()
    ps_off()


# MAIN

def main():
    global mot_trans, mot_rot

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

    logging.info("==== SUBSUMPTION ARCHITECTURE MODULE MAIN ====")
    say("Subsumption Architecture Module Main")
    try:
        setup()
        while True:
            # do main things
            time.sleep(1)
    except KeyboardInterrupt:
        print("")
        msg="Ctrl-C Detected in Main"
        logging.info(msg)
        say(msg)

    except Exception as e:
        logging.info("Handling main exception: %s",e)

    finally:
        teardown()
        logging.info("==== Subsumption Module Main Done ====")
        say("Subsumption module main done")


if __name__ == "__main__":
    main()

