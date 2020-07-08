# GoPiGo3 Path Map and Occupancy Grid

# Based on BigFaceRobotics Big Wheel Bot
- video: https://www.youtube.com/watch?v=LcqCLlF2qpE
- code: https://github.com/BigFace83/Big-Wheel-Bot
- brought down with "git clone https://github.com/BigFace83/Big-Wheel-Bot.git"
- Big Wheel Bot is a
  - remote controlled Arduino based bot with encoder odometry
  - RPi reads csv "cmd_data" from remote control and HC05 Ultrasonic sensor via serial connection 
  - RPi sends csv cmd_data unchanged to Arduino via usb serial
    -  data0,data1,data2,data3,data4_shutdownPi,data5_recording
  - Raspberry Pi based camera, ultrasonic range sensor, (and IR range sensor)
    - Logs a time-stamped line of odometry and sensor readings to <timestamp>/Data.txt
    - Captures a camera frame for every time-stamped log entry to <timestamp>/<timestamp>.avi
    - Data.txt Format (comma separated):
      LeftEnc, RightEnc, yaw, FrontSonar, RearSonar, LeftIR, RightIR, Servo1, Servo2
    - Valid Sonar Readings are < 5000
    - Left IR points fwd + 45 degrees
    - Right IR points fwd - 45 degrees
  - Big_Wheel_Pi.py
```
    - loop 
      read cmd_data from HC05 Ultrasonic sensor,and remote buttons 
      send cmd_data to Arduino 
      read Arduino Data
      save a video frame to datetime_str/datetime_str.avi
      write Arduino Data to datetime_str/Data.txt file
      at 5 frames/second
```




# GoPiGo3 Relevant Metrics:
- Distance Sensor Beam Width: 25 deg, Max range 3000 mm
- PiCam v1.3 Horizontal FoV: 53.5 degrees
- GoPiGo3 (Carl) Spin Radius: 14cm ctr "axle" to corner
                 Orbit Radius: 19cm ctr wheel to opposite corner
- Occupancy Grid Size = 30cm to allow GoPiGo3 360 degree spin inside cell

# Requirements:
- install vlc to see .avi files


# FILE: carlDataLogger.py
PURPOSE: Collect sensor data while user drives bot with keyboard
```
USAGE: carlDataLogger.py [-h] [-fps FPS] [-d]

optional arguments:
  -h, --help           show this help message and exit
  -fps FPS, --fps FPS  video [4] frames with data capture per second
  -d, --display        optional display video
```

- Initializes keyboard controlled bot and sensors
- Creates directory ./<start_datetime_str>/
- Opens ./<start_datetime_str>/Data.txt for recording sensor data 
- Loops approximately 4 fps times per second
  - reads sensors
  - writes (timestamp precision is 1ms):
    timestamp, l_enc, r_enc, imu_hdg, pan_ang, ds_mm
  - adds 320x240 pixel frame from picam to start_datetime_str.avi
  - checks kbd for command, executes command (non-blocking)
  - Optional -d or --display will show picam frames during execution
    (if started in RPi desktop command shell)
- Stop recording data and video with /<ESC/> key
- Use VLC from Raspbian For Robots Web Desktop or vnc/remote RPi desktop to view avi file
- Records Camera at 320x240 at [-fps 4] to start_datetime_str/start_datetime_str.avi
- Records datetime_str, l_enc, r_enc, imu_heading, servo angle, range for each frame to Data.txt
- Uses kbd_easygopigo3.GoPiGo3WithKeyboard class to control the bot and pan servo mounted range sensor
- Quits when Esc key pressed

- USAGE:  ./carlDataLogger.py [-fps 4] [-d or --display] [--help]
- NOTE:   On RPi 3B, 4 fps is maximum for accurate interval data and video 


# FILE: kbd_egpg3_run_this.py
PURPOSE: Tests kbd_easygopigo3.py (without data logging)
USAGE: ./kbd_egpg3_run_this.py



# FILE: kbd_easygopigo3.py
PURPOSE: Keyboard Controlled GoPiGo3 Class w/Servo Support
USAGE: See / run    kbd_egpg3_run_this.py
BASED ON:  Dexter/Projects/BasicRobotControl

MODIFICATIONS:
- Added monkeypatched tiltpan object (self.tp) 
- Added servo control keys  4:left 12.5 degrees, 5:center + off, 6:right 12.5 degrees
  (based on my TiltPan class)
- Added status line under logo with WheelDia, WheelBaseWidth, Speed, and Voltage
    e.g.    WD: 64.00  WBW: 114.05  SPD: 150  V: 10.7
- Added methods for Arrow Keys 
    Up: fwd 30cm, Dn: bwd 15cm, Left: Spin CCW 90, and Right: Spin CW 90
- Changed <F3> to perform forward 90 degree turn (from one wheel revolution)
- Added  <F5> Clockwise 180 degree spin
- Changed color change key from <INSERT> to <BACKSPACE> (Mac has no insert key)
- All commands non-blocking


OPERATION:
```
   _____       _____ _  _____         ____  
  / ____|     |  __ (_)/ ____|       |___ \ 
 | |  __  ___ | |__) || |  __  ___     __) |
 | | |_ |/ _ \|  ___/ | | |_ |/ _ \   |__ < 
 | |__| | (_) | |   | | |__| | (_) |  ___) |
  \_____|\___/|_|   |_|\_____|\___/  |____/ 
                                            
  WD: 64.00  WBW: 114.05  SPD: 150  V: 10.7
                                            

Press the following keys to run the features of the GoPiGo3.
To move the motors, make sure you have a fresh set of batteries powering the GoPiGo3.

[key w       ] :  Move the GoPiGo3 forward
[key s       ] :  Move the GoPiGo3 backward
[key a       ] :  Turn the GoPiGo3 to the left
[key d       ] :  Turn the GoPiGo3 to the right
[key <SPACE> ] :  Stop the GoPiGo3 from moving
[key <UP>    ] :  Drive forward for 30 cm
[key <DOWN>  ] :  Drive backward for 15cm
[key <LEFT>  ] :  Spin Left/CCW 90 degrees
[key <RIGHT> ] :  Spin Right/CW 90 degrees
[key <F1>    ] :  Drive forward for 10 cm
[key <F2>    ] :  Drive forward for 10 inches
[key <F3>    ] :  Turn Right 90 degrees (only left wheel rotates)
[key <F5>    ] :  Spin Right/CW 180 degrees
[key 1       ] :  Turn ON/OFF left blinker of the GoPiGo3
[key 2       ] :  Turn ON/OFF right blinker of the GoPiGo3
[key 3       ] :  Turn ON/OFF both blinkers of the GoPiGo3
[key 4       ] :  Rotate Servo Left 12.5 degrees
[key 5       ] :  Center Servo
[key 6       ] :  Rotate Servo Right 12.5 degrees
[key 8       ] :  Turn ON/OFF left eye of the GoPiGo3
[key 9       ] :  Turn ON/OFF right eye of the GoPiGo3
[key 0       ] :  Turn ON/OFF both eyes of the GoPiGo3
[key <BACKSPACE>] :  Change the eyes' color on the go
[key <ESC>   ] :  Exit
```


# FILE: path_plot.py
PURPOSE: Analyze Data.txt file to plot position/path estimate from imu and wheel encoders
```
USAGE: path_plot.py [-h] -f FOLDER [-o OUTFILE] [-s SIZE] [-v] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -f FOLDER, --folder FOLDER
                        path to data folder
  -o OUTFILE, --outfile OUTFILE
                        optional write final path map to OUTFILE (.png best)
  -s SIZE, --size SIZE  optional map size [400] in cm
  -v, --verbose         optional verbose DEBUG mode
  -d, --display         optional display path during analysis
```

# FILE: sensorModel.py
PURPOSE: provides occupancy probability map for: 
  - sensor with angular beam width, such as ultrasound or ToF IR Laser distance sensor
  - sensor with coherent beam, such as LIDAR

USAGE:  
```
    import sensorModel
    grid_map, occ = sensorModel.BeamModel(...)
    # see file for parameters and example usage
```

![sensorModel.BeamModel()](VL53L0X_Sensor_Model.png?raw=true)
