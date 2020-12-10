#!/usr/bin/env python3

# file: easypicamsensor.py

"""
  DOCUMENTATION:

  This class allows simplified access to the Pi Camera as a sensor

  light() # return average intensity across entire sensor (0.0 pitch black to 100.0 blinding light)

  light.max() # return [max_intensity, percent_width, percent_height], value and relative location in image
  Maybe horizontal angle would be more directly useful?

  light_right() # return average intensity across right half of sensor

  light_left() # return average intensity across left half of sensor

  color() # returns estimate of dominant color of central area of sensor

  last_motion() # returns time, direction, magnitude of last motion over theshold

  pause() # minimize processing and battery load

  resume() # use after pause()
"""
import numpy as np
from di_sensors.easy_mutex import ifMutexAcquire, ifMutexRelease
import os
from picamera import PiCamera
from picamera.array import PiRGBArray
import picamera.array
from threading import Thread
from time import sleep
# import matplotlib.image as mplimg
# import matplotlib.pyplot as mplplt
import colorsys
from PIL import Image


PROG_NAME = os.path.basename(__file__)

IMAGE_DIMS = (320,240)
stream_width = 320
stream_height = 240
stream_framerate = 3

# colors from https://www.rapidtables.com/web/color/RGB_Color.html
"""
color_rgb = ( ( 0 , 0 , 0 , "Black"),
              (120,105, 30, "Brown"),
              (255, 0 , 0 , "Red"),
              (255,165, 0 , "Orange"),
              (255,255, 0 , "Yellow"),
              ( 0 ,128, 0 , "Green"),
              ( 0 , 0 ,255, "Blue"),
              (128, 0 ,128, "Violet"),
              (128,128,128, "Gray"),
              (255,255,255, "White") )
"""

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
    n = val/2.55  # (value div 255) times 100
    if n<0: n = 0.0
    if n>100: n = 100.0
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
class PiVideoStream:
    '''
    Create a picamera in memory video stream and
    return a frame when update called
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
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
                                                     format="rgb",
                                                     use_video_port=True)
        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.thread = None   # Initialize thread
        self.frame = None
        self.stopped = False

    def start(self):
        ''' start the thread to read frames from the video stream'''
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        sleep(5)  # let camera warm up
        return self

    def update(self):
        ''' keep looping infinitely until the thread is stopped'''
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)
            # if the thread indicator variable is set, stop the thread
            # and release camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        ''' return the frame most recently read '''
        return self.frame

    def stop(self):
        ''' indicate that the thread should be stopped '''
        self.stopped = True
        if self.thread is not None:
            self.thread.join()

class EasyPiCamSensor():
    '''
    Class for interfacing with the Pi Camera as a basic light sensor
    '''

    def __init__(self,use_mutex=True):
        """
        Constructor for initializing the Pi Camera as a basic sensor
        """

        self.use_mutex = use_mutex
        self._light_ave_intensity = 999
        self._dominant_color = (999 , 999, 999)
        self._color = "unknown"

        print("Initializing PiCam Video Stream")
        self.stream = PiVideoStream()
        self.stream.sensor = self   # make a way for stream to set values in parent
        self.stream.start()


    def light(self):
        ifMutexAcquire(self.use_mutex)
        try:
            image = self.stream.read()
            pixAverage = np.average(image[...,1])
            # print ("Light Meter pixAverage: {:.1f}".format(pixAverage))
            self._light_ave_intensity = normalize_0_to_255(pixAverage)
        except Exception as e:
            print("light(): {}".format(str(e)))
            pass
        finally:
            ifMutexRelease(self.use_mutex)
        return self._light_ave_intensity


    def light_left_right(self):
        ifMutexAcquire(self.use_mutex)
        try:
            image = self.stream.read()
            left_half,right_half = np.hsplit(image,2)
            # print("left_half.shape:", left_half.shape)
            left_half_ave = np.average(left_half[...,1])
            # print ("Light Meter left_half: {:.1f}".format(left_half_ave))
            # print("right_half.shape:", right_half.shape)
            right_half_ave = np.average(right_half[...,1])
            # print ("Light Meter right_half: {:.1f}".format(right_half_ave))
            self._light_left_ave_intensity = normalize_0_to_255(left_half_ave)
            self._light_right_ave_intensity = normalize_0_to_255(right_half_ave)
        except:
            print("light(): {}".format(str(e)))
            pass
        finally:
            ifMutexRelease(self.use_mutex)
        return self._light_left_ave_intensity, self._light_right_ave_intensity

    def color(self,verbose=False):
        ifMutexAcquire(self.use_mutex)
        try:
            image = self.stream.read()
            h,w,rgb = image.shape
            # print("h:{}, w:{}, rgb:{}".format(h,w,rgb))
            # print("image[ {}, {} ] {} ".format(h/2, w/2, tuple(image[0, 0]) ))
            center_pixel = tuple(image[ int(h/2), int(w/2) ])
            # print("center_pixel:", center_pixel)
            self._color = nearest_color(center_pixel)
            # print("nearest rgb color", self._color)
            # print("center_pixel[:]:",center_pixel[:])
            center_pixel_hsv = colorsys.rgb_to_hsv(*center_pixel)
            center_pixel_hsv = (int(center_pixel_hsv[0]*360), int(center_pixel_hsv[1]*100), center_pixel_hsv[2])
            if verbose: print("**** center_pixel - rgb:{} hsv: {}".format(center_pixel, center_pixel_hsv))
            # print("nearest hsv color", nearest_color(center_pixel_hsv,color_hsv))
        except Exception as e:
            print("color(): {}".format(str(e)))
            pass
        finally:
            ifMutexRelease(self.use_mutex)
        return self._color


    def save_image_to_file(self,fn='capture.jpg'):
        ifMutexAcquire(self.use_mutex)
        try:
            image = self.stream.read()
            pilimage = Image.fromarray(image)
            pilimage.save(fn)
        except Exception as e:
            print("save_image_to_file({}) failed".format(fn))
            print(str(e))
            fn=None
        finally:
            ifMutexRelease(self.use_mutex)
        return fn


    def pause(self):
        ifMutexAcquire(self.use_mutex)
        try:
            result = self.stream.stop()
        except Exception as e:
            print("EasyPiCamSensor pause()) failed")
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
        for i in range(15):
            print("light(): {:.1f}".format(epcs.light()))

            left_half,right_half = epcs.light_left_right()
            print("light_left_right():  {:.1f},  {:.1f}".format(left_half,right_half))

            print("color(): {}".format(epcs.color()))

            epcs.save_image_to_file("capture.jpg")
            sleep(1)


        # epcs.pause()
        # print("PiCam Sensor paused")
    except KeyboardInterrupt:
        print("\n Exiting")


if (__name__ == '__main__'):  main()

