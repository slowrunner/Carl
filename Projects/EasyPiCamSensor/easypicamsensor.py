#!/usr/bin/env python3

# file: easypicamsensor.py

"""
  DOCUMENTATION:

  Python Class to treat the PiCamera as a unified family of robot sensors

  Motion Detection and camera stream based on https://github.com/waveform80/picamera_demos/blob/master/gesture_detect.py

  Color Detection based on https://github.com/CleoQc/GoPiGoColorDetection

  API:

    epcs = easypicamsensor.EasyPiCamSensor()
        Create and start Easy Pi Camera Sensor object
        Read values from config_easypicamsensor.json if exists

    light() # return average intensity across entire sensor (0.0 pitch black to 100.0 blinding light)

    light_left_right() # return average intensity across left half and right half of sensor

    color() # returns best estimate of color of central area of sensor using "BEST" method

    color_values_dist_method(method="BEST") # returns nearest color with distance and method ("RGB" or "HSV") used

    motion_dt_x_y() # returns time of first motion left|right and/or up|down since last method call

    motion_dt_x_y_npimage() # returns details and image of first motion left|right and/or up|down since last method call

    max_ang_val() # returns the horizontal angle from centerline (+/- half FOV, left negative) of bright area and max intensity (0-100)

    save_image_to_file(fn="capture.jpg",npimage=None) # saves passed or last frame to file encoded as JPEG

    get_image() # returns RGB numpy image array

    learn_colors(tts_prompts=False) # learn one or more colors with optional TTS prompting

    print_colors() # print the current color table

    known_color(color_name) # returns True if color_name is in the current color table

    delete_color(color_name) # removes a color from the (local copy) EasyPiCamSensor object color table
        (must then call save_colors() to make it permanantly gone)

    save_colors(path="config_easypicamsensor.json") # save color table in file [default: config_easypicamsensor.json]
        (Probably a good idea to save to a .json.test file to protect the existing config file; So use responsibly.)

    read_colors() # reads color table from config_easypicamsensor.json file

    get_config(dataname=None,path="config_easypicamsensor.json")  # retrieves variable or entire dictionary from config file if exists

    save_config(dataname,datavalue,path="config_easypicamsensor.json")   # save a value or variable in the conf file
        e.g:  epcs.save_config("vflip",True) for later retrieval with vflip = epcs.get_config("vflip")
        e.g:  epcs.save_config("my_color_array",my_color_array) for later retrieval with my_color_array = epcs.get_config("my_color_array")

    get_all_data() # returns dict with all "by-frame" data

    print_all_data() # convenience prints dict returned by get_all_data()



  NOTE: The color table colors_hsv_rgb[] can be saved in a JSON config file file,
        which will be read whenever easypicamsensor.EasyPiCamSensor() object is created.
        The color_table is stored and read with RGB and HSV lists (not tuples).

        Using print_colors() will print out the color table with color tuples (because it is easier to read).
        If the user wishes to change the DEFAULT_COLORS_RGB_HSV[] array to be values from config_easypicamsensor.json,
            use the test main() which will read the config_easypicamsensor.json, and call print_colors().
            Copy the color lines into easypicamsensor.py after DEFAULT_COLORS_RGB_HSV = [

  ARCHITECTURE:

  The EasyPiCamSensor class encapsulates  
  - PiCamSensor class:  
    * Creates a thread to run PiCamSensor.update() roughly 10 times per second  
      - PiCamSensor.update() computes average light intensity for the left half, the whole, and the right half of a camera image  
        and estimates what color is present in the central portion of the image by matching RGB values to a table of colors,  
        and estimates what color is present in the central portion of the image by matching HSV values to a table of colors,  
        and computes the horizontal angle from centerline to an thresholded area of brightest pixels  
    * Starts a PiCamera class object which will capture video frames at 10fps  
    * Creates MyGestureDetector for the PiCamera object to analyze motion using three consecutive frames  
      - When MyGestureDetector.analyze() finds new motion it latches the direction of motion and the time it occurred  
        (reading the latched motion clears the latch, ready to hold the next motion event that will occur)

   EasyPiCamSensor <-- PiCamSensor <-- PiCamera  
                                          ^  
                                          |  
                                   <-- MyGestureDetector  

"""
import numpy as np
import os
from picamera import PiCamera
from picamera.array import PiMotionAnalysis
from threading import Thread, Lock
from time import sleep
import datetime as dt
import colorsys
from PIL import Image, ImageOps
import io
import traceback
import json
import math
from builtins import input
import espeakng

PROG_NAME = os.path.basename(__file__)

DEFAULT_H_FOV = 55.5  # horizontal FOV of PiCamera v1.13
stream_width = 320
stream_height = 240
stream_framerate = 10
QUEUE_SIZE = 3  # (10) number of consecutive frames to analyse for motion
THRESHOLD = 1.0  # (4.0) minimum average motion required

_debug = False

# ===== Utility Methods ====

def normalize_0_to_255(val):
    if val >= 255:
        n = 100.0
    if val < 0:
        n = 0.0
    else:
        n = val/2.55  # (value div 255) times 100
    return n


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
    ['Black' ,(  0,  0,  0),(  0,  0,  0)],
    ['Brown' ,( 99, 81, 36),( 43, 63, 39)],
    ['Red'   ,(129, 25, 24),(134, 81, 51)],
    ['Orange',(111,106, 97),( 41, 12, 44)],
    ['Yellow',(130,135,  1),( 62, 99, 53)],
    ['Green' ,( 10, 81, 19),(127, 87, 32)],
    ['Blue'  ,( 27, 60, 91),(209, 70, 36)],
    ['Violet',( 91, 83,105),(261, 21, 41)],
    ['White' ,(123,142,136),(161, 13, 56)]
    ]


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


def get_ave_rgb(channel):
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

def get_ave_hsv(channel):

    hsv=[]
    avghsv=[] #average hsv
    for i in range(3):
        hsv.append(list(channel[i].getdata()))
        # avghsv.append(sum(hsv[i])/(255.0*len(hsv[i])))
        if i == 0:
            ave = round((360 * (sum(hsv[i])/(255.0*len(hsv[i])))),2)
        else:
            ave = round((100.0 * (sum(hsv[i])/(255.0*len(hsv[i])))),2)
        avghsv.append( ave )
    if _debug: print ("get_ave_hsv(): avg hsv: ({:.3f}, {:.3f}, {:.3f})".format(avghsv[0],avghsv[1],avghsv[2]))
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

    # print ("distance2hsv(): color difference is {:.2f}".format(diff))
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
        distance = distance2rgb(inrgb,rgbBeingEvaluated)
        if _debug:
            print("nearest_rgbcolor_dist(): color {} distance {:.2f} from {}".format(colorBeingEvaluated, distance, tuple(rgbBeingEvaluated)))
        studycolor.append(distance)
    color_table_estimate = color_table[studycolor.index(min(studycolor))]
    color_estimate = color_table_estimate[0]
    color_estimate_distance = min(studycolor)
    if _debug:
        print("nearest_rgbcolor_dist(): for color {}".format(inrgb))
        print("nearest_rgbcolor_dist(): color estimate: {} distance: {:.2f}".format(color_estimate,color_estimate_distance))
    color_estimate_distance = round(color_estimate_distance, 2)  # extreme precision might be misleading
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
        if _debug:
            print("nearest_hsvcolor_dist(): color {} distance {:.2f} from {}".format(colorBeingEvaluated, distance, tuple(hsvBeingEvaluated)))
        studycolor.append(distance)
    color_table_estimate = color_table[studycolor.index(min(studycolor))]
    color_estimate = color_table_estimate[0]
    color_estimate_distance = min(studycolor)
    if _debug:
        print("nearest_hsvcolor_dist(): for color {}".format(inhsv))
        print("nearest_hsvcolor_dist(): color estimate: {} distance: {:.2f}".format(color_estimate,color_estimate_distance))
    color_estimate_distance = round(color_estimate_distance, 2)  # extreme precision might be misleading

    return color_estimate,color_estimate_distance


#------------ MY GESTURE DETECTOR ------------------------------------------------------------------
# The analyse method of this class is run on every frame of video
# by the camera sensor object
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


    # return a dictionary with all "by-frame" data
    def all_data(self):
        data_dict = {}
        data_dict["x_move"] = self._x_move
        data_dict["y_move"] = self._y_move
        data_dict["latch_move_time"] = self._latch_move_time
        data_dict["latch_x_move"] = self._latch_x_move
        data_dict["latch_y_move"] = self._latch_y_move
        self.reset_motion_latch()
        return data_dict

#------------------- PiCamSensor -----------------------------------------------------------
# Creates a Pi Camera Sensor that will
# - start the camera in auto exposure mode to adjust to the current lighting
# - turns off auto exposure after 5 seconds "warm-up"
# - run MyGestureDetector on each frame
# - starts a thread to run PiCamSensor.update() on camera frames roughly 10 times per second
class PiCamSensor:

    '''
    Create a picamera in memory video stream and
    start an update() thread to get a frame, and maintain analysis variables

    '''
    def __init__(self, resolution=(stream_width, stream_height),
                 framerate=stream_framerate,
                 rotation=0,
                 hflip=False, vflip=False):
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

        self.gesture_detector = MyGestureDetector(self.camera)
        # replace os.devnull, the output parm, to get the actual frames
        self.camera.start_recording(
            os.devnull, format='h264', motion_output=self.gesture_detector)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.thread = None   # Initialize thread
        self.npframe = None
        self.pilframe = None
        self._dt_frame = None
        self.stopped = False
        self._color_rgb = "unknown"
        self._color_dist_rgb = "999"
        self._color_ave_rgb = (0,0,0)
        self._color_hsv = "unknown"
        self._color_dist_hsv = 999
        self._color_ave_rgb = (0,0.0)
        self._light_ave_intensity = 999
        self._light_left_ave_intensity = 999
        self._light_right_ave_intensity = 999
        self._light_max_deg_val = (999,999)
        self.mutex = Lock()
        self.colors_rgb_hsv = []
        self._latch_move_npimage = None


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
                self.camera.wait_recording(0.025)
                stream.truncate(0)
                self.camera.capture(stream, format='jpeg', use_video_port=True)
                stream.seek(0)
                jpeg_image = Image.open(stream)
                self._dt_frame = dt.datetime.now()
                self.npframe = np.asarray(jpeg_image)
                self.pilframe = jpeg_image.convert('RGB')

                self.mutex.acquire()
                self.set_color()
                self.set_light_ave_intensity()
                self.set_light_left_right()
                self.set_light_max()
                if (self.gesture_detector._latch_move_time is not None) and (self._latch_move_npimage is None):
                    self._latch_move_npimage = self.npframe
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


    def get_npframe(self):
        ''' return the frame most recently read '''
        try:
            # self.mutex.acquire()
            image = self.npframe
            # self.mutex.release()
        except Exception as e:
            print("easypicamsensor.get_npframe() Exception:" + str(e))
        return image


    def stop(self):
        ''' indicate that the thread should be stopped '''
        self.stopped = True
        if self.thread is not None:
            self.thread.join()


    def set_color(self):
        try:
            # PIL image array method
            pilimage = self.pilframe
            central_pixs = crop_center(pilimage,6,6)      # get a 6x6 portion from the image
            central_rgb_channels = central_pixs.split()  # split into three images, one for each R,G,B
            self._color_ave_rgb = get_ave_rgb(central_rgb_channels)
            if _debug: print("color_ave_rgb:",self._color_ave_rgb)
            pil_nearest_rgb_color, pil_nearest_rgb_dist = nearest_rgbcolor_dist(self._color_ave_rgb,self.colors_rgb_hsv)
            self._color_rgb = pil_nearest_rgb_color
            self._color_dist_rgb = pil_nearest_rgb_dist

            central_hsv_channels = central_pixs.convert('HSV').split()
            self._color_ave_hsv = get_ave_hsv(central_hsv_channels)
            if _debug: print("color_ave_hsv: ({:.1f},{:.1f},{:.1f})".format(self._color_ave_hsv[0],self._color_ave_hsv[1],self._color_ave_hsv[2]))
            pil_nearest_hsv_color, pil_nearest_hsv_dist = nearest_hsvcolor_dist(self._color_ave_hsv,self.colors_rgb_hsv)
            self._color_hsv = pil_nearest_hsv_color
            self._color_dist_hsv = pil_nearest_hsv_dist

        except Exception as e:
            print("easypicamsensor.set_color(): {}".format(str(e)))
            traceback.print_exc()
            pass


    def get_color(self):
        try:
            color,values,dist,method = self.get_color_values_dist_method("BEST")
        except Exception as e:
            print("easypicamsensor.get_color() Exception:" + str(e))
        return color


    def get_color_values_dist_method(self,method="BEST"):
        if (method == "RGB"):
            color  = self._color_rgb
            dist   = self._color_dist_rgb
            values = self._color_ave_rgb
        elif (method == "HSV"):
            color  = self._color_hsv
            dist   = self._color_dist_hsv
            values = self._color_ave_hsv
        else:    # method == "BEST" or anything but {"RGB" | "HSV"}
            if ((self._color_rgb == 'Black') or \
                (self._color_rgb == 'White') or \
                (self._color_rgb == 'Red')   or \
                (self._color_rgb == 'Brown')  ):
                color  = self._color_rgb
                dist   = self._color_dist_rgb
                values = self._color_ave_rgb
                method = "RGB"
            else:
                color  = self._color_hsv
                dist   = self._color_dist_hsv
                values = self._color_ave_hsv
                method = "HSV"

        return color,values,dist,method


    def set_light_ave_intensity(self):
        try:
            image = self.npframe
            pixAverage = np.average(image[...,1])
            if _debug: print ("Light Meter pixAverage: {:.1f}".format(pixAverage))
            self._light_ave_intensity = round(normalize_0_to_255(pixAverage),2)
        except Exception as e:
            print("easypicamsensor.light(): {}".format(str(e)))
            self._light_ave_intensity = 999
            pass


    def get_light(self):
        try:
            light = self._light_ave_intensity
        except Exception as e:
            print("easypicamsensor.get_light() Exception:" + str(e))
        return light


    def set_light_left_right(self):
        try:
            image = self.npframe
            left_half,right_half = np.hsplit(image,2)
            left_half_ave = np.average(left_half[...,1])
            right_half_ave = np.average(right_half[...,1])
            self._light_left_ave_intensity = round(normalize_0_to_255(left_half_ave),2)
            self._light_right_ave_intensity = round(normalize_0_to_255(right_half_ave),2)
        except:
            print("easypicamsensor.set_light_left_right(): {}".format(str(e)))
            pass


    def get_light_left_right(self):
        light_left = self._light_left_ave_intensity
        light_right = self._light_right_ave_intensity
        return light_left,light_right


    # read current latched motion state, (throw away image) and reset to none
    def get_motion_dt_x_y(self):
        latch_motion_time,motion_x,motion_y = self.gesture_detector.get_motion_latch()
        motion_image = self.get_motion_image()  # reset the latched image
        return latch_motion_time,motion_x,motion_y


    # read current latched motion image and reset to None
    def get_motion_image(self):
        motion_image = self._latch_move_npimage
        self._latch_move_npimage = None
        return motion_image


    # read current latched motion state with latched motion npimage and reset to none
    def get_motion_dt_x_y_npimage(self):
        latch_motion_time,motion_x,motion_y = self.gesture_detector.get_motion_latch()
        motion_image = self.get_motion_image()  # get any image and reset to None
        return latch_motion_time,motion_x,motion_y,motion_image


    def set_light_max(self):
        try:
            npgimage = np.array(Image.fromarray(self.npframe).convert('L'))
            if _debug:
                pilimage = Image.fromarray(npgimage)
                pilimage.save("grayscaled.jpg")
            pixMax = npgimage.max()
            if _debug: print ("Light Max: {}".format(pixMax))
            threshold = int(pixMax - 3)
            [r,c] = np.where(npgimage == pixMax)
            if _debug:
                print("set_light_max(): {} points above threshold {}".format(np.size(r), threshold))
                print("r:",r)
                print("c:",c)
            ave_r = int(np.average(r))
            ave_c = int(np.average(c))
            if _debug: print("set_light_max(): brightest spot ({},{})".format(ave_r,ave_c))
            width = npgimage.shape[1]
            if _debug: print("set_light_max(): image width:",width)
            h_angle_from_centerline = round(hAngle(ave_c, width, DEFAULT_H_FOV),2)
            if _debug: print("set_light_max(): angle to brightest spot {:.1f}".format(h_angle_from_centerline))
            max_intensity = round(normalize_0_to_255(pixMax),2)
            if _debug: print("set_light_max(): max_intensity: {:.1f}".format(max_intensity))
            self._light_max_deg_val = (h_angle_from_centerline, max_intensity)
        except Exception as e:
            print("easypicamsensor.set_light_max(): {}".format(str(e)))
            traceback.print_exc()
            self._light_max_deg_val = (999,999)


    def get_light_max_ang_val(self):
        hangle_deg,max_val = self._light_max_deg_val
        return hangle_deg,max_val


    def learn_color(self,color_name,debug=_debug):
        try:
            pilimage = self.pilframe
            central_pixs = crop_center(pilimage,32,24)      # get a small portion from the center of the image
            central_pixs.save(color_name+".jpg")
            central_rgb_channels = central_pixs.split()  # split into three images, one for each R,G,B
            self._color_ave_rgb = get_ave_rgb(central_rgb_channels)
            if debug: print("color_ave_rgb: ",self._color_ave_rgb)

            central_hsv_channels = central_pixs.convert('HSV').split()
            self._color_ave_hsv = get_ave_hsv(central_hsv_channels)
            if debug: print("color_ave_hsv: ({:.3f},{:.3f},{:.3f})".format(self._color_ave_hsv[0],self._color_ave_hsv[1],self._color_ave_hsv[2]))

            status = None
            for i in range(len(self.colors_rgb_hsv)):
                if color_name in self.colors_rgb_hsv[i]:
                    old_color = self.colors_rgb_hsv[i]
                    new_color = [color_name, self._color_ave_rgb, self._color_ave_hsv]
                    self.colors_rgb_hsv[i] = new_color
                    status = "Replaced {}".format(color_name)

            if status is None:
                old_color = []
                new_color = [color_name, self._color_ave_rgb, self._color_ave_hsv]
                self.colors_rgb_hsv.append(new_color)
                status = "Added {} ".format(color_name)

            if debug:
                if old_color:
                    print("learn_color({}) replaced:".format(color_name))
                    print("       {}".format(old_color))
                    print("  with {}".format(new_color))
                else:
                    print("learn_color({}) added:".format(color_name))
                    print("       {}".format(new_color))
                print("colors_rgb_hsv:",self.colors_rgb_hsv)
        except Exception as e:
            print("learn_color({}): Exception: {}".format(color_name,str(e)))
            traceback.print_exc()
        return status


    def delete_color(self,color_name):
        try:
            old_color = None
            status = "Color {} not found".format(color_name)
            for i in range(len(self.colors_rgb_hsv)):
                if color_name in self.colors_rgb_hsv[i]:
                    old_color = self.colors_rgb_hsv[i]
                    del self.colors_rgb_hsv[i]
                    status = "Deleted {}".format(color_name)

            if _debug:
                if old_color:
                    print("delete_color({}) deleted {}".format(color_name,old_color))
        except Exception as e:
            status = "delete_color({}): Exception: {}".format(color_name,str(e))
            print(status)
        return status


    def known_color(self,color_name):
        found = False
        try:
            for i in range(len(self.colors_rgb_hsv)):
                if color_name in self.colors_rgb_hsv[i]:
                    found = True
        except Exception as e:
            print("known_color({}): Exception: {}".format(color_name,str(e)))
        return found


    def all_data(self):
        data_dict = self.gesture_detector.all_data()
        data_dict["dt_frame"] = self._dt_frame
        data_dict["color_rgb"] = self._color_rgb
        data_dict["color_dist_rgb"] = self._color_dist_rgb
        data_dict["color_ave_rgb"] = self._color_ave_rgb
        data_dict["color_hsv"] = self._color_hsv
        data_dict["color_dist_hsv"] = self._color_dist_hsv
        data_dict["color_ave_hsv"] = self._color_ave_hsv
        data_dict["light_ave_intensity"] = self._light_ave_intensity
        data_dict["light_left_ave_intensity"] = self._light_left_ave_intensity
        data_dict["light_right_ave_intensity"] = self._light_right_ave_intensity
        data_dict["light_max_deg_val"] = self._light_max_deg_val
        return data_dict




# ------- EASY PI CAMERA SENSOR --------------

class EasyPiCamSensor():
    '''
    Class for interfacing with the Pi Camera as a basic light, color, and motion sensor
    '''

    def __init__(self, resolution=(stream_width, stream_height),
                 framerate=stream_framerate,
                 rotation=0,
                 hflip=False, vflip=False):

        """
        Constructor for initializing the Pi Camera as a basic sensor

        Note: rotation: Valid values are 0, 90, 180, and 270 only.
        """

        if _debug: print("EasyPiCamSensor(): Initializing PiCam Video Stream")
        self.picamsensor = PiCamSensor(resolution=resolution, framerate=framerate, rotation=rotation, hflip=hflip, vflip=vflip)
        self.read_colors()    # get color table from config_easypicamsensor.json or DEFAULT_COLORS_RGB_HSV
        self.picamsensor.start()


    def motion_dt_x_y(self):
        motion_dt,motion_x,motion_y = self.picamsensor.get_motion_dt_x_y()
        return motion_dt,motion_x, motion_y


    def motion_dt_x_y_npimage(self):
        motion_dt,motion_x,motion_y,motion_image = self.picamsensor.get_motion_dt_x_y_npimage()
        return motion_dt,motion_x, motion_y, motion_image


    def light(self):
        light_ave_intensity = self.picamsensor.get_light()
        return light_ave_intensity


    def light_left_right(self):
        light_left,light_right = self.picamsensor.get_light_left_right()
        return light_left,light_right


    def color(self):
        color = self.picamsensor.get_color()
        return color


    def color_values_dist_method(self,method="BEST"):
        color,values,dist,method = self.picamsensor.get_color_values_dist_method(method)
        return color,values,dist,method


    def max_ang_val(self):
        return self.picamsensor.get_light_max_ang_val()


    def save_image_to_file(self,fn='capture.jpg',npimage=None):
        if (npimage is None):
            try:
                self.picamsensor.mutex.acquire()
                npimage = self.picamsensor.get_npframe()
            except Exception as e:
                print("save_image_to_file(): get_npframe failed")
                print(str(e))
                fn=None
            finally:
                self.picamsensor.mutex.release()

        if fn is not None:
            try:
                pilimage = Image.fromarray(npimage)
                pilimage.save(fn)
            except Exception as e:
                print("easypicamerasensor.save_image_to_file({}) failed".format(fn))
                print(str(e))
                fn = None
        return fn


    def get_image(self):
        try:
            # self.mutex.acquire()
            image = self.picamsensor.get_npframe()
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
        if data is None: data = self.picamsensor.colors_rgb_hsv

        self.save_config("colors_rgb_hsv",data,path)


    def read_colors(self,dataname="colors_rgb_hsv",path='config_easypicamsensor.json'):
        '''
        read color definition from config file
        '''
        try:
            self.picamsensor.colors_rgb_hsv = self.get_config(dataname,path)
            if _debug: print("read colors from {}".format(path))
        except Exception as e:
            print("read_colors() Exception:")
            print(str(e))
            traceback.print_exc()
        if  not self.picamsensor.colors_rgb_hsv:
            print("{} or {} not found".format(path,dataname))
            print("Using DEFAULT_COLORS_RGB_HSV.")
            self.picamsensor.colors_rgb_hsv = DEFAULT_COLORS_RGB_HSV


    def print_colors(self,data=None):
        """
        print color_rgb_hsv data for inclusion as new DEFAULT_COLORS_RGB_HSV
        """
        if data is None: 
            data = self.picamsensor.colors_rgb_hsv
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
        print("\n    ]")


    def known_color(self,color_name):
        '''
        Check for color in known color table
        '''
        return self.picamsensor.known_color(color_name)


    def delete_color(self,color_name):
        '''
        Delete color, if it exists, from known color table
        '''
        return self.picamsensor.delete_color(color_name)


    def save_config(self,dataname, datavalue, path='config_easypicamsensor.json'):
        '''
        Save a datavalue into json config file with string dataname
        e.g:  epcs.save_config("vflip",True) for later retrieval with vflip = epcs.get_config("vflip")
        '''

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


    def learn_colors(self,tts_prompts=False,debug=_debug):
        '''
        With optional TTS prompting
        '''
        if tts_prompts:
            tts = espeakng.Speaker()
        color_name = "TBD"
        while color_name != "":
            alert = "Enter Color Name To Learn or just Return to abort: "
            if tts_prompts: tts.say(alert)
            color_name = input(alert)
            if color_name != "":
                alert = "Press Return when ready to learn {}".format(color_name)
                if tts_prompts: tts.say(alert)
                input(alert)
                status = self.picamsensor.learn_color(color_name,debug)
                print(status)
                if tts_prompts: tts.say(status)
            else:
                alert = "Learn colors aborted"
                print(alert)
                if tts_prompts: tts.say(alert)
                break


    # gather all "by-frame" data into a dictionary
    def get_all_data(self):
        data_dict = self.picamsensor.all_data()
        return data_dict


    def print_all_data(self,data_dict):
        for n,v in data_dict.items():
            print("{:<25s} = {}".format(n,str(v)))






# ------- TEST MAIN -----
def main():
    print("\nStarting EasyPiCamSensor Test Main")
    try:
        print("Initializing EasyPiCamSensor() object")
        epcs = EasyPiCamSensor()
        print("EasyPiCamSensor Initialization Complete\n")
    except Exception as e:
        print("Failed to instantiate and start EasyPiCamSensor object")
        print(str(e))
        exit(1)

    except KeyboardInterrupt:
        print("\n^C Detected, Exiting")
        exit(0)

    print("Loaded colors: Tests loading from config_easypicamsensor.json if exists")
    epcs.print_colors()


    # === TEST "updated every frame" methods
    print("light() returns: {:0.1f}".format(epcs.light()))
    light_left,light_right = epcs.light_left_right()
    print("light_left_right() returns: {:0.1f},{:0.1f}".format(light_left,light_right))
    motion_dt,motion_x,motion_y = epcs.motion_dt_x_y()
    print("motion_dt_x_y() returns: {} {} {}".format(motion_dt, motion_x, motion_y))
    print("color() returns: {}".format(epcs.color()))
    color,values,dist,method = epcs.color_values_dist_method()
    print("color_values_dist_method(): returns {} {} {} {}".format(color,values,dist,method))
    h_angle, max_val =  epcs.max_ang_val()
    print("max_ang_val() returns: {:.1f} degrees value: {:.1f} ".format(h_angle,max_val))

    # === TEST Utilities
    print("saved capture to {}".format(epcs.save_image_to_file()))

    print("Test learn_colors() by adding a Gray, for testing delete_color('Gray') next")
    epcs.learn_colors()
    epcs.print_colors()   # print the new table with learned colors

    print("saving colors to config_easypicamsensor.json.test")  # test saving colors
    epcs.save_colors(path="config_easypicamsensor.json.test")
    print("NOTE:  .test at the end - does not overwrite existing config_easypicamsensor.json")

    # Test reading colors from a named file
    print("reading colors from config_easypicamsensor.json.test")
    epcs.read_colors(path="config_easypicamsensor.json.test")
    print("colors:")         # print the colors read from the just written file
    epcs.print_colors()

    # Test known_color utility
    print('Check if "Gray" exists')
    if epcs.known_color("Gray"):
        print("Gray exists in colors_rgb_hsv list")
    else:
        print("Gray not found in colors_rgb_hsv list")

    # Test delete_color()
    print("Test delete Gray")
    status = epcs.delete_color("Gray")
    print(status)

    epcs.print_colors()  # show colors after deleting Gray

    print("get_all_data():")
    all_data_dict = epcs.get_all_data()
    epcs.print_all_data(all_data_dict)


    print("\nDone")


if (__name__ == '__main__'):  main()

