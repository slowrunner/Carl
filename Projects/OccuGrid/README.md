Occupancy Grid and Path Map

Based on BigFaceRobotics Big Wheel Bot
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
      LeftEnc, RightEnc, Yaw, FrontSonar, RearSonar, LeftIR, RightIR, Servo1, Servo2
    - Valid Sonar Readings are < 5000
    - Left IR points fwd + 45 degrees
    - Right IR points fwd - 45 degrees
  - Big_Wheel_Pi.py
    - loop
      read cmd_data from HC05 Ultrasonic sensor,and remote buttons
      send cmd_data to Arduino 
      read Arduino Data
      save a video frame to datetime_str/datetime_str.avi
      write Arduino Data to datetime_str/Data.txt file
      at 5 frames/second



File: carlDataLogger.py [-fps 1]
- Initializes bot and sensors
- Creates directory ./<datetime>/
- Opens ./<datetime>/Data.txt for recording sensor data 
- Loops fps times per second
  - reads sensors
  - writes (timestamp precision is 1ms):
    timestamp, l_enc, r_enc, imu_hdg, pan_ang, ds_mm
  - adds frame from pycam to pycam.mp4
- Stop recording data and video with ctrl-c
