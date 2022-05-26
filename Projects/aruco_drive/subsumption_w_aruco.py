#!/usr/bin/env python3

"""
FILE: subsumption_w_aruco.py

PURPOSE: Add "Find ArUco Marker", "Drive To ArUco Marker", and "Ready at Dock", to
         [Brooks 84/85/86] Subsumption Architecture For A Mobile Robot

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

from imutils.video import VideoStream
import imutils
import cv2
sys.path.append('/home/pi/Carl/plib/')
import camUtils
import wheellog

SAFE_TURNING_CIRCLE_RADIUS = 20    # cm - safe for GoPiGo3 to turn away if no object within this distance
MIN_TURNING_CIRCLE_RADIUS  =  5    # cm - safe for GoPiGo3 to turn toward objects farther than this distance

BUMP_DISTANCES =     { "front":  5, "right front":  7, "right":  5, "left front":   7, "left":   5 }
OBSTACLE_DISTANCES = { "front": 20, "right front": 28, "right": 20, "left front":  28, "left":  20 }
PAN_ANGLES_5 =         { "front": 90, "right": 0, "right front":  45, "left front": 135, "left": 180 }
PAN_ANGLES_3 =         { "front": 90, "right front":  45, "left front": 135 }
PAN_ANGLE_FRONT =      { "front": 90 }

TALK = False

CW = 1
CCW = -1


obstacles =         { "front": False, "right front": False, "right":  False, "left front": False, "left": False }
bumps     =         { "front": False, "right front": False, "right":  False, "left front": False, "left": False }

egpg = None   # The EasyGoPiGo3 robot object

tScan = None  # Scan Behavior Thread Object
scan_behavior_active = False
inhibit_scan = True
SCAN_DWELL = 0.05
pan_angles = PAN_ANGLES_3
dist_reading_cm = 0		# global holding of latest distance reading

tArUcoSensor = None  # ArUco Sensor Behavior Thread
aruco_sensor_behavior_active = False
inhibit_aruco_sensor = False

tMotors = None  # Motor Control Thread Object
motors_behavior_active = False
inhibit_drive = True
mot_trans = 0     # motor translation command
mot_rot = 0       # motor rotation command
mot_deg = 0       # turn_degrees() command
mot_cm  = 0       # drive_cm() command
MOTORS_RATE = 250

tArbitrate = None  # Motor Arbitration Thread Object
arbitrate_behavior_active = False
inhibit_arbitrate = False
ARBITRATE_RATE = 20    # 50 times per second

tEscape = None  #               Escape Behavior Thread Object
escape_behavior_active = False  # flag indicating escape behavior is active/needed
inhibit_escape = True           # Set true to ignore very close scan readings
escape_trans = 0                # escape active trans percent
escape_rot = 0                  # escape active rotation percent
escape_deg = 0                  # escape active turn degrees
escape_cm  = 0                  # escape active drive cm
escape_default_trans = 50       # trans velocity percent
escape_default_rot = 50         # spin velocity percent
escape_trans_time = 0.5           # forward/backward time
escape_rot_time = 1             # spin in place time
escape_stop_time = 1            # stop duration before any escape maneuver
ESCAPE_RATE = 15		# Check for escape needed roughly 10 times per second


tAvoid = None  #               Avoid Behavior Thread Object
avoid_behavior_active = False  # flag indicating avoid behavior is active/needed
inhibit_avoid = True           # Set true to ignore very close scan readings
avoid_trans = 0                # avoid active trans percent
avoid_rot = 0                  # avoid active rotation percent
avoid_deg = 0                  # avoid active turn degrees
avoid_cm  = 0                  # avoid active drive cm
avoid_default_trans = 50       # slow a little when avoiding - trans velocity percent
avoid_default_rot = 25         # spin velocity percent
AVOID_RATE = 10		# Check for avoid needed roughly 10 times per second


tCruise = None  #               Cruise Behavior Thread Object
cruise_behavior_active = False  # flag indicating cruise behavior is active/needed
inhibit_cruise = True           # Set true to not let cruise behavior take charge
cruise_trans = 0                # cruise active trans percent
cruise_rot = 0                  # cruise active rotation percent
cruise_deg = 0                  # cruise active turn degrees
cruise_cm  = 0                  # cruise active drive cm
cruise_default_trans = 50       # trans velocity percent
CRUISE_RATE = 5		# Check for cruise needed roughly 10 times per second

tArUcoDrive = None              # ArUco Drive Behavior Thread Object
aruco_drive_behavior_active = False  # flag indicating behavior is active/needed
inhibit_aruco_drive = True          # Set true to prohibit behavior
aruco_drive_trans = 0                # active trans percent
aruco_drive_rot = 0                  # active rotation percent
aruco_drive_deg = 0                  # active turn degrees
aruco_drive_cm  = 0                  # active drive cm
aruco_drive_default_trans = 50       # trans velocity percent
ARUCO_DRIVE_RATE = 5           # Check for aruco drive needed times per second
MARKER_AHEAD_PIXEL = 269        # Drive straight forward for this marker cX
DOCKING_READY_DIST = 44         # Stop when facing dock at this distance

tArUcoFind = None              # ArUco Find Behavior Thread Object
aruco_find_behavior_active = False  # flag indicating behavior is active/needed
inhibit_aruco_find = True          # Set true to prohibit behavior
aruco_find_trans = 0                # active trans percent
aruco_find_rot = 0                  # active rotation percent
aruco_find_deg = 0                  # active turn degrees
aruco_find_cm  = 0                  # active drive cm
aruco_find_default_rot = 10         # trans velocity percent
ARUCO_FIND_RATE = 3           # Check for aruco drive needed times per second
ARUCO_FIND_SCAN_TIME = 60     # search for 60 seconds
HALF_FOV_X_PIXELS = 320  # center of 640x480 image

tArUcoSensor = None              # ArUco Sensor Behavior Thread Object
aruco_sensor_behavior_active = False  # flag indicating behavior is active/needed
inhibit_aruco_sensor = False          # Set true to prohibit behavior
ARUCO_SENSOR_RATE = 5           # Check for aruco drive needed times per second
aruco_markers = []              # list of markers (markerID, cX, cY)
DISPLAY_MARKERS = False         # if X-server available can set True to see markers

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

def if_marker():
    return aruco_markers

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

    egpg.pan.rotate_servo(pan_angles["front"])
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

def scan_behavior():
        global scan_behavior_active, dist_reading_cm

        try:
            msg="Starting scan behavior"
            logging.info(msg)

            egpg.pan.rotate_servo(pan_angles["front"])
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

            for direction in pan_angles:
                angle = pan_angles[direction]
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
                    # logging.info(msg)
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
#   - mot_deg     +/= degrees to turn (non-blocking)
#   - mot_cm      +/- cm to drive (non-blocking)

def motors_behavior():
        global motors_behavior_active, mot_deg, mot_cm

        motors_behavior_active = True
        current_trans = 0
        current_rot = 0
        current_deg = 0
        current_cm  = 0
        sim_start_time = None

        logging.info("Starting motors behavior")
        while tMotors.exitFlag is not True:
            time.sleep(1.0/MOTORS_RATE)
            if (current_deg != 0):      # active in turn_degrees
                logging.info("Motors Behavior: Active in turn_degrees")
                if (mot_deg == 0):          # early stop request
                    logging.info("Motors Behavior Early Stop of turn_degrees")
                    current_deg = 0    # set turn_degrees not active
                    motors_behavior_active = False
                    if inhibit_drive is not True:
                        egpg.stop()
                        continue
                    else:
                        sim_start_time = None
                        continue
                # active no early stop request 
                ldps = egpg.get_motor_status(egpg.MOTOR_LEFT)[3]
                rdps = egpg.get_motor_status(egpg.MOTOR_RIGHT)[3]
                # logging.info("motors status l: {} DPS  r: {} DPS".format(ldps,rdps))
                if (ldps + rdps) == 0:     # Done turn
                    if (sim_start_time):
                        dt = time.time() - sim_start_time
                        if (dt < 1):
                            continue
                        else:
                            sim_start_time = None
                    msg="Motors Behavior turn_degrees completed"
                    logging.info(msg)
                    current_deg = 0
                    mot_deg = 0
                    motors_behavior_active = False
                elif mot_deg == 0:  # stop turn early
                    egpg.stop()
                    logging.info("Motors Behavior turn_degrees terminated early")
                    sim_start_time = None   # in case simulating 


            elif (mot_deg != current_deg):  # turn_degrees desired
                msg="Motors Behavior turn_degrees: {}".format(mot_deg)
                logging.info(msg)
                current_deg = mot_deg
                motors_behavior_active = True
                if inhibit_drive is not True:
                    logging.info("Motors Behavior: Commanding egpg.turn_degrees({})".format(mot_deg))
                    egpg.turn_degrees(mot_deg, blocking=False)
                else:
                    logging.info("Motors Behavior inhibit_drive True - simulating command")
                    sim_start_time = time.time()



            if (current_cm != 0):      # active in drive_cm
                if (mot_cm == 0):          # early stop request
                    logging.info("Motors Behavior Early Stop of drive_cm")
                    current_cm = 0    # set drive_cm not active
                    motors_behavior_active = False
                    if inhibit_drive is not True:
                        egpg.stop()
                        continue
                    else:
                        sim_start_time = None
                        continue
                # active no early stop request 
                ldps = egpg.get_motor_status(egpg.MOTOR_LEFT)[3]
                rdps = egpg.get_motor_status(egpg.MOTOR_RIGHT)[3]
                # logging.info("motors status l: {} DPS  r: {} DPS".format(ldps,rdps))
                if (ldps + rdps) == 0:     # Done turn
                    if (sim_start_time):
                        dt = time.time() - sim_start_time
                        if (dt < 1):
                            continue
                        else:
                            sim_start_time = None
                    msg="Motors Behavior drive_cm completed"
                    logging.info(msg)
                    current_cm = 0
                    mot_cm = 0
                    motors_behavior_active = False
                elif mot_cm == 0:  # stop turn early
                    egpg.stop()
                    logging.info("Motors Behavior drive_cm terminated early")
                    sim_start_time = None   # in case simulating 

            elif (mot_cm != current_cm):  # drive_cm desired
                msg="Motors Behavior drive_cm: {}".format(mot_cm)
                logging.info(msg)
                current_cm = mot_cm
                motors_behavior_active = True
                if inhibit_drive is not True:
                    egpg.drive_cm(mot_cm, blocking=False)
                else:
                    logging.info("Motors Behavior inhibit_drive True - simulating command")
                    sim_start_time = time.time()


            elif (mot_trans != current_trans) or (mot_rot != current_rot):
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
    global escape_behavior_active, escape_trans, escape_rot, escape_deg, escape_cm

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
                escape_deg = 0                 # stop any turn_degrees
                escape_cm  = 0                 # stop any drive_cm

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
    global avoid_behavior_active, avoid_trans, avoid_rot, avoid_deg, avoid_cm

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
                avoid_deg = 0
                avoid_cm  = 0

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


# ARUCODRIVE BEHAVIOR

def aruco_drive_behavior():
    global aruco_drive_behavior_active, inhibit_aruco_drive, aruco_drive_trans, aruco_drive_rot, aruco_drive_deg, aruco_drive_cm, pan_angles, inhibit_scan, inhibit_aruco_sensor

    try:
        msg="Starting Aruco Drive Behavior Thread"
        logging.info(msg)
        docking_ready = False

        while (tArUcoDrive.exitFlag is not True):

            time.sleep(1.0/ARUCO_DRIVE_RATE)
            if inhibit_aruco_drive:
                # pan_angles = prior_pan_angles
                # inhibit_scan = prior_inhibit_scan
                continue

            if aruco_drive_behavior_active is not True:   # start up behavior

                # save off scan parameters and start scan as front only
                prior_pan_angles = pan_angles
                prior_inhibit_scan = inhibit_scan
                pan_angles = PAN_ANGLE_FRONT
                inhibit_scan = False

                # start aruco_sensor_behavior if not already running
                inhibit_aruco_sensor = False
                logging.info("aruco_drive_behavior: enabled aruco_sensor")

                aruco_drive_behavior_active = True
                logging.info("aruco_drive_behavior: active and not inhibited")

            elif if_marker():
                marker = if_marker()[0]
                logging.info("aruco_drive_behavior: got marker: {}".format(marker))

                if if_obstacle():
                    logging.info("aruco_drive_behavior: blocked by obstacle")
                    aruco_drive_trans = 0
                    aruco_drive_rot = 0
                    aruco_drive_deg = 0
                    aruco_drive_cm  = 0
                    inhibit_aruco_drive = True

                elif (dist_reading_cm > DOCKING_READY_DIST):
                    logging.info("aruco_drive_behavior: Driving toward marker")
                    aruco_drive_trans = aruco_drive_default_trans
                    dX = marker[1] - MARKER_AHEAD_PIXEL
                    logging.info("aruco_drive_behavior: marker cX: {} dX: {} dist: {}".format(marker[1], dX, dist_reading_cm))
                    if (abs(dX) > 10):
                        aruco_drive_rot = int(dX/10)
                    else:
                        aruco_drive_rot = 0
                    aruco_drive_deg = 0
                    aruco_drive_cm  = 0
                elif docking_ready is not True:
                    docking_ready = True
                    logging.info("aruco_drive_behavior: Arrived at docking ready point")
                    aruco_drive_trans = 0
                    aruco_drive_rot = 0
                    aruco_drive_deg = 0
                    aruco_drive_cm  = 0
                    time.sleep(2)
                    logging.info("aruco_drive_behavior: Turning 180")
                    aruco_drive_deg = 180   # arbitrate will reset this when accepted
                    while aruco_drive_deg > 0:
                        logging.info("aruco_drive_behavior: waiting for turn 180 to complete")
                        time.sleep(1.0/ARUCO_DRIVE_RATE)
                else:  # at docking reedy and turned 180
                    inhibit_aruco_drive = True
                    aruco_drive_behavior_active = False

            else:   # marker not in view
                logging.info("aruco_drive_behavior: stopping")
                aruco_drive_trans = 0
                aruco_drive_rot = 0
                aruco_drive_deg = 0
                aruco_drive_cm  = 0
                # inhibit_aruco_drive = True

    except Exception as e:
        emergency_stop()
        msg="Exception in aruco_drive_behavior"
        logging.info(msg)
        logging.info("Exception {}".format(str(e)))
        aruco_drive_behavior_active = False
        inhibit_aruco_drive = True
        tArUcoDrive.exc = e

# END ARUCODRIVE BEHAVIOR

# ARUCO FIND BEHAVIOR
# - Rotate slowly until ArUco marker is seen
# - Turn to face marker


def aruco_find_behavior():
    global aruco_find_behavior_active, inhibit_aruco_find, inhibit_aruco_sensor, aruco_find_trans, aruco_find_rot, aruco_find_deg, aruco_find_cm

    try:
        msg="Starting Aruco Find Behavior Thread"
        logging.info(msg)


        while (tArUcoFind.exitFlag is not True):

            time.sleep(1.0/ARUCO_FIND_RATE)
            if inhibit_aruco_find:
                aruco_find_behavior_active = False
                continue

            logging.info("aruco_find_behavior: active")
            aruco_find_behavior_active = True

            if inhibit_aruco_sensor is True:
                inhibit_aruco_sensor = False    # turn on scanning
                logging.info("aruco_find_behavior: Enabling aruco_sensor_behavior")
                time.sleep(1)

            angle_turned = 0
            start_l_enc, start_r_enc = egpg.read_encoders()
            start_time = time.time()
            scan_time_sec = 0
            found_aruco_marker = len(aruco_markers)
            while (found_aruco_marker is not True) and (angle_turned < 720) and (scan_time_sec < ARUCO_FIND_SCAN_TIME):
                # start or continue rotation
                aruco_find_trans = 0
                aruco_find_rot = aruco_find_default_rot
                aruco_find_deg = 0
                aruco_find_cm  = 0

                # yield to keep processor load down
                time.sleep(1.0/ARUCO_FIND_RATE)
                # compute angle turned
                curr_l_enc, curr_r_enc = egpg.read_encoders()
                dEnc_l = curr_l_enc - start_l_enc
                dEnc_r = curr_r_enc - start_r_enc
                angle_turned = wheellog.enc_to_angle_deg(egpg, dEnc_l, dEnc_r)
                scan_time_sec = time.time() - start_time
                logging.info("aruco_find_behavior: angle_turned: {:>4.0f}  scan_time_sec: {:>4.0f}".format(angle_turned, scan_time_sec))
                # May have found a marker
                if len(aruco_markers) > 0:
                    markerID = aruco_markers[0][0]
                    cX = aruco_markers[0][1]
                    cY = aruco_markers[0][2]
                    logging.info("aruco_find_behavior:  Found  marker {} at [{}, {}]".format(markerID, cX, cY))
                    if  abs(cX - HALF_FOV_X_PIXELS) < 80:
                        found_aruco_marker = True
            # Found marker or spun twice
            aruco_find_rot = 0   # stop turning
            if (angle_turned > 720) or (scan_time_sec > ARUCO_FIND_SCAN_TIME):
                logging.info("aruco_find_behavior: angle_turned: {:>4.0f}  scan_time_sec: {:>4.0f}".format(angle_turned, scan_time_sec))
                logging.info("aruco_find_behavior:  Failed to find marker")
                inhibit_aruco_sensor = True
                inhibit_aruco_find = True            # stop trying to find
                continue

            # May have found a marker
            if len(aruco_markers) > 0:
                markerID = aruco_markers[0][0]
                cX = aruco_markers[0][1]
                cY = aruco_markers[0][2]
                logging.info("aruco_find_behavior:  Terminating search  marker {} at [{}, {}]".format(markerID, cX, cY))

            # Done
            inhibit_aruco_find = True



    except Exception as e:
        msg="Exception in aruco_find_behavior"
        logging.info(msg)
        logging.info("Exception {}".format(str(e)))
        aruco_find_behavior_active = False
        inhibit_aruco_find = True
        tArUcoFind.exc = e

# END ARUCO FIND BEHAVIOR


# ARUCO SENSOR BEHAVIOR

def aruco_sensor_behavior():
    global aruco_sensor_behavior_active, inhibit_aruco_sensor, aruco_markers

    try:
        msg="Starting Aruco Sensor Behavior Thread"
        logging.info(msg)

        prior_inhibit_aruco_sensor = inhibit_aruco_sensor
        arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
        arucoParams = cv2.aruco.DetectorParameters_create()
        # initialize the video stream and allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        vs = VideoStream(src=0, framerate=15)
        if inhibit_aruco_sensor is not True:
            vs.start()
        # vs = VideoStream(usePiCamera=True, framerate=10)
        aruco_sensor_behavior_active = True
        prior_inhibit_aruco_sensor = inhibit_aruco_sensor

        while (tArUcoSensor.exitFlag is not True):

            time.sleep(1.0/ARUCO_SENSOR_RATE)
            if inhibit_aruco_sensor:
                if prior_inhibit_aruco_sensor is not True:
                    logging.info("Aruco Sensor Now Inhibited")
                    aruco_markers = []
                    vs.stop()
                    prior_inhibit_aruco_sensor = inhibit_aruco_sensor
                continue


            elif prior_inhibit_aruco_sensor:   # was inhibited now not
                logging.info("Aruco Sensor No Longer Inhibited")
                vs.start()
                time.sleep(0.5)
                prior_inhibit_aruco_sensor = inhibit_aruco_sensor 
           # logging.info("aruco_sensor_behavior executing now")
            colorframe = vs.read()
            # colorframe = picam2.capture_array()
            frame = cv2.cvtColor(colorframe, cv2.COLOR_BGR2GRAY)
            # frame = imutils.resize(frame, width=1000)
            # frame = imutils.resize(frame, width=1000)
            # detect ArUco markers in the input frame
            (corners, ids, rejected) = cv2.aruco.detectMarkers(frame,
                                       arucoDict, parameters=arucoParams)

            # verify *at least* one ArUco marker was detected
            if len(corners) > 0:
                # flatten the ArUco IDs list
                ids = ids.flatten()
                # loop over the detected ArUCo corners
                new_aruco_markers = []
                for (markerCorner, markerID) in zip(corners, ids):
                    # extract the marker corners (which are always returned in
                    # top-left, top-right, bottom-right, and bottom-left order)
                    corners = markerCorner.reshape((4, 2))
                    (topLeft, topRight, bottomRight, bottomLeft) = corners

                    # convert each of the (x, y)-coordinate pairs to integers
                    topRight = (int(topRight[0]), int(topRight[1]))
                    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                    topLeft = (int(topLeft[0]), int(topLeft[1]))

                    # draw the bounding box of the ArUCo detection
                    # cv2.line(colorframe, topLeft, topRight, (0, 255, 0), 2)
                    # cv2.line(colorframe, topRight, bottomRight, (0, 255, 0), 2)
                    # cv2.line(colorframe, bottomRight, bottomLeft, (0, 255, 0), 2)
                    # cv2.line(colorframe, bottomLeft, topLeft, (0, 255, 0), 2)
                    # compute the center (x, y)-coordinates of the ArUco marker
                    cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                    cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                    if DISPLAY_MARKERS:
                        # draw the center of the ArUco marker
                        cv2.circle(colorframe, (cX, cY), 4, (0, 0, 255), -1)
                        # draw the ArUco marker ID on the frame
                        cv2.putText(colorframe, str(markerID),
                           (topLeft[0], topLeft[1] - 15),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 0), 2)
                        cv2.imshow("aruco_sensor_behavior", colorframe)
                        cv2.waitKey(1)
                    # print("Marker: {} at [{}, {}]".format(str(markerID), cX, cY))
                    if len(new_aruco_markers) == 0:
                        new_aruco_markers = [(markerID, cX, cY)]
                aruco_markers = new_aruco_markers
                # logging.info("Aruco Sensor Behavior: aruco_markers: {}".format(aruco_markers))
            else:
                if DISPLAY_MARKERS:
                    cv2.destroyAllWindows()
                aruco_markers = []
        # terminating aruco_sensor_behavior
        if vs is not None:
            vs.stop()
        aruco_sensor_behavior_active = False

    except Exception as e:
        msg="Exception in aruco_sensor_behavior"
        logging.info(msg)
        logging.info("Exception {}".format(str(e)))
        aruco_sensor_behavior_active = False
        inhibit_aruco_sensor = True
        if DISPLAY_MARKERS:
            cv2.destroyAllWindows()
        tArUcoSensor.exc = e
        if vs is not None:
            vs.stop()

# END ARUCO SENSOR BEHAVIOR

# CRUISE BEHAVIOR

def cruise_behavior():
    global cruise_behavior_active, cruise_trans, cruise_rot, cruise_deg, cruise_cm

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
            cruise_deg = 0
            cruise_cm  = 0

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
    global arbitrate_behavior_active, mot_trans, mot_rot, mot_degrees, mot_cm, aruco_drive_deg, aruco_drive_cm

    try:
        msg="Starting Arbitrate Behavior Thread"
        logging.info(msg)

        waiting_deg = False  # flag when waiting for motors behavior to complete turn_degrees()
        waiting_cm  = False  # flag when waiting for motors behavior to complete drive_cm()

        while (tArbitrate.exitFlag is not True):
            time.sleep(1.0/ARBITRATE_RATE)

            if inhibit_arbitrate:
                continue


            if escape_behavior_active:
                # logging.info("Setting Escape Commands")
                mot_trans = escape_trans
                mot_rot   = escape_rot
                mot_deg     = escape_deg
                mod_cm      = escape_cm
            elif avoid_behavior_active:
                # logging.info("Setting Avoid Commands")
                mot_trans  = avoid_trans
                mot_rot    = avoid_rot
                mot_deg     = avoid_deg
                mod_cm      = avoid_cm
            elif aruco_find_behavior_active:
                # logging.info("arbitrate_behavior: Setting ArUco Find Commands")
                mot_trans   = aruco_find_trans
                mot_rot     = aruco_find_rot
                mot_deg     = aruco_find_deg
                mod_cm      = aruco_find_cm
            elif aruco_drive_behavior_active:
                logging.info("Setting ArUco Drive Commands deg:{} cm:{} trans:{} rot:{}".format(aruco_drive_deg, aruco_drive_cm, aruco_drive_trans, aruco_drive_rot))
                if aruco_drive_deg != 0:   # reset to show accepted
                    if waiting_deg:
                        if mot_deg == 0:  # done
                            waiting_deg = False
                            aruco_drive_deg = 0
                        else:     # not done
                            pass
                    else:           # tell motors to start turn_degrees
                        mot_deg     = aruco_drive_deg
                        waiting_deg = True
                elif aruco_drive_cm != 0:    # reset to show accepted
                    if waiting_cm:
                        if mot_cm == 0:  # done
                            waiting_cm = False
                            aruco_drive_cm = 0
                        else:     # not done
                            pass
                    else:           # tell motors to start drive_cm()
                        mot_cm     = aruco_drive_cm
                        waiting_cm = True
                else:
                    mot_trans   = aruco_drive_trans
                    mot_rot     = aruco_drive_rot
                    mot_deg     = aruco_drive_deg
                    mod_cm      = aruco_drive_cm
            elif cruise_behavior_active:
                # logging.info("Setting Cruise Commands")
                mot_trans   = cruise_trans
                mot_rot     = cruise_rot
                mot_deg     = cruise_deg
                mod_cm      = cruise_cm
            else:
                # logging.info("Stopping - No Commands")
                mot_trans  = 0
                mot_rot    = 0
                mot_deg    = 0
                mod_cm     = 0


    except Exception as e:
        msg="Exception in arbitrate_behavior"
        mot_trans  = 0
        mot_rot    = 0
        mot_deg    = 0
        mod_cm     = 0
        logging.info(msg)
        logging.info("Exception {}".format(str(e)))
        arbitrate_behavior_active = False
        tArbitrate.exc = e

# END ARBITRATE BEHAVIOR







# SETUP AND TEAR DOWN BEHAVIOR

def setup():
    global egpg, tScan, tMotors, tEscape, tArbitrate, tAvoid, tCruise, tArUcoFind, tArUcoDrive, tArUcoSensor

    try:
        egpg = init_robot(ds_port="RPI_1", pan_port="SERVO1")

        msg="Subsumption Architecture Setup Initiated"
        logging.info(msg)
        say(msg)

        tScan = Behavior(scan_behavior)
        tScan.start()

        tArUcoSensor = Behavior(aruco_sensor_behavior)
        tArUcoSensor.start()

        tArUcoFind = Behavior(aruco_find_behavior)
        tArUcoFind.start()

        tArUcoDrive = Behavior(aruco_drive_behavior)
        tArUcoDrive.start()

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
        logging.info("Telling ArUco Drive behavior thread to exit (if still running)")
        tArUcoDrive.exitFlag = True
        logging.info("Waiting for ArUco Drive thread to exit")
        tArUcoDrive.join()
    except Exception as e:
        logging.info("Got exception set in ArUcoDrive thread: %s", e)

    try:
        logging.info("Telling ArUco Find behavior thread to exit (if still running)")
        tArUcoFind.exitFlag = True
        logging.info("Waiting for ArUco Find thread to exit")
        tArUcoFind.join()
    except Exception as e:
        logging.info("Got exception set in ArUco Find thread: %s", e)

    try:
        logging.info("Telling ArUco Sensor  behavior thread to exit (if still running)")
        tArUcoSensor.exitFlag = True
        logging.info("Waiting for ArUco Sensor thread to exit")
        tArUcoSensor.join()
    except Exception as e:
        logging.info("Got exception set in ArUco Sensor thread: %s", e)

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

    logging.info("==== ArUco Drive  MODULE MAIN ====")
    say("R. U co. Drive.")
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
        logging.info("==== ArUco Drive  Main Done ====")
        say("R. U co. Drive. Main done.")


if __name__ == "__main__":
    main()

