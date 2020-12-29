
# Easy PiCamera Sensor Class For GoPiGo3 Robots

Python3 Class to treat the PiCamera as a unified family of sensors useful in robot programs 

including:
- Left, Front, Right Light Intensity (0-100)
- Motion Detector (Left, Right, Up, Down)
- Color Detector With Color Table ReLearning 
  (Black, Brown, Red, Orange, Yellow, Green, Blue, Violet, White)
- Maximum Intensity area horizontal angle from center and value (0-100)  
- 320x240 RGB image save to JPEG file or retrieve as numpy array

Refresh rate is roughly 10 per second.

# To Bring Down To Your GoPiGo
```
wget https://github.com/slowrunner/Carl/raw/master/Projects/EasyPiCamSensor/EasyPiCamSensor.tgz 
tar -xzvf EasyPiCamSensor.tgz
```

# Requirements

Python Requirements (**All come in the stock ModRobotics Rasbian_For_Robots**):  
- Python3
- picamera
- threading
- colorsys
- PIL  
- numpy
- espeakng
- math
- json
- traceback
- datetime
- os
- PIL  (Python Image Lib)
- time
- io
- builtins
- (Does not use/require OpenCV)

Other Requirements:  
- GoPiGo3 for some example programs
- (Sensor does not require GoPiGo3)  

Note:  The tgz contains a version of easygopigo3.py with a working steer(lft_pct,rt_pct) method  
- For use with the Braitenberg Vehicle examples  
- The current ModRobotics easygopigo3.py steer() method has a problem. 

# ARCHITECTURE
```
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
```

# API

-  epcs = easypicamsensor.EasyPiCamSensor()   
   *  Create and start Easy Pi Camera Sensor object
   *  Read values from config_easypicamsensor.json if exists

-  light() # return average intensity across entire sensor (0.0 pitch black to 100.0 blinding light)

-  light_left_right() # return average intensity across left half and right half of sensor

-  color() # returns estimate of color of central area of sensor using "RGB" method

-  color_dist_method(method="RGB") # returns nearest color with distance and method ("RGB" or "HSV") used 

-  motion_dt_x_y() # returns time of first motion left|right and/or up|down since last method call

-  motion_dt_x_y_npimage() # returns details and image of first motion left|right and/or up|down since last method call

-  max_ang_val()  # returns the horizontal angle from centerline (+/- half FOV, left negative) of bright area and max intensity (0-100)  

-  save_image_to_file(npimage=None,fn="capture.jpg")  # saves passed or last frame to file encoded as JPEG

-  get_image()  # returns RGB numpy image array

-  learn_colors(tts_prompts=False) # learn one or more colors with optional TTS prompting

-  print_colors() # print the current color table

-  known_color(color_name) # returns True if color_name is in the current color table

-  delete_color(color_name) # removes a color from the (local copy) EasyPiCamSensor object color table  
   (must then call save_colors() to make it permanantly gone)  

-  save_colors(path="config_easypicamsensor.json") # save color table in file [default: config_easypicamsensor.json]  
   (Probably a good idea to save to a .json.test file to protect the existing config file; So use responsibly.)

-  read_colors()  # reads color table from config_easypicamsensor.json file

-  save_config(dataname,datavalue,path="config_easypicamsensor.json")   # save a value or variable in the conf file  
     e.g:  epcs.save_config("vflip",True) for later retrieval with vflip = epcs.get_config("vflip")  
           epcs.save_config("my_color_array",my_color_array) for later retrieval with my_color_array = epcs.get_config("my_color_array")

-  get_config(dataname=None,path="config_easypicamsensor.json")  # retrieve a value or entire config dictionaryfrom config file if exists

-  get_all_data()  # returns dict with all "by-frame" data

-  print_all_data()  # convenience prints dict returned by get_all_data()


# EasyPiCamSensor Example Programs:

- read_sensor.py
  * Reads all "by-frame" data from sensor 10 times per second and pretty prints with headings every 15 readings

```
xmove ymov     latch_move_time      l_x  l_y       frame_time        color   rgb   dist    hsv    dist  left   whole  right  maxAng   val
 none none 2020-12-29 00:26:04.60  left none 2020-12-29 00:26:09.10  Black  Black  64.53  Brown  14.24  24.98  18.48  11.99 (-23.94, 80.78)
 none none                         none none 2020-12-29 00:26:09.20  Black  Black  63.73  Brown  14.90  24.98  18.48  11.99 (-23.94, 81.57)
```

- i_see_color.py [-h] [-v]
  * Uses EasyPiCamSensor.color() and optionally [-v] espeakng TTS to report estimate color seen
  * User selects either RGB or HSV color matching method (RGB is much better than HSV)
  * Target_Colors.pdf provides color samples that match the default sensor color table 
    (Print on matte photo paper for best results)

![Target Color Samples](Graphics/Target_Colors_Tiny.png?raw=true)

- i_see_light.py
  * Comments when someone turns a room light on or off

- i_see_motion.py [-h] [-v]
  * Reports first motion and datatime since last report
  * Recognizes left or right, up or down motion
  * Option [-v] adds TTS reports

- i_see_colors_in_motion.py [-h] [-v]
  * Prints and optionally [-v] speaks last motion and color 
  * Saves image of motion to motion_capture-YYYY-MM-DD_HH_MM_SS.jpg
  * Note: Image may not catch a fast moving object 

![Color and Motion Detect With Image Save](Graphics/motion_capture.jpg)

- face_the_light.py [-h] [-v]
  * Turns GoPiGo3 robot to face the brightest area in room
  * Option [-v] narrates with Text-To-Speech

- braitenberg2B.py [-h] [-v] [-g N.n] [-s]
  * implements Braitenberg Vehicle 2B "loves light"
  * Uses left and right light intensity as stimulus for the opposite side wheel
  * Implementation adds obstacle inhibition of forward motion for vehicle protection
  * Option [-v] narrates with Text-To-Speech
  * Option [-g N.n] introduces stimulus amplification with given gain.  [Default 1.0]
  * Option [-s]  pops window on desktop every few seconds showing robot view  
    (This option only works from command shell on robot's desktop)

![Braitenberg Vehicle 2B using EasyPiCamSensor.light_left_right()](Graphics/Braitenberg2b_Light_Value_Stimulus.png)

[Video: GoPiGo3 "Carl" w/EasyPiCamSensor Braitenberg Vehicle 2B](https://vimeo.com/493585330)

- simple_braitenberg2A.py
  * implements Braitenberg Vehicle 2A "loves the dark" 
  * Uses left and right light intensity as stimulus for the same side wheel
  * Implementation adds obstacle inhibition of forward motion for vehicle protection
  * (Does not use TTS)

- teach_me_colors.py
  * Allows adding or re-learning one or more colors 

- delete_a_color.py
  * Allows testing and easily deleting a poor performing color from the config_easypicamsensor.json file


# Credits

- Color sensing based on work of Nicole Parrot  
  https://github.com/CleoQc/GoPiGoColorDetection

- Motion / Gesture Detection based on the work of Dave Jones at https://github.com/waveform80/picamera_demos

# DISCLAIMER

There are certainly more elegant ways of doing this.  
This is the best I could do with my limited understanding of Python and the Pi Camera.

This code comes with no warranty of correct function.  

If you think it should do something it doesn't,  
or shouldn't do something it does,  
you should know this was a learning experience for me,  
**It is not a product.  I am not interested in maintaining it for you!**

**If you know how to make it better, create a pull request.**  
Perhaps I will learn how to merge other people's code.

- I should have investigated http://www.brucelindbloom.com/index.html?ColorDifferenceCalcHelp.html  
  for better color distance calculation.
