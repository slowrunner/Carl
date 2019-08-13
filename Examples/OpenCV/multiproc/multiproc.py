#!/usr/bin/env python3
#
# multiproc.py

"""
Documentation:


Demonstrate using multiprocessing with PiCamera

"""

# from __future__ import print_function # use python 3 syntax but make it compatible with python 2
# from __future__ import division       #                           ''

import sys
try:
    sys.path.append('/home/pi/Carl/plib')
    import speak
    import tiltpan
    import status
    import battery
    import myDistSensor
    import lifeLog
    import runLog
    import myconfig
    import myimutils   # display(windowname, image, scale_percent=30)
    Carl = True
except:
    Carl = False
import easygopigo3 # import the EasyGoPiGo3 class
import numpy as np
import datetime as dt
import argparse
from time import sleep
import os
import io
import cv2
import time
import multiprocessing as mp
from queue import Empty
import picamera
from PIL import Image
import lanes

# ARGUMENT PARSER
# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--file", required=True, help="path to input file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
# ap.add_argument("-l", "--loop", default=False, action='store_true', help="optional loop mode")
# args = vars(ap.parse_args())
# print("Started with args:",args)
# filename = args['file']
# loopFlag = args['loop']

# CONSTANTS


# VARIABLES


# METHODS

class QueueOutput(object):
    def __init__(self, queue, finished):
        print("QueueOutput().init started")
        self.queue = queue
        self.finished = finished
        self.stream = io.BytesIO()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, put the last frame's data in the queue
            size = self.stream.tell()
            if size:
                self.stream.seek(0)
                self.queue.put(self.stream.read(size))
                self.stream.seek(0)
        self.stream.write(buf)

    def flush(self):
        print("QueueOutput().flush started")
        self.queue.close()
        self.queue.join_thread()
        self.finished.set()

def do_capture(queue, finished):
    with picamera.PiCamera(resolution='VGA', framerate=30) as camera:
        output = QueueOutput(queue, finished)
        camera.start_recording(output, format='mjpeg')
        # camera.start_recording(output, format='bgr')
        camera.wait_recording(10)
        camera.stop_recording()
        print("do_capture() ran")

def do_processing(queue, finished):
    while not finished.wait(0.1):
        try:
            stream = io.BytesIO(queue.get(False))
        except Empty:
            print("do_processing(): stream empty")
            pass
        else:
            stream.seek(0)
            #image = Image.open(stream)
            # put image into numpy array
            buff = np.fromstring(stream.getvalue(), dtype=np.uint8)
            image = cv2.imdecode(buff, 1)
            strTime = dt.datetime.now().strftime('%H:%M:%S.%f')[:-3]
            print('%s pid %d do_processing: Processing %dx%d image' % (
            #    strTime, os.getpid(), image.size[0], image.size[1]))
                strTime, os.getpid(), image.shape[0], image.shape[1]))

            # Pretend it takes 0.1 seconds to process the frame; on a quad-core
            # Pi this gives a maximum processing throughput of 40fps
            #time.sleep(0.1)
            cv2.imwrite("carls_lane.jpg", image)
            combo_image = lanes.find_lane_in(image)
            cv2.imwrite("result-{}.jpg".format(strTime),combo_image)
            #cv2.imshow("image",image)
            #cv2.waitKey(0)

# MAIN

def main():
    if Carl: runLog.logger.info("Started")
    try:
        egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    except:
        strToLog = "Could not instantiate an EasyGoPiGo3"
        print(strToLog)
        if Carl: lifeLog.logger.info(strToLog)
        exit(1)
    if Carl:
        myconfig.setParameters(egpg)
        tp = tiltpan.TiltPan(egpg)
        tp.tiltpan_center()
        tp.off()

    try:
        # Do Somthing in a Loop
        loopSleep = 1 # second
        loopCount = 0
        keepLooping = False
        while keepLooping:
            loopCount += 1
            # do something
            sleep(loopSleep)

        # Do Something Once
        queue = mp.Queue()
        finished = mp.Event()
        capture_proc = mp.Process(target=do_capture, args=(queue, finished))
        processing_procs = [
            mp.Process(target=do_processing, args=(queue, finished))
            for i in range(4)
            ]
        for proc in processing_procs:
            proc.start()
        capture_proc.start()
        for proc in processing_procs:
            proc.join()
        capture_proc.join()








    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
