# Multi-threaded PiCamera Processing with OpenCV

From: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/

Config:  RPi 3B 320x240 32fps source, no display, "no processing on image"

pi@Carl:~/Carl/Examples/OpenCV/increasing-RPi-FPS $ python3 picamera_fps_demo.py 
[INFO] sampling frames from `picamera` module...
[INFO] elasped time: 3.84
[INFO] approx. FPS: 26.33
[INFO] sampling THREADED frames from `picamera` module...
[INFO] elasped time: 0.44
[INFO] approx. FPS: 225.05

Result: 
32 fps is one frame every 31.25ms
 
The single thread handling with no processing of a frame 
   steals an extra 3.84ms per frame,
   bringing the "max grab rate" down to 26 fps

Multi-threaded handling, again with no processing of a frame,
   allows a "max grab rate" of 225fps meaning 
   frame handling requires 4.4ms before processing,
   allowing 31.25-4.4 = 26.81ms of processing time per frame.




