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
from di_sensors.easy_mutex import ifMutexAcquire, ifMutexRelease
import os
from picamera import PiCamera
from picamera.array import PiMotionAnalysis
from threading import Thread
from time import sleep
import datetime as dt
# import matplotlib.image as mplimg
# import matplotlib.pyplot as mplplt
import colorsys
from PIL import Image
import io

PROG_NAME = os.path.basename(__file__)

IMAGE_DIMS = (320,240)
stream_width = 320
stream_height = 240
stream_framerate = 10
QUEUE_SIZE = 3  # (10) number of consecutive frames to analyse for motion
THRESHOLD = 1.0  # (4.0) minimum average motion required



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

def normalize_0_to_255(val):
    if val >= 255:
        n = 100.0
    if val < 0: 
        n = 0.0
    else:
        n = val/2.55  # (value div 255) times 100
    return n

def nearest_color(query, subjects=color_rgb ):
    estimate = min( subjects  , key = lambda subject: sum( (s - q) ** 2 for s, q in zip( subject, query ) ) )
    return estimate[3]


def dominant_color(image):
    print("not implemented yet")


def make_test_array(value=(0,0,0),dims=IMAGE_DIMS):
     a = np.full((3,2,3),[255,255,255])
     print("a{}".format(list(a.shape)))
     print(a)
     return a


#------------------------------------------------------------------------------

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

        if (self._latch_move_time == None) and ((self._x_move != 'none') or (self._y_move != 'none')):
             self._latch_move_time = dt.datetime.now()
             self._latch_x_move = self._x_move
             self._latch_y_move = self._y_move
             # print('MyGestureDetector.analyse() Motion Latched: {} {} {}'.format(
             #                self._latch_move_time, self._latch_x_move, self._latch_y_move))


        # Update the display
        # if (self._x_move != 'none') or (self._y_move != 'none'):
        #    print('MyGestureDetector.analyse(): %s %s' % (self._x_move, self._y_move))


    def reset_motion_latch(self):
        self._latch_x_move = 'none'
        self._latch_y_move = 'none'
        self._latch_move_time = None


    def get_motion_latch(self):
        lxm = self._latch_x_move
        lym = self._latch_y_move
        lmt = self._latch_move_time
        self.reset_motion_latch()
        return lmt, lxm, lym

"""
with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 24
    with MyGestureDetector(camera) as gesture_detector:
        camera.start_recording(
            os.devnull, format='h264', motion_output=gesture_detector)
        try:
            while True:
                camera.wait_recording(1)
        finally:
            camera.stop_recording()

"""





#------------------------------------------------------------------------------
class PiGestureStream:
    '''
    Create a picamera in memory video stream and
    start an update() thread to get a frame, and maintain analysis variables
    _color: from {"Black", "Brown", "Red", "Orange", "Yellow", "Green", "Blue", "Violet", "White"}
    _light_ave_intensity: from {0-100, 999 unknown}

    to which mutex protected access is provided by:
    get_color()
    get_light()
    get_light_left_right()
    get_frame()

    '''
    def __init__(self, resolution=(stream_width, stream_height),
                 framerate=stream_framerate,
                 rotation=0,
                 hflip=False, vflip=False,
                 use_mutex=True):
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
        self.use_mutex = use_mutex

    def start(self):
        ''' start the thread to read frames from the video stream'''
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        sleep(5)  # let camera warm up
        self.camera.exposure_mode = 'off'
        return self

    def update(self):
        ''' keep looping infinitely until the thread is stopped'''
        """
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            ifMutexAcquire(self.use_mutex)
            self.frame = f.array
            self.rawCapture.truncate(0)
            # if the thread indicator variable is set, stop the thread
            # and release camera resources
            self.set_color()
            self.set_light_ave_intensity()
            self.set_light_left_right()
            ifMutexRelease(self.use_mutex)

            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return
        """
        while True:
            try:
                stream = io.BytesIO()    # stream to hold jpeg frames
                self.camera.wait_recording(1)
                stream.truncate(0)
                self.camera.capture(stream, format='jpeg', use_video_port=True)
                stream.seek(0)
                jpeg_image = Image.open(stream)
                self.frame = np.asarray(jpeg_image)
                ifMutexAcquire(self.use_mutex)
                self.set_color()
                self.set_light_ave_intensity()
                self.set_light_left_right()
                ifMutexRelease(self.use_mutex)

            except Exception as e:
                 print("update(),wait_recording() Exception")
                 print(str(e))
                 self.camera.stop_recording()
                 self.camera.close()
                 return
            if self.stopped:
                # self.stream.close()
                # self.rawCapture.close()
                self.camera.stop_recording()
                self.camera.close()
                return

    def get_frame(self):
        ''' return the frame most recently read '''
        ifMutexAcquire(self.use_mutex)
        image = self.frame
        ifMutexRelease(self.use_mutex)
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
            h,w,rgb = image.shape
            center_pixel = tuple(image[ int(h/2), int(w/2) ])
            center_pixel_hsv = colorsys.rgb_to_hsv(*center_pixel)
            center_pixel_hsv = (int(center_pixel_hsv[0]*360), int(center_pixel_hsv[1]*100), center_pixel_hsv[2])
            if verbose: print("**** center_pixel - rgb:{} hsv: {}".format(center_pixel, center_pixel_hsv))
            # print("nearest hsv color", nearest_color(center_pixel_hsv,color_hsv))
            # ifMutexAcquire(self.use_mutex)
            self._color = nearest_color(center_pixel)
            # print("nearest rgb color", self._color)
            # print("center_pixel[:]:",center_pixel[:])

        except Exception as e:
            print("color(): {}".format(str(e)))
            pass
        finally:
            # ifMutexRelease(self.use_mutex)
            pass

    def get_color(self):
        ifMutexAcquire(self.use_mutex)
        color = self._color
        ifMutexRelease(self.use_mutex)
        return color

    def set_light_ave_intensity(self):
        try:
            image = self.frame
            pixAverage = np.average(image[...,1])
            # print ("Light Meter pixAverage: {:.1f}".format(pixAverage))
            self._light_ave_intensity = normalize_0_to_255(pixAverage)
        except Exception as e:
            print("light(): {}".format(str(e)))
            self._light_ave_intensity = 999
            pass

    def get_light(self):
        ifMutexAcquire(self.use_mutex)
        light = self._light_ave_intensity
        ifMutexRelease(self.use_mutex)
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
            print("set_light_left_right(): {}".format(str(e)))
            pass

    def get_light_left_right(self):
        ifMutexAcquire(self.use_mutex)
        light_left = self._light_left_ave_intensity
        light_right = self._light_right_ave_intensity
        ifMutexRelease(self.use_mutex)
        return light_left,light_right

    # read current latched motion state, and reset to none
    def get_motion_dt_x_y(self):
        ifMutexAcquire(self.use_mutex)
        latch_motion_time,motion_x,motion_y = self.gesture_detector.get_motion_latch()
        ifMutexRelease(self.use_mutex)
        return latch_motion_time,motion_x,motion_y




class EasyPiCamSensor():
    '''
    Class for interfacing with the Pi Camera as a basic light sensor
    '''

    def __init__(self,use_mutex=True):
        """
        Constructor for initializing the Pi Camera as a basic sensor
        """

        self.use_mutex = use_mutex
        self._dominant_colors = []

        print("Initializing PiCam Video Stream")
        self.stream = PiGestureStream()
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


    def save_image_to_file(self,fn='capture.jpg'):
        ifMutexAcquire(self.use_mutex)
        try:
            image = self.stream.get_frame()
            pilimage = Image.fromarray(image)
            pilimage.save(fn)
        except Exception as e:
            print("save_image_to_file({}) failed".format(fn))
            print(str(e))
            fn=None
        finally:
            ifMutexRelease(self.use_mutex)
        return fn

    def get_image(self):
        ifMutexAcquire(self.use_mutex)
        try:
            image = self.stream.get_frame()
            # pilimage = Image.fromarray(image)
        except Exception as e:
            print("get_image() failed")
            print(str(e))
            # pilimage = None
            image = None
        finally:
            ifMutexRelease(self.use_mutex)
        return image



    def pause(self):
        ifMutexAcquire(self.use_mutex)
        try:
            result = self.stream.stop()
        except Exception as e:
            print("EasyPiCamSensor pause()) failed")
            print(str(e))
        finally:
            ifMutexRelease(self.use_mutex)


    def resume(self):
        try:
            result = self.stream.start()
        except Exception as e:
            print("EasyPiCamSensor resume()) failed")
            print(str(e))
        finally:
            ifMutexRelease(self.use_mutex)






# Test main
def main():
    try:
        epcs = EasyPiCamSensor()
    except Exception as e:
        print("Failed to instantiate and start EasyPiCamSensor object")
        print(str(e))
        exit(1)

    # Test video class
    try:
        for i in range(60):
            print("light(): {:.1f}".format(epcs.light()))

            left_half,right_half = epcs.light_left_right()
            print("light_left_right():  {:.1f},  {:.1f}".format(left_half,right_half))

            print("color(): {}".format(epcs.color()))

            epcs.save_image_to_file("capture.jpg")
            sleep(1)


        epcs.pause()
        print("PiCam Sensor paused for 60 seconds")
        sleep(60)
        epcs.resume()
        print("PiCam Sensor resumed")
        for i in range(60):
            print("\n")
            print("light(): {:.1f}".format(epcs.light()))
            print("color(): {}".format(epcs.color()))
            sleep(1)


    except KeyboardInterrupt:
        print("\n Exiting")


if (__name__ == '__main__'):  main()

