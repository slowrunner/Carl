#!/usr/bin/env python

"""
## File: printMaps.py

This module prints out LIDAR like maps:

- view180()  prints r-theta data for 180 degrees of view (theta: 0 = Left, r=0 at bottom of view)
- view360()  prints r-theta data for 360 degrees of view (theta: 0 = Left, r=0 in center of view)

from distance_list and angle_list of unsorted values

And can create test data for 180 or 360 degree views
- createTestData()   returns sector scan of readings
- createTestWallData()  returns sector scan of a wall in front of GoPiGo3
- create360TestData()   returns a 360 degree scan around GoPiGo3
- create360TestWallsData()  returns four wall square around GoPiGo3

With a test main
- main() tests routines

# Required Elements:


# Usage:
1) import printMaps.py
2) collect data
3) printMaps.view180()    or printMaps.view360()

# History:
 ------------------------------------------------
  Author        Date                    Comments
  McDonley      Sept 2018      Based on DI us_servo_scan.py Karen June 2014

** Notes:
  DI refers to Dexter Industries see DexterIndustries.com

## License

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

#
from __future__ import print_function
from __future__ import division
#
from collections import Counter
import math
from math import pi, radians, degrees, cos, sin
import numpy as np
import random

debug = False                  # True to print all raw values


# ******** PRINT FORWARD 180 Degree VIEW *********
#
# view180()      Print a "forward 180 view" with GoPiGo3 at middle of x-axis grid
#                0 deg = left 90 deg center 180 deg right
#		 Scale is adjusted to farthest valid reading
#	Parmaeters:
#		dist_l		# required list of range values  e.g. [20, 30, 20] facing into corner
#		ang_l		# required list of reading angle (0=left) e.g. [0,90,180]
#		grid_width=80	# optional printout chars to fit map into
#		units="cm"	# optional label for range units
#		ignore_over=300 # use to ignore readings beyond valid sensor detection range
#				  or if sensor returns a particular value if nothing detected
#

def view180(dist_l,ang_l,grid_width=80,units="cm",ignore_over=300):
        CHAR_ASPECT_RATIO=2.12
        if debug: print("view180() called with grid_width:",grid_width)
        if not(grid_width % 2): grid_width -=1
        if debug: print("using grid_width:",grid_width)
        index_list_valid_readings = [i for i, x in enumerate(dist_l) if (0 < dist_l[i] < ignore_over)]
        valid_dist_l = [dist_l[i] for i in index_list_valid_readings]
        valid_ang_l  = [ang_l[i] for i in index_list_valid_readings]
        num_of_readings = len(valid_dist_l)
        x=[0]*(num_of_readings+1)       # list to hold the x coordinate of each point
        y=[0]*(num_of_readings+1)       # list to hold the y coordinate of each point
        grid_height = int( int((grid_width-3)/2) / CHAR_ASPECT_RATIO)
        max_valid = max(valid_dist_l)
        X_SCALE_FACTOR=max_valid/int((grid_width-3)/2)
        Y_SCALE_FACTOR=X_SCALE_FACTOR * CHAR_ASPECT_RATIO
        if debug:
            print("Farthest reading:{} ".format(max(dist_l)),end='')
            print("Farthest_valid:{} ".format(max_valid),end='')
            print("X_SCALE_FACTOR:{} Y_SCALE_FACTOR:{}".format(X_SCALE_FACTOR,Y_SCALE_FACTOR))
            print("grid_width: {} grid_height: {}".format(grid_width,grid_height))
        #Convert the distance and angle to (x,y) coordinates and scale it down
        if debug:  print("Scaled Cartesian Data (0deg=left)")
        for i in range(num_of_readings):
                x[i] = -int( valid_dist_l[i] * cos(radians(valid_ang_l[i]) )/X_SCALE_FACTOR )
                y[i] =  int( valid_dist_l[i] * sin(radians(valid_ang_l[i]) )/Y_SCALE_FACTOR )
                if debug:
                   print("x[{}] y[{}]=[{} {}]".format(i,i,x[i],y[i]))

 
        #Create a grid  [ [top row] , [next lower] ... [bottom (y=0) row] ]
        grid = [[0 for a in range(grid_width-2)] for a in range(grid_height+1)]
        if debug:
            print("grid[0]:",grid[0])
            print("len(grid):",len(grid))

        if debug:  print("Put value 1 in grid for each trusted_reading")
        for i in range (num_of_readings):
                grid_x = int((grid_width-3)/2 + x[i])
                #if x[i] > 0: grid_x +=1
                grid_y = grid_height-y[i]
                if debug:
                    print("x[{0}]:{1} grid_x: {2}  y[{0}]:{3} grid_y: {4}".format(i,x[i],grid_x, y[i], grid_y))
                grid[grid_y][grid_x] = 1

        bot_fence=" "+'-'*int((grid_width-3)/2)+"0"+'-'*int((grid_width-3)/2)
        top_fence=" "+'-'*(grid_width-2)


        #Print the map
        label=("{:.0f} {}".format(int((grid_width-3)/2)*X_SCALE_FACTOR,units))
        print("\nMap:"+" "*int((grid_width-12)/2),label)
        print(top_fence)
        for i in range(grid_height+1):
                if debug:
                    print("|", end='')
                    for j in range (grid_width-2):
                        print(grid[i][j], end='')
                    print("|")
                print("|", end='')
                for j in range (grid_width-2):
                        if (j==int((grid_width-3)/2)) and i == grid_height:
                                print("+", end='')
                        elif grid[i][j]==0:
                                print(" ", end='')
                        else:
                                print("o", end='')
                print("|")
        print(bot_fence, label)
        closest_obj=min(valid_dist_l)
        farthest_reading=max(dist_l)
        print("Each '-' is {:.1f} {}      ".format(X_SCALE_FACTOR,units),end='')
        print("Each '|' is {:.1f} {}".format(Y_SCALE_FACTOR,units))
        print("Closest Object: {0:.1f} {1}  ".format(closest_obj,units),end='')
        print("Farthest Valid Object: {:.1f} {}".format(max_valid,units))
        print("Farthest Reading: {:.1f} {}".format(farthest_reading,units))
        return closest_obj      #Return the closest distance in all directions

# END view180()



# ******** PRINT 360 Degree VIEW ***********
#
#   view360(dist_l,ang_l,grid_width, units,ignore_over)
# 
#       Print a "360 degree view with 90 up" and GoPiGo3 at middle of grid
#                0 deg = left center   270 deg bottom center   180 deg right center
#		         Scale is adjusted to farthest valid reading
#                Note:  ALL RANGE VALUES ARE POSITIVE VALUES!
#	Parmaeters:
#		dist_l		# required list of range values  e.g. [20, 30, 20] facing into corner
#		ang_l		# required list of reading angle (0=left) e.g. [0,90,180]
#		grid_width=80	# optional printout chars to fit map into
#		units="cm"	# optional label for range units
#		ignore_over=300 # use to ignore readings beyond valid sensor detection range
#				  or if sensor returns a particular value if nothing detected
#

def view360(dist_l,ang_l,grid_width=80, units="cm", ignore_over=300):
        #debug=True
        CHAR_ASPECT_RATIO=2.12
        if debug: print("view360() called with grid_width:",grid_width)
        if not(grid_width % 2): grid_width -=1
        if debug: print("using grid_width:",grid_width)
        index_list_valid_readings = [i for i, x in enumerate(dist_l) if dist_l[i] < ignore_over]
        valid_dist_l = [dist_l[i] for i in index_list_valid_readings]
        valid_ang_l  = [ang_l[i] for i in index_list_valid_readings]
        num_of_readings = len(valid_dist_l)
        x=[0]*(num_of_readings+1)       # list to hold the x coordinate of each point
        y=[0]*(num_of_readings+1)       # list to hold the y coordinate of each point
        grid_height = int( (grid_width-3) / CHAR_ASPECT_RATIO)
        max_valid = max(valid_dist_l)
        X_SCALE_FACTOR=max_valid/int((grid_width-3)/2)
        Y_SCALE_FACTOR=X_SCALE_FACTOR * CHAR_ASPECT_RATIO
        if debug:
            print("Farthest reading:{} ".format(max(dist_l)),end='')
            print("Farthest_valid:{} ".format(max_valid),end='')
            print("X_SCALE_FACTOR:{} Y_SCALE_FACTOR:{}".format(X_SCALE_FACTOR,Y_SCALE_FACTOR))
            print("grid_width: {} grid_height: {}".format(grid_width,grid_height))
        #Convert the distance and angle to (x,y) coordinates and scale it down
        if debug:  print("Scaled Cartesian Data (0deg=left)")
        for i in range(num_of_readings):
                x[i] = -int( valid_dist_l[i] * cos(radians(valid_ang_l[i]) )/X_SCALE_FACTOR )
                y[i] =  int( valid_dist_l[i] * sin(radians(valid_ang_l[i]) )/Y_SCALE_FACTOR )
                if debug:
                   print("x[{}] y[{}]=[{} {}]".format(i,i,x[i],y[i]))


        #Create a grid  [ [top row] , [next lower] ... [bottom row] ]
        grid = [[0 for a in range(grid_width-2)] for a in range(grid_height+1)]
        if debug:
            print("grid[0]:",grid[0])
            print("len(grid):",len(grid))

        if debug:  print("Put value 1 in grid for each trusted_reading")
        for i in range (num_of_readings):
                grid_x = int((grid_width-3)/2 + x[i])
                #if x[i] > 0: grid_x +=1
                grid_y = int(grid_height/2)-y[i]
                if debug:
                    print("x[{0}]:{1} grid_x: {2}  y[{0}]:{3} grid_y: {4}".format(i,x[i],grid_x, y[i], grid_y))
                grid[grid_y][grid_x] = 1

        bot_fence=" "+'-'*int((grid_width-3)/2)+"0"+'-'*int((grid_width-3)/2)
        top_fence=" "+'-'*(grid_width-2)


        #Print the map
        label=("{:.0f} {}".format(int((grid_width-3)/2)*X_SCALE_FACTOR,units))
        print("\nMap:"+" "*int((grid_width-12)/2),"90 deg")
        print(top_fence,label)
        for i in range(grid_height):
                if debug:
                    print("|", end='')
                    for j in range (grid_width-2):
                        print(grid[i][j], end='')
                    print("|")
                print("|", end='')
                for j in range (grid_width-2):
                        if (j==int((grid_width-3)/2)) and i == int(grid_height/2):
                                print("+", end='')
                        elif grid[i][j]==0:
                                print(" ", end='')
                        else:
                                print("o", end='')
                if i == int(grid_height/2):
                    print("0  180 deg")
                else:
                    print("|")
        print(bot_fence, label)
        closest_obj=min(valid_dist_l)
        farthest_reading=max(dist_l)
        print("Each '-' is {:.1f} {}      ".format(X_SCALE_FACTOR,units),end='')
        print("Each '|' is {:.1f} {}".format(Y_SCALE_FACTOR,units))
        print("Closest Object: {0:.1f} {1}  ".format(closest_obj,units),end='')
        print("Farthest Valid Object: {:.1f} {}".format(max_valid,units))
        print("Farthest Reading: {:.1f} {}".format(farthest_reading,units))
        return closest_obj      #Return the closest distance in all directions

# END view360()





# ******* DISPLAY VALUES
#
# display_values(dist_l,ang_l)
#
def display_values(dist_l,ang_l):
    print("len(dist_l):",len(dist_l))
    print("len(ang_l):",len(ang_l))
    for i in range(len(dist_l)):
        print("r[{0}]: {1:.1f} theta[{0}]: {2:.1f}".format(i,dist_l[i],ang_l[i]))





# ******* CREATE 180 Degree SECTOR TEST DATA *******
#
#   createSectorTestData(sector,min_radius,radius,items,randomize_data)
#
#    Parms:
#
#       sector=120              Optional Scan Angle subtended around (pan) servo 90 degrees
#       min_radius=10           Optional minimum sensor distance for randomize_data
#       radius=50               Optional Desired Sensor Distance Readings
#       items=9                 Optional Desired Number of Readings (angles) within Desired Sector
#       randomize_data=False    Set to True for random distance readings between min_radius and radius
#
#   Returns:
#       returns two lists: distance_list[], angle_list[]

def createSectorTestData(sector=120, min_radius=10, radius=50, items=9, randomize_data = False):
    DECIMAL_DIGITS = 1

    half_sector = int(sector/2)
    angle_increment = half_sector/int(items/2)
    left_angle = 90-half_sector
    right_angle = 90+half_sector
    theta_l = []
    radius_l = []
    theta_list = np.arange(left_angle, right_angle+1, angle_increment)
    if debug:
        print("half_sector:",half_sector)
        print("angle_increment:",angle_increment)
        print("theta_list:",theta_list)



    for theta in theta_list:
        theta_l += [theta]
        if randomize_data:
            radius_l += [round(random.uniform(min_radius,radius),DECIMAL_DIGITS)]
        else: radius_l += [radius]
    if debug:
        print("\nTest Data")
        print("radius_l:",radius_l)
        print("theta_l:",theta_l)
    return radius_l,theta_l





# ******* CREATE 360 View TEST DATA *******
#
# create360TestData(min_radius,radius,items,randomize_data)
#
#    Parms:
#
#       sector=120              Optional Scan Angle subtended around (pan) servo 90 degrees
#       min_radius=10           Optional minimum sensor distance for randomize_data
#       radius=50               Optional Desired Sensor Distance Readings
#       items=9                 Optional Desired Number of Readings (angles) within Desired Sector
#       randomize_data=False    Set to True for random distance readings between min_radius and radius
#   Returns:
#       returns two lists: distance_list[], angle_list[]

def create360TestData(min_radius=10, radius=50, items=24, randomize_data = False):
    #debug=True
    DECIMAL_DIGITS = 1

    angle_increment = 360/items
    start_end_angle = 90

    theta_l = []
    radius_l = []
    theta_list = np.arange(0, 360, angle_increment)
    theta_list = [ (theta+90)%360 for theta in theta_list]
    if debug:
        print("angle_increment:",angle_increment)
        print("theta_list:",theta_list)



    for theta in theta_list:
        if randomize_data:
            radius_l += [round(random.uniform(min_radius,radius),DECIMAL_DIGITS)]
        else: radius_l += [radius]
    if debug:
        print("\n360 Test Data")
        print("len(theta_list):",len(theta_list))
        print("requested items:",items)
        print("radius_l:",radius_l)
        print("theta_l:",theta_list)
    return radius_l,theta_list





# ******* CREATE SINGLE TEST WALL DATA *******
#
# createTestWallData(sector,dist_to_wall_ctr,angle_to_normal_of_wall,items,sensor_error_pct)
#
#    Parms:
#
#       sector=60                   Optional Scan Angle subtended around (pan) servo 90 degrees
#       dist_to_wall_ctr=20         Optional Distance To Wall (90 degree range)
#       angle_to_normal_of_wall=0   Optional Angle of Wall
#                                   0 = no tilt, +X deg gives left readings longer, right readings shorter
#       items=9                     Optional Desired Number of Readings (angles) within Desired Sector
#       sensor_error_pct            Optional Percentage of Reading Error e.g. =4 wiggles readings +/- 2%
#   Returns:
#       returns two lists: distance_list[], angle_list[]

def createTestWallData(sector=60, dist_to_wall_ctr=20, angle_to_normal_of_wall=0, items=3, sensor_error_pct = 0):
    #debug=True
    half_sector = int(sector/2)
    angle_increment = half_sector/int(items/2)
    left_angle = 90-half_sector
    right_angle = 90+half_sector
    theta_l = []
    radius_l = []
    theta_list = np.arange(left_angle, right_angle+1, angle_increment)
    if debug:
        print("half_sector:",half_sector)
        print("angle_increment:",angle_increment)
        print("theta_list:",theta_list)

    # range along normal to wall is dist_to_wall_ctr * cos(angle_to_normal_of_wall)
    r_normal= dist_to_wall_ctr * cos(radians(angle_to_normal_of_wall))


    # if normal to wall is 90
    # cos = adjacent/hypotenuse so hypotenuse=cos(theta)/adjacent
    for theta in theta_list:
        theta_l += [theta]

        # beta  (angle from normal to theta) is 90+normal-theta
        beta = 90 + angle_to_normal_of_wall - theta
        # radius = distance along the normal to the wall * cos(angle between the normal and the sensor angle)
        radius = r_normal / cos(radians(beta))
        if sensor_error_pct != 0:
            error = random.uniform(-sensor_error_pct/2.0, sensor_error_pct/2.0) / 100.0
            radius = radius * (1+error)
        radius_l += [radius]

    if debug:
        print("\nTest Wall Data")
        print("radius_l:",radius_l)
        print("theta_l:",theta_l)
    return radius_l,theta_l


def sqr(x):
    return pow(x,2)






# ******* CREATE 360 Degree FOUR WALL TEST DATA *******
#
# create360TestWallData(dist_to_walls,items,sensor_error_pct)
#
#    Creates 360 Degree scan data of a four wall square looking first at a corner
#
#        #
#      # + #
#        #
#
#    Parms:
#
#       dist_to_walls=50            Optional Distance To Center of Walls (45,135,225,315 degree range)
#       items=24                    Optional Desired Number of Readings (angles) within Desired Sector
#       sensor_error_pct=0          Optional Percentage of Reading Error e.g. =4 wiggles readings +/- 2%
#
#   Returns:
#       returns two lists: distance_list[], angle_list[]

def create360TestWallData(dist_to_walls=50,items=24,sensor_error_pct=0):
    #debug=True
    angle_to_normal_to_wall=45
    DECIMAL_DIGITS = 1
    angle_increment = 360/items
    start_end_angle = 90
    # range along normal to wall is dist_to_wall_ctr * cos(angle_to_normal_of_wall)
    r_normal= dist_to_walls * cos(radians(angle_to_normal_to_wall))

    theta_l = []
    radius_l = []
    theta_list = np.arange(0, 360, angle_increment)
    theta_list = [ (theta+90) % 360 for theta in theta_list]
    if debug:
        print("angle_increment:",angle_increment)
        print("theta_list:",theta_list)
        print("dist_to_walls: {:.0f} r_normal: {:.0f}".format(dist_to_walls,r_normal))

    for theta in theta_list:
        if 90 <= theta < 180:
            # beta  (angle from normal to theta) is 90+normal-theta
            beta = 90 + angle_to_normal_to_wall - theta
            radius = r_normal / cos(radians(beta))
        elif 180 <= theta < 270:
            # beta  (angle from normal to theta) is 90+normal-theta
            beta = 90 + -angle_to_normal_to_wall - theta
            radius = -r_normal / cos(radians(beta))
        elif 270 <= theta < 360:
            # beta  (angle from normal to theta) is 90+normal-theta
            beta = 90 + angle_to_normal_to_wall - theta
            radius = -r_normal / cos(radians(beta))
        else:   # 0 <= theta < 90
            # beta  (angle from normal to theta) is 90+normal-theta
            beta = 90 + -angle_to_normal_to_wall - theta
            radius = r_normal / cos(radians(beta))
        if debug: print("theta:{:0.1f} reading:{:0.1f}".format(theta,radius))

        if sensor_error_pct != 0:
            error = random.uniform(-sensor_error_pct/2.0, sensor_error_pct/2.0) / 100.0
            radius = radius * (1+error)
        radius_l += [radius]



    if debug:
        print("\n360 Test Data")
        print("len(theta_list):",len(theta_list))
        print("requested items:",items)
        print("radius_l:",radius_l)
        print("theta_l:",theta_list)
    return radius_l,theta_list






# ******* TEST MAIN *****
def main():

    print("***** TEST printmaps.py *******")


    print("\n\nCREATE and DISPLAY: 180 Degree Sector READINGS ")
    #  CREATE EVENLY SPACED MAX DISTANCE r-theta READINGS
    dist_l,ang_l = createSectorTestData(sector=180, min_radius=2, radius=60, items=36, randomize_data=False)
    #  DISPLAY DATA in 180 character width
    view180(dist_l, ang_l, grid_width=60, units="inches")

    print("\n\nCREATE and DISPLAY: 120 Degree Sector READINGS ")
    #  CREATE EVENLY SPACED MAX DISTANCE r-theta READINGS
    dist_l,ang_l = createSectorTestData(sector=120, min_radius=2, radius=230, items=9, randomize_data=False)
    #  DISPLAY DATA in 180 character width
    view180(dist_l, ang_l, grid_width=60, units="cm")

    print("\n\nCREATE and DISPLAY: 120 Degree Sector RANDOMIZED READINGS")
    #  CREATE EVENLY SPACED Random DISTANCE r-theta READINGS
    dist_l,ang_l = createSectorTestData(sector=120, min_radius=2, radius=80, items=1000, randomize_data=True)
    #  DISPLAY DATA in 60 character width
    view180(dist_l, ang_l, grid_width=60, units="inches")

    print("\n\nCREATE and DISPLAY: 60 Degree Sector of WALL AT 90 degrees")
    #  CREATE TEST WALL r-theta READINGS
    dist_l,ang_l = createTestWallData(sector=60,dist_to_wall_ctr=12,items=5)
    #  DISPLAY DATA in 180 character width
    view180(dist_l, ang_l, grid_width=60, units="inches")

    print("\n\nCREATE and DISPLAY: 60 Degree Sector of Wall (NORMAL 15deg) with SENSOR ERRORS")
    #  CREATE TEST WALL r-theta READINGS For wall at an angle
    dist_l,ang_l = createTestWallData(sector=60,dist_to_wall_ctr=12,angle_to_normal_of_wall=15, items=5,sensor_error_pct=4)
    #  DISPLAY DATA in 180 character width
    view180(dist_l, ang_l, grid_width=60, units="inches")

    print("\n\nCREATE and DISPLAY: 360 Degree Scan")
    #  CREATE 360 Degree EVENLY SPACED MAX DISTANCE r-theta READINGS
    dist_l,ang_l = create360TestData( min_radius=2, radius=230, items=24, randomize_data=False)
    # display_values(dist_l,ang_l)
    #  DISPLAY DATA in 180 character width
    view360(dist_l, ang_l, grid_width=60, units="cm")

    print("\n\nCREATE and DISPLAY: 360 Degree Scan with RANDOMIZED READINGS")
    #  CREATE 360 Degree EVENLY SPACED RANDOM r-theta READINGS
    dist_l,ang_l = create360TestData( min_radius=150, radius=230, items=24, randomize_data=True)
    # display_values(dist_l,ang_l)
    #  DISPLAY DATA in 180 character width
    view360(dist_l, ang_l, grid_width=60, units="cm")

    print("\n\nCREATE and DISPLAY: 360 Degree Scan of FOUR WALLS")
    #  CREATE 360 Degree TEST WALL EVENLY SPACED MAX DISTANCE r-theta READINGS
    dist_l,ang_l = create360TestWallData( dist_to_walls=25, items=48)
    # display_values(dist_l,ang_l)
    #  DISPLAY DATA in 180 character width
    view360(dist_l, ang_l, grid_width=60, units="cm")

    print("\n\nCREATE and DISPLAY: 360 Degree Scan of FOUR WALLS with 15% SENSOR ERRORS")
    #  CREATE 360 Degree TEST WALL EVENLY SPACED MAX DISTANCE r-theta READINGS
    dist_l,ang_l = create360TestWallData( dist_to_walls=25, items=48, sensor_error_pct=15)
    # display_values(dist_l,ang_l)
    #  DISPLAY DATA in 180 character width
    view360(dist_l, ang_l, grid_width=60, units="cm")




if __name__ == "__main__":
    main()
