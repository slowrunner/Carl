# Easy PiCamera Sensor Class For GoPiGo3 Robots

Python3 Class to treat the PiCamera as a unified family of GoPiGo3 robot sensors 

including:
- Left, Front, Right Light Intensity (0-100)
- Motion Detector (Left, Right, Up, Down)
- Color Detector With Color Table ReLearning 
  (Black, Brown, Red, Orange, Yellow, Green, Blue, Violet, White) 
- 320x240 RGB image save to JPEG file or retrieve as numpy array

Refresh rate is roughly 10 values per second.

Python Requirements:
- ModRobotics di_sensors.easy_mutex 
- picamera
- threading
- colorsys
- PIL  
- numpy
- (Does not use/require OpenCV)


EasyPiCamSensor Examples:

- i_see_color.py uses EasyPiCamSensor.color() and optionally espeakng TTS to report estimate color seen
  * Target_Colors.pdf provides color samples that match the default sensor color table 

![Target Color Samples](Graphics/Target_Colors_Tiny.png?raw=true)

- light_commentary.py uses EasyPiCamSensor.light() to report relative light increase and decrease
- i_see_motion.py  uses EasyPiCamSensor.motion() to report left, right, up, or down motion seen
- i_see_colors_in_motion.py demonstrates color and motion detection with image save to file
![Color and Motion Detect With Image Save](Graphics/motion_capture.jpg)

- braitenberg2B.py  uses EasyPiCamSensor.light_left_right() to implement Braitenberg Vehicle 2B 
  * (with adjustable gain and obstacle inhibition) 
  * on a ModRobotics GoPiGo3 with ModRobotics Distance Sensor
![Braitenberg Vehicle 2B using EasyPiCamSensor.light_left_right()](Graphics/Braitenberg2b_Light_Value_Stimulus.png?raw=true)

- face_the_light.py uses EasyPiCamSensor.light() and the GoPiGo3 robot to find and face brightest light source

# API

-  epcs = easypicamsensor.EasyPiCamSensor(use_mutex=True)   # Create sensor object

-  light() # return average intensity across entire sensor (0.0 pitch black to 100.0 blinding light)

-  light_left_right() # return average intensity across left half and right half of sensor

-  color() # returns estimate of color of central area of sensor

-  motion_dt_x_y() # returns time of first motion left/right and/or up/down since last method call

-  save_image_to_file(fn="capture.jpg")  # saves last image to file encoded as JPEG

-  get_image()  # returns RGB numpy image array

