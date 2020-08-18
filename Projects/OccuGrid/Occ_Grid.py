import cv2
import numpy as np
import os
import math
import Sensor_Model
import sys


os.chdir('Data/Garden_10_04_20') #Path to data file

Map_Size = 300

Xr = float(Map_Size/2) #Set intial robot position
Yr = float(Map_Size/2)

cellsize = 50 #Set cell width and height in mm
scale = float(1)/cellsize #Set map scale

mm_per_tick = 5 #Encoder resolution

linecount = 0 #Track file line number for debugging

cv2.namedWindow("Sonar Grid Map", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Sonar Grid Map", 100, 100) 

cv2.namedWindow("IR Grid Map", cv2.WINDOW_NORMAL)
cv2.resizeWindow("IR Grid Map", 100, 100) 

cv2.namedWindow("Combined Grid Map", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Combined Grid Map", 1000, 1000) 


cv2.waitKey(10)

Map_log_sonar = np.full((Map_Size,Map_Size),0,np.single) #Log odds occupancy grid map for Sonar data. Initialise all cells to contain 0.
Map_log_IR = np.full((Map_Size,Map_Size),0,np.single) #Log odds occupancy grid map for IR sensor data. Initialise all cells to contain 0.


count = len(open("Data.txt").readlines(  ))
print count

f = open("Data.txt", "r") #Open data file for reading
for line in f: #Step through each line of the data file
    #Each line is a comma separated list of values of the form:
    #LeftEncoder, RightEncoder, Yaw, FrontSonar, RearSonar, LeftIR, RightIR, Servo1, Servo2

    mylist = [int(x) for x in line.split(',')] #Split line into individual values
    
    linecount += 1
    angle = mylist[2] #Robot heading angle
    inv_angle = angle+180 #angle for rear sonar sensor
    avencoder = (mylist[0]+mylist[1])/2 #Distance travelled by robot is approximated to average of both encoder readings
    Fsonar = mylist[3]*10 #Sonar values are in cm, convert to mm by muliplying by 10
    Rsonar = mylist[4]*10
    LIR = mylist[5]*10 #Same for IR sensor values
    RIR = mylist[6]*10

    if Fsonar < 5000:
        Sonar_log, points = Sensor_Model.SonarModel(Map_log_sonar, Xr, Yr, angle, Fsonar, cellsize, scale)
        Map_log_sonar = np.add(Map_log_sonar, Sonar_log)

    if Rsonar < 5000:
        Sonar_log, Rsonarpoints = Sensor_Model.SonarModel(Map_log_sonar, Xr, Yr, inv_angle, Rsonar, cellsize, scale)
        Map_log_sonar = np.add(Map_log_sonar, Sonar_log)
        #points = np.append(points, Rsonarpoints, axis=0)

    IR_log, LIRpoints = Sensor_Model.IRModel(Map_log_IR, Xr, Yr, (angle-45), LIR, cellsize, scale)
    Map_log_IR = np.add(Map_log_IR, IR_log)
    #points = np.append(points, LIRpoints, axis=0)

    IR_log, RIRpoints = Sensor_Model.IRModel(Map_log_IR, Xr, Yr, (angle+45), RIR, cellsize, scale)
    Map_log_IR = np.add(Map_log_IR, IR_log)
    #points = np.append(points, RIRpoints, axis=0)

    Xrnext = Xr + float((math.cos(math.radians(angle)) * (avencoder*mm_per_tick)*scale)) #Calculate new robot position from encoder readings
    Yrnext = Yr + float((math.sin(math.radians(angle)) * (avencoder*mm_per_tick)*scale))

    #cv2.line(map_image, (int(Xr),int(Yr)), (int(Xrnext),int(Yrnext)), 150, 1)

    Xr = Xrnext
    Yr = Yrnext

    #output progress bar to terminal
    
    # the exact output you're looking for:
    percent = float(linecount)/count
    sys.stdout.write('\r')
    sys.stdout.write("{0:1%} ".format(percent))
    sys.stdout.flush()

    Map_P_sonar = 1 - (1/(1+(np.exp(Map_log_sonar)))) #Convert log odds matrix to probability matrix
    Disp_img_sonar = 1-Map_P_sonar #invert image so that free cells are white and occupied cells are black
    cv2.imshow("Sonar Grid Map", Disp_img_sonar)

    Map_P_IR = 1 - (1/(1+(np.exp(Map_log_IR)))) #Convert log odds matrix to probability matrix
    Disp_img_IR = 1-Map_P_IR #invert image so that free cells are white and occupied cells are black
    cv2.imshow("IR Grid Map", Disp_img_IR)

    #Combine IR and sonar arrays by finding the largest value out of each array and adding to new array
    Map_P_Combined = np.where((Map_P_sonar > 0.5) | (Map_P_IR > 0.5), np.maximum(Map_P_sonar, Map_P_IR), np.minimum(Map_P_sonar, Map_P_IR))
    #Map_P_Combined = 1 - ((1-Map_P_sonar)*(1-Map_P_IR))
    Disp_img_Combined = 1-Map_P_Combined #invert image so that free cells are white and occupied cells are black
    cv2.imshow("Combined Grid Map", Disp_img_Combined)
    cv2.waitKey(1)
    #last_scan = np.zeros((Map_log.shape),np.single)
    #for x in points:
    #    Ximg = x[0][0]
    #    Yimg = x[0][1]
    #    last_scan[Yimg][Ximg] = 1
        
    #cv2.imshow("Last Scan", last_scan)
    #cv2.waitKey(1)

    #retval, threshold = cv2.threshold(Disp_img, 0.6, 255, cv2.THRESH_BINARY) #Threshold resulting occ grid map
    

    

cv2.waitKey(0)




