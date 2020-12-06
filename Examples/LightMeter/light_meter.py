#!/usr/bin/env python3

# file: light_meter.py

"""
Use Pi Camera to measure relative light levels

Initializes camera exposure in automatic mode, then prevents exposure change 
to meaure relative light level changes.

$ ./light_meter.py 
Initializing Pi Camera
Light Meter pixAverage: 94.1         <-- Ambient room lighting big window sunny
Light Meter pixAverage: 94.0
Light Meter pixAverage: 93.8
...
Light Meter pixAverage: 155.5      <-- White box 
Light Meter pixAverage: 179.1
Light Meter pixAverage: 180.7
...
Light Meter pixAverage: 21.3       <--  Black box
Light Meter pixAverage: 20.1
Light Meter pixAverage: 25.7
...
Light Meter pixAverage: 244.8    <-- Flashlight shining into Pi Camera
Light Meter pixAverage: 254.0
Light Meter pixAverage: 253.9
...
Light Meter pixAverage: 0.7     <-- Hand over the camera blocking light
Light Meter pixAverage: 0.4
Light Meter pixAverage: 0.7
...
Light Meter pixAverage: 85.3    <-- back to ambient room lighting with cloud
Light Meter pixAverage: 88.8
Light Meter pixAverage: 89.4
^C
Exiting ..

"""
import picamera
import picamera.array
import numpy as np
from time import sleep


def main():
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        with picamera.array.PiRGBArray(camera) as stream:
            camera.exposure_mode = 'auto'
            camera.awb_mode = 'auto'
            print("Initializing Pi Camera")
            sleep(2)
            # turn auto exposure mode off so values reflect light variation
            camera.exposure_mode = 'off'
            while True:
                try:
                    camera.capture(stream, format='rgb')
                    # pixAverage = int(np.average(stream.array[...,1]))
                    pixAverage = np.average(stream.array[...,1])
                    print ("Light Meter pixAverage: {:.1f}".format(pixAverage))
                    sleep(1)
                    # get rid of past frames in stream
                    stream.truncate()
                    stream.seek(0)
                except KeyboardInterrupt:
                    print("\nExiting ..")
                    break

if __name__ == "__main__": main()
