#!/usr/bin/env python
#
# GUARD CLOSEST OBJECT
"""
This program performs the following plan:
1) Perform 360 degree scan (Spin GoPiGo3 one complete revolution taking distance measurements)
2) Print 360 degree view to console
3) Turn toward closest object
4) Move to "Guard Spot" (wheels 8 inches from object: 1.5" baseboards, 5.5" turning radius, 1.5" safety)
5) Rotate 180 to "Guarding Direction"
6) Repeatedly perform 160 degree sector servo scan
  - If something moves closer, announce "I saw that"
  - If something moves within Guard Area, announce "Back off.  I am protecting this area"

"""

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import sys
sys.path.append('/home/pi/Carl/plib')

from time import sleep, clock
import easygopigo3 # import the GoPiGo3 class
import math
import printmaps
import scan360
import tiltpan
import servoscan
import status
import battery
import runLog

def remove_zero_readings(dist_l,angle_l):
    nz_reading_index_l = [i for i, x in  enumerate(dist_l) if dist_l[i] > 0]
    nz_dist_l = [dist_l[i] for i in nz_reading_index_l]
    nz_angl_l = [angle_l[i] for i in nz_reading_index_l]
    return nz_dist_l,nz_angl_l

def closest_obj(dist_l,angle_l):
    nz_dist_l, nz_angle_l = remove_zero_readings(dist_l,angle_l)
    closest_obj_i = dist_l.index(min(nz_dist_l))
    return nz_dist_l[closest_obj_i], nz_angle_l[closest_obj_i]



def main():

    runLog.logger.info("Starting GCO.py")
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True) # Create an instance of the EasyGoPiGo3 class
    ds = egpg.init_distance_sensor()
    ts = egpg.init_servo(tiltpan.TILT_PORT)
    ps = egpg.init_servo(tiltpan.PAN_PORT)

    tiltpan.tiltpan_center()

    # Adjust GOPIGO3 CONSTANTS to my bot   default EasyGoPiGo3.WHEEL_DIAMETER = 66.5 mm
    egpg.WHEEL_DIAMETER = 64.5				# empirical from systests/wheelDiaRotateTest.py
    egpg.WHEEL_CIRCUMFERENCE = egpg.WHEEL_DIAMETER * math.pi
    egpg.WHEEL_BASE_WIDTH = 114.72
    egpg.WHEEL_BASE_CIRCUMFERENCE = egpg.WHEEL_BASE_WIDTH * math.pi

    dist_list_mm = []
    at_angle_list = []
    scan360speed = 120
    safe_distance = 20.32 # cm  8 inches wheels to wall/object
    ds_to_wheels = 7      # cm    distance sensor is 2.75 inches in front of wheels
    try:
        #  spin360 taking distance measurement
        print("\n360 degree scan  at speed={}".format(scan360speed))
	dist_list_mm,at_angle_list = scan360.spin_and_scan(egpg, ds, 360, speed=scan360speed)   # spin taking distance readings
	range_list_cm = [ dist/10 for dist in dist_list_mm ]
	printmaps.view360(range_list_cm, at_angle_list)     # print view (all r positive, theta 0=left
	print("Readings:{}".format(len(at_angle_list)))

        sleep(3)

        #  spin to face closest object
	dist_to_target, scan_angle_to_target = closest_obj(range_list_cm, at_angle_list)
        angle_to_target = scan_angle_to_target - 90   # adjust for 0=left
	print("\nClosest object is {:.1f} cm at {:.0f} degrees".format(dist_to_target, angle_to_target))

        sleep(3)

        print("\nTurning {:.0f} at {} dps to face closest object".format(angle_to_target, egpg.get_speed()))
	egpg.turn_degrees(angle_to_target)

        sleep(3)

        #  travel to point where wheels are 10 inches from object (will back up if too close)
        dist_to_guard_spot = dist_to_target + ds_to_wheels  - safe_distance
        print("\nMoving {:.0f} cm to guard spot".format(dist_to_guard_spot))
        egpg.drive_cm(dist_to_guard_spot)

        sleep(3)

        #  perform a 160 degree scan with obj in the center
        #  spin 180 to face away from object
        print("\nTurning 180 to guard direction")
        egpg.turn_degrees(180)

        sleep(3)

        #  loop
            #  perform a quick 160 degree scan
            #  if something gets closer, wag head and announce "I saw that."
        while True:
            dist_l,angl_l=servoscan.ds_map(ds, ps,num_of_readings=72,rev_axis=True)
            printmaps.view180(dist_l,angl_l,grid_width=80,units="cm",ignore_over=230)
            #  turn  distance sensor (eyes) to face closest object
	    dist_to_closest, scan_angle_to_closest = closest_obj(dist_l, angl_l)
            angle_to_closest = scan_angle_to_closest # - 90   # adjust for 0=left
            print("\nClosest object is {:.1f} cm at {:.0f} degrees".format(dist_to_closest, angle_to_closest))
            print("\nPointing {:.0f} to face closest object".format(angle_to_closest))
	    tiltpan.pan(angle_to_closest)
	    sleep(2)
            status.printStatus(egpg,ds)
            sleep(30)
            tiltpan.tiltpan_center()
#            status.batterySafetyCheck()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    egpg.stop()           # stop motors
            runLog.logger.info("Exiting GCO.py"
    	    print("Ctrl-C detected - Finishing up")
    egpg.stop()

if __name__ == "__main__":
	main()
