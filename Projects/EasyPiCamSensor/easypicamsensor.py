#!/usr/bin/env python3

# file: easypicamsensor.py

"""
  DOCUMENTATION:

  Python Class to treat the PiCamera as a unified family of robot sensors

  light() # return average intensity across entire sensor (0.0 pitch black to 100.0 blinding light)

  light.max() # return [max_intensity, percent_width, percent_height], value and relative location in image
  Maybe horizontal angle would be more directly useful?

  light_left_right() # return average intensity across left half and right half of sensor

  color() # returns estimate of color of central area of sensor

  motion_dt_x_y() # returns time of first motion left/right and/or up/down since last method call

  save_image_to_file(fn="capture.jpg")  # saves last image to file encoded as JPEG

  get_image()  # returns RGB numpy image array


  Motion Detection and camera stream based on https://github.com/waveform80/picamera_demos/blob/master/gesture_detect.py

"""
import numpy as np
import os
from picamera import PiCamera
from picamera.array import PiMotionAnalysis
from threading import Thread, Lock
from time import sleep
import datetime as dt
# import matplotlib.image as mplimg
# import matplotlib.pyplot as mplplt
import colorsys
from PIL import Image, ImageOps
import io
import traceback
import csv
import json


PROG_NAME = os.path.basename(__file__)

IMAGE_DIMS = (320,240)
DEFAULT_H_FOV = 55.5  # horizontal FOV of PiCamera v1.13
stream_width = 320
stream_height = 240
stream_framerate = 10
QUEUE_SIZE = 3  # (10) number of consecutive frames to analyse for motion
THRESHOLD = 1.0  # (4.0) minimum average motion required


# ===== Utility Methods ====

def normalize_0_to_255(val):
    if val >= 255:
        n = 100.0
    if val < 0: 
        n = 0.0
    else:
        n = val/2.55  # (value div 255) times 100
    return n




# ===== numpy image based color code ======

# colors from https://github.com/slowrunner/Carl/blob/master/Projects/EasyPiCamSensor/Target_Colors.pdf
# printed on matte paper captured in diffuse sunlight through window.
# Useful Color Calculator: https://www.rapidtables.com/convert/color/index.html

color_rgb = ( ( 55, 48, 65, "Black"),
              (145, 88, 55, "Brown"),
              (190, 35, 55, "Red"),
              (160, 85, 70, "Orange"),
              (140,120, 0 , "Yellow"),
              ( 80,145, 20, "Green"),
              ( 0 , 90,200, "Blue"),
              (120, 80,140, "Violet"),
              (110,110,140, "White") )


color_hsv = ( ( 0 , 0 , 0 , "Black"),
              ( 30,100, 59, "Brown"),
              ( 0 ,100,100, "Red"),
              ( 30,100,100, "Orange"),
              ( 60,100,100, "Yellow"),
              (120,100, 50, "Green"),
              (240,100,100, "Blue"),
              (300,100, 50, "Violet"),
              ( 0 , 0 , 50, "Gray"),
              ( 0 , 0 ,100, "White") )

def nearest_color(query, subjects=color_rgb ):
    estimate = min( subjects  , key = lambda subject: sum( (s - q) ** 2 for s, q in zip( subject, query ) ) )
    return estimate[3]



def dominant_color(image):
    print("not implemented yet")


# hAngle(targetPixel, hRes, hFOV=DEFAULT_H_FOV)
#             returns horizontal angle off center in degrees
def hAngle(targetPixel, hRes, hFOV=DEFAULT_H_FOV):
    Base = (hRes/2) / np.tan( np.deg2rad( hFOV/2 ))
    dCtr = targetPixel - (hRes // 2)
    leftRight = np.sign(dCtr)    # negative = left, positive = right of center
    xAngle = np.rad2deg( np.arctan( abs(dCtr) / Base ))
    return (leftRight * xAngle)


#  ====== PIL Image based color code ======

# DEFAULT_COLORS by RGB (0-255) and HSV (H:0-359.9 SV:0.0-100 ) values
# [
# ['color', (R,G, B), (h s v)],
# ...
# ]
DEFAULT_COLORS_RGB_HSV = [
['Black' , ( 55,  48,  65), (  0,   0,   0)],
['Brown' , (145,  88,  55), ( 30, 100,  59)],
['Red'   , (190,  35,  55), (  0, 100, 100)],
['Orange', (160,  85,  70), ( 30,  60,  90)],
['Yellow', (140, 120,   0), ( 60, 100, 100)],
['Green' , ( 80, 145,  50), (120, 100,  50)],
['Blue'  , (  0,  90, 200), (240, 100, 100)],
['Violet', (120,  80, 140), (300, 100,  50)],
['White' , (110, 110, 140), (  0,   0, 100)]
]

colors_rgb_hsv = []

def crop_center(img,cropx,cropy):
    # numpy image crop
    # y,x,c = img.shape
    # startx = x//2 - cropx//2
    # starty = y//2 - cropy//2
    # central_image = img[starty:starty+cropy, startx:startx+cropx, :]

    # PIL image crop
    w, h = img.size
    left  = (w - cropx)/2
    top   = (h - cropy)/2
    right = (w + cropx)/2
    bot   = (h + cropy)/2
    central_image = img.crop((left, top, right, bot))

    return central_image




def getrgb(channel):
    '''
    channel is a tuple containing each band.
    Average each band and return as a tuple
    Averages are cast into int as we don't need to be that precise
    '''
    rgb=[]
    avgrgb=[] # average rgb
    for i in range(3):
        rgb.append(list(channel[i].getdata()))
        avgrgb.append(int(sum(rgb[i])/len(rgb[i])))
        # print ("avg rgb:{}".format(avgrgb[i]))
    return (avgrgb[0],avgrgb[1],avgrgb[2])

def gethsv(channel):

    hsv=[]
    avghsv=[] #average hsv
    for i in range(3):
        hsv.append(list(channel[i].getdata()))
        # avghsv.append(sum(hsv[i])/(255.0*len(hsv[i])))
        if i == 0:
            ave = 360 * (sum(hsv[i])/(255.0*len(hsv[i])))
        else:
            ave = 100.0 * (sum(hsv[i])/(255.0*len(hsv[i])))
        avghsv.append( ave )
    print ("gethsv: avg hsv: ({}, {}, {})".format(avghsv[0]),avghsv[1],avghsv[2])
    return ((avghsv[0],avghsv[1],avghsv[2]))


def distance2rgb(incolor,basecolor):
    '''
    calculate the distance between one rgb tuple and another one
    '''
    return math.sqrt((incolor[0] - basecolor[0])**2 + (incolor[1] - basecolor[1])**2 + (incolor[2] - basecolor[2])**2)


def distance2hsv(incolor,basecolor):
    '''
    calculate the distance between one hue and another hue
    problem is white, black, and red all have hue near 0/360
        white = 0, 100,   0
        black = 0,   0,   0
        red   = 0, 100, 100
    When hue is near 0/360, use distance from all three values
    '''
    problem_threshold_lower = 5  # if hue is less than 5 or greater than 350-5 (355)
    problem_threshold_upper = 360 - problem_threshold_lower 
    if (incolor[0] < problem_threshold_lower) or (incolor[0] > problem_threshold_upper) :
        diff = math.sqrt((incolor[0] - basecolor[0])**2 + (incolor[1] - basecolor[1])**2 + (incolor[2] - basecolor[2])**2)
    else:
        diff = abs( (incolor[0] - basecolor[0]) )

    print ("distance2hsv(): color difference is {}".format(diff))
    return (diff)

def nearest_rgbcolor_dist(inrgb,color_table=DEFAULT_COLORS_RGB_HSV):
    '''
    return as string name of, and distance from, the closest known color
    based the RGB values in the known color table
    inrgb is an average RGB tuple
    '''

    studycolor = []  # list of all distances from known colors
    for color in color_table:
        colorBeingEvaluated = color[0]
        rgbBeingEvaluated = color[1]   # rgb tuple
        distance = distance2rgb(incolor,rgbBeingEvaluated)
        print("nearest_rgbcolor_dist(): color {} distance {}".format(colorBeingEvaluated, distance))
        studycolor.append(distance)
    color_table_estimate = color_table[studycolor.index(min(studycolor))]
    color_estimate = color_table_estimate[0]
    color_estimate_distance = min(studycolor)
    print("nearest_rgbcolor_dist(): color estimate: {} distance: {}".format(color_estimate,color_estimate_distance))

    return color_estimate,color_estimate_distance

def nearest_hsvcolor_dist(inhsv,color_table=DEFAULT_COLORS_RGB_HSV):
    '''
    returns a string name of, and distance from, the closest known color 
    based on hsv distance (hue if for h not near 0/360, and whole hsv near 0/360)
    inhsv is a HSV tuple
    '''
    studycolor = []  # list of all distances from known colors
    for color in color_table:
        colorBeingEvaluated = color[0]
        hsvBeingEvaluated = color[2]   # hsv tuple
        distance = distance2hsv(inhsv,hsvBeingEvaluated)
        print("nearest_hsvcolor_dist(): color {} distance {}".format(colorBeingEvaluated, distance))
        studycolor.append(distance)
    color_table_estimate = color_table[studycolor.index(min(studycolor))]
    color_estimate = color_table_estimate[0]
    color_estimate_distance = min(studycolor)
    print("nearest_hsvcolor_dist(): color estimate: {} distance: {}".format(color_estimate,color_estimate_distance))

    return color_estimate,color_estimate_distance


#------------ MY GESTURE DETECTOR ------------------------------------------------------------------
# The analyse method of this class is run on every frame of video
# by the camera object
class MyGestureDetector(PiMotionAnalysis):
    def __init__(self, camera):
        super(MyGestureDetector, self).__init__(camera)
        self.x_queue = np.zeros(QUEUE_SIZE, dtype=np.float)
        self.y_queue = np.zeros(QUEUE_SIZE, dtype=np.float)
        self._x_move = "unknown"
        self._y_move = "unknown"
        self._latch_move_time = None
        self._latch_x_move = 'none'
        self._latch_y_move = 'none'

    # processes each frame for motion
    def analyse(self, a):
        # Roll the queues and overwrite the first element with a new
        # mean (equivalent to pop and append)
        self.x_queue = np.roll(self.x_queue, 1)
        self.y_queue = np.roll(self.y_queue, 1)
        self.x_queue[0] = a['x'].mean()
        self.y_queue[0] = a['y'].mean()
        # Calculate the mean of both queues
        x_mean = self.x_queue.mean()
        y_mean = self.y_queue.mean()
        # Convert left/up to -1, right/down to 1, and movement below
        # the threshold to 0
        self._x_move = ('none' if abs(x_mean) < THRESHOLD else 'right' if x_mean < 0.0 else 'left')
        self._y_move = ('none' if abs(y_mean) < THRESHOLD else 'down'   if y_mean < 0.0 else 'up')

        # if new motion and no prior motion being remembered, save this motion and the datetime it occurred
        if (self._latch_move_time == None) and ((self._x_move != 'none') or (self._y_move != 'none')):
             self._latch_move_time = dt.datetime.now()
             self._latch_x_move = self._x_move
             self._latch_y_move = self._y_move
             # print('MyGestureDetector.analyse() Motion Latched: {} {} {}'.format(
             #                self._latch_move_time, self._latch_x_move, self._latch_y_move))


        # Update the display
        # if (self._x_move != 'none') or (self._y_move != 'none'):
        #    print('MyGestureDetector.analyse(): %s %s' % (self._x_move, self._y_move))

    # forget any remembered motion
    def reset_motion_latch(self):
        self._latch_x_move = 'none'
        self._latch_y_move = 'none'
        self._latch_move_time = None

    # retrieve motion latch variables, forget any prior motion
    def get_motion_latch(self):
        lxm = self._latch_x_move
        lym = self._latch_y_move
        lmt = self._latch_move_time
        self.reset_motion_latch()
        return lmt, lxm, lym



#------------------- Pi Gesture Stream -----------------------------------------------------------
# Creates a Pi Camera Stream that will
# - starts the camera in auto exposure mode to adjust to the current lighting
# - turns off auto exposure after 5 seconds "warm-up"
# - run MyGestureDetector on each frame
# - starts a thread to analyze a camera frame roughly 10 times per second
class PiGestureStream:
    '''
    Create a picamera in memory video stream and
    start an update() thread to get a frame, and maintain analysis variables
    _color: from {"Black", "Brown", "Red", "Orange", "Yellow", "Green", "Blue", "Violet", "White"}
    _light_ave_intensity: from {0-100, 999 unknown}
    _light_max:  

    to which mutex protected access is provided by:
    get_color()
    get_light()
    get_light_left_right()
    get_frame()
    get_max()

    '''
    def __init__(self, resolution=(stream_width, stream_height),
                 framerate=stream_framerate,
                 rotation=0,
                 hflip=False, vflip=False, verbose=False):
        # initialize the camera and stream
        try:
            self.camera = PiCamera()
        except Exception as e:
            print("PiCamera Already in Use by Another Process")
            print("Exiting %s Due to Error" %  PROG_NAME)
            print(str(e))
            exit(1)
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.camera.hflip = hflip
        self.camera.vflip = vflip
        self.camera.rotation = rotation
        # self.rawCapture = PiRGBArray(self.camera, size=resolution)
        # self.stream = self.camera.capture_continuous(self.rawCapture,
        #                                              format="rgb",
        #                                              use_video_port=True)

        self.gesture_detector = MyGestureDetector(self.camera)
        # replace os.devnull, the output parm, to get the actual frames
        self.camera.start_recording(
            os.devnull, format='h264', motion_output=self.gesture_detector)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.thread = None   # Initialize thread
        self.frame = None
        self.stopped = False
        self._color = "unknown"
        self._light_ave_intensity = 999
        self._light_left_ave_intensity = 999
        self._light_right_ave_intensity = 999
        self._light_max_deg_val = (999,999)
        self.verbose = verbose
        self.mutex = Lock()

    def start(self):
        ''' start the thread to read frames from the video stream'''
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        sleep(5)  # let camera warm up
        self.camera.exposure_mode = 'off'
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            try:
                stream = io.BytesIO()    # stream to hold jpeg frames
                self.camera.wait_recording(1)
                stream.truncate(0)
                self.camera.capture(stream, format='jpeg', use_video_port=True)
                stream.seek(0)
                jpeg_image = Image.open(stream)
                self.frame = np.asarray(jpeg_image)
                self.mutex.acquire()
                self.set_color()
                self.set_light_ave_intensity()
                self.set_light_left_right()
                self.set_light_max()
                self.mutex.release()

            except Exception as e:
                print("during or after update(),wait_recording() Exception")
                print(str(e))
                self.camera.stop_recording()
                self.camera.close()
                print("easypicamsensor.update() closed camera, returning")
                return
            if self.stopped:
                self.camera.stop_recording()
                self.camera.close()
                print("easypicamsensor.update() closed camera, returning")
                return

    def get_frame(self):
        ''' return the frame most recently read '''
        try:
            # self.mutex.acquire()
            image = self.frame
            # self.mutex.release()
        except Exception as e:
            print("easypicamsensor.get_frame() Exception:" + str(e))
        return image

    def stop(self):
        ''' indicate that the thread should be stopped '''
        self.stopped = True
        if self.thread is not None:
            self.thread.join()

    def set_color(self,verbose=False):
        try:
            # image = self.stream.get_frame()
            image = self.frame
            # numpy image array method
            h,w,rgb = image.shape
            center_pixel = tuple(image[ int(h/2), int(w/2) ])
            center_pixel_hsv = colorsys.rgb_to_hsv(*center_pixel)
            center_pixel_hsv = (int(center_pixel_hsv[0]*360), int(center_pixel_hsv[1]*100), center_pixel_hsv[2])
            if verbose: print("**** center_pixel - rgb:{} hsv: {}".format(center_pixel, center_pixel_hsv))
            if verbose: print("nearest hsv color", nearest_color(center_pixel_hsv,color_hsv))
            # self.mutex.acquire()
            self._color = nearest_color(center_pixel)
            if verbose: print("nearest rgb color", self._color)
            if verbose: print("center_pixel[:]:",center_pixel[:])

            # PIL image array method
            pilimage = Image.fromarray(np.uint8(image)).convert('RGB')
            central_pixs = crop_center(pilimage,6,6)      # get a 6x6 portion from the image
            central_rgb_channels = central_pixs.split()  # split into three images, one for each R,G,B
            ave_central_rgb = getrgb(central_rgb_channels)
            if verbose: print("ave_central_rgb:",ave_central_rgb)
            central_color = nearest_color(ave_central_rgb)
            if verbose: print("nearest central color",central_color)
            self._color = central_color
        except Exception as e:
            print("easypicamsensor.set_color(): {}".format(str(e)))
            traceback.print_exc()
            pass

    def get_color(self):
        try:
            self.mutex.acquire()
            color = self._color
            self.mutex.release()
        except Exception as e:
            print("easypicamsensor.get_color() Exception:" + str(e))

        return color

    def set_light_ave_intensity(self):
        try:
            image = self.frame
            pixAverage = np.average(image[...,1])
            # print ("Light Meter pixAverage: {:.1f}".format(pixAverage))
            self._light_ave_intensity = normalize_0_to_255(pixAverage)
        except Exception as e:
            print("easypicamsensor.light(): {}".format(str(e)))
            self._light_ave_intensity = 999
            pass

    def get_light(self):
        try:
            self.mutex.acquire()
            light = self._light_ave_intensity
            self.mutex.release()
        except Exception as e:
            print("easypicamsensor.get_light() Exception:" + str(e))
        return light

    def set_light_left_right(self):
        try:
            image = self.frame
            left_half,right_half = np.hsplit(image,2)
            left_half_ave = np.average(left_half[...,1])
            right_half_ave = np.average(right_half[...,1])
            self._light_left_ave_intensity = normalize_0_to_255(left_half_ave)
            self._light_right_ave_intensity = normalize_0_to_255(right_half_ave)
        except:
            print("easypicamsensor.set_light_left_right(): {}".format(str(e)))
            pass

    def get_light_left_right(self):
        try:
            self.mutex.acquire()
            light_left = self._light_left_ave_intensity
            light_right = self._light_right_ave_intensity
            self.mutex.release()
        except Exception as e:
            print("easypicamsensor.get_light_left_right() Exception:" + str(e))
        return light_left,light_right

    # read current latched motion state, and reset to none
    def get_motion_dt_x_y(self):
        try:
            self.mutex.acquire()
            latch_motion_time,motion_x,motion_y = self.gesture_detector.get_motion_latch()
            self.mutex.release()
        except Exception as e:
            print("easypicamsensor.get_motion_dt_x_y() Exception:" + str(e))
        return latch_motion_time,motion_x,motion_y

    def set_light_max(self):
        debug=False
        try:
            npgimage = np.array(Image.fromarray(self.frame).convert('L'))
            if debug:
                pilimage = Image.fromarray(npgimage)
                pilimage.save("grayscaled.jpg")
            pixMax = npgimage.max()
            if debug: print ("Light Max: {}".format(pixMax))
            threshold = int(pixMax - 3)
            [r,c] = np.where(npgimage == pixMax)
            if debug:
                print("set_light_max(): {} points above threshold {}".format(np.size(r), threshold))
                print("r:",r)
                print("c:",c)
            ave_r = int(np.average(r))
            ave_c = int(np.average(c))
            if debug: print("set_light_max(): brightest spot ({},{})".format(ave_r,ave_c))
            width = npgimage.shape[1]
            if debug: print("set_light_max(): image width:",width)
            h_angle_from_centerline = hAngle(ave_c, width, DEFAULT_H_FOV)
            if debug: print("set_light_max(): angle to brightest spot {:.1f}".format(h_angle_from_centerline))
            max_intensity = normalize_0_to_255(pixMax)
            if debug: print("set_light_max(): max_intensity: {:.1f}".format(max_intensity))
            self._light_max_deg_val = (h_angle_from_centerline, max_intensity)
        except Exception as e:
            print("easypicamsensor.set_light_max(): {}".format(str(e)))
            traceback.print_exc()
            self._light_max_deg_val = (999,999)


    def get_light_max_ang_val(self):
        try:
            hangle_deg,max_val = self._light_max_deg_val
        except Exception as e:
            print("easypicamsensor.get_light_max() Exception:" + str(e))
            hangle_deg = 999
            max_val = 999
        return hangle_deg,max_val



class EasyPiCamSensor():
    '''
    Class for interfacing with the Pi Camera as a basic light sensor
    '''

    def __init__(self, verbose = False):
        """
        Constructor for initializing the Pi Camera as a basic sensor
        """

        self._dominant_colors = []
        self.verbose = verbose
        self.colors_rgb_hsv = []
        self.read_colors()
        if self.verbose: print("Initializing PiCam Video Stream")
        self.stream = PiGestureStream(verbose=verbose)
        self.stream.start()

    def motion_dt_x_y(self):
        motion_dt,motion_x,motion_y = self.stream.get_motion_dt_x_y()
        return motion_dt,motion_x, motion_y

    def light(self):
        light_ave_intensity = self.stream.get_light()
        return light_ave_intensity


    def light_left_right(self):
        light_left,light_right = self.stream.get_light_left_right()
        return light_left,light_right


    def color(self,verbose=False):
        color = self.stream.get_color()
        return color

    def max_ang_val(self):
        return self.stream.get_light_max_ang_val()




    def save_image_to_file(self,fn='capture.jpg'):
        try:
            self.stream.mutex.acquire()
            image = self.stream.get_frame()
        except Exception as e:
            print("save_image_to_file(): get_frame failed")
            print(str(e))
            fn=None
        finally:
            self.stream.mutex.release()

        if fn is not None:
            try:
                pilimage = Image.fromarray(image)
                pilimage.save(fn)
            except Exception as e:
                print("easypicamerasensor.save_image_to_file({}) failed".format(fn))
                print(str(e))
                fn = None
        return fn

    def get_image(self):
        try:
            # self.mutex.acquire()
            image = self.stream.get_frame()
        except Exception as e:
            print("easypicamsensor.get_image() failed")
            print(str(e))
            image = None
        finally:
            # self.mutex.release()
            pass
        return image


    def save_colors(self,data=None,path='config_easypicamsensor.json'):
        """
        Write data to a CSV file path
        """
        if data is None: data = self.colors_rgb_hsv

        # with open(path, "w") as csv_file:
        #     writer = csv.writer(csv_file, delimiter=',')
        #     for line in data:
        #         writer.writerow(line)

        self.save_config("colors_rgb_hsv",data,path)


    def read_colors(self,dataname="colors_rgb_hsv",path='config_easypicamsensor.json'):
        '''
        read color definition from config file
        '''

        try:
            self.colors_rgb_hsv = self.get_config(dataname,path)
        except Exception as e:
            print("read_colors() Exception:")
            print(str(e))
            traceback.print_exc()
        if  not self.colors_rgb_hsv:
            print("{} not found in {}".format(dataname,path))
            print("Using DEFAULT_COLORS_RGB_HSV.")
            self.colors_rgb_hsv = DEFAULT_COLORS_RGB_HSV



    def print_colors(self,data=None):
        """
        print color_rgb_hsv data for inclusion as new DEFAULT_COLORS_RGB_HSV
        """
        if data is None: 
            data = self.colors_rgb_hsv
            print('colors_rgb_hsv = [')
        else:
            print('[')

        i = 1
        rows = len(data)
        for row in data:
            print("    [{:<8s},({:>3.0f},{:>3.0f},{:>3.0f}),({:>3.0f},{:>3.0f},{:>3.0f})]".format(
                "'"+str(row[0])+"'",row[1][0],row[1][1],row[1][2],
                                        row[2][0],row[2][1],row[2][2] ),end='')
            if i < rows:
                print(",")   # and a newline
            i += 1
        print("]\n")

    def save_config(self,dataname, datavalue, path='config_easypicamsensor.json'):
        lConfigData = {}
        try:
            lConfigData = self.get_config()
            if lConfigData == None:
               lConfigData = {}
            lConfigData[dataname] = datavalue

            with open(path,'w') as outfile:
                json.dump( lConfigData, outfile )
        except:
            return False
        return True

    def get_config(self,dataname=None,path='config_easypicamsensor.json'):
        try:
            with open(path,'r') as infile:
                lConfigData = json.load(infile)
                if (dataname == None):
                    return lConfigData
                else:
                    return lConfigData[dataname]
        except:
            return None


# ------- TEST MAIN -----
def main():
    print("\nStarting EasyPiCamSensor Test Main")
    try:
        epcs = EasyPiCamSensor(verbose=True)
    except Exception as e:
        print("Failed to instantiate and start EasyPiCamSensor object")
        print(str(e))
        exit(1)

    except KeyboardInterrupt:
        print("\n^C Detected, Exiting")
        exit(0)

    print("colors:")
    epcs.print_colors()

    print("saving colors to config_easypicamsensor.json.test")
    epcs.save_colors(path="config_easypicamsensor.json.test")

    print("reading colors from config_easypicamsensor.json.test")
    epcs.read_colors(path="config_easypicamsensor.json.test")
    print("colors:")
    epcs.print_colors()


    print("light() returns: {:0.1f}".format(epcs.light()))
    light_left,light_right = epcs.light_left_right()
    print("light_left_right() returns: {:0.1f},{:0.1f}".format(light_left,light_right))
    motion_dt,motion_x,motion_y = epcs.motion_dt_x_y()
    print("motion_dt_x_y() returns: {} {} {}".format(motion_dt, motion_x, motion_y))
    print("color() returns: {}".format(epcs.color()))
    h_angle, max_val =  epcs.max_ang_val()
    print("max_ang_val() returns: {:.1f} degrees value: {:.1f} ".format(h_angle,max_val))
    print("saved capture to {}".format(epcs.save_image_to_file()))
    print("\nDone")


if (__name__ == '__main__'):  main()

