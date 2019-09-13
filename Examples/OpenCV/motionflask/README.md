# Web Streaming OpenCV PiCam Image With Detected Motion Boxed

Based on https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/  

Stream OpenCV video to web browser - applies motion detection

![Carl Video Surveillance](CarlMotionFlask.png?raw=true)


# USAGE:  
 ./webstreaming.py -i ip.ip.ip.ip -o port [-f NN]  (background frames set 32 default)
 (Python3, OpenCV 3.4)

# PERFORMANCE  
  On Raspberry Pi 3B GoPiGo3 Robot:  (PiCamera v1.3 10fps 320x240)  
  
![RPI-Monitor Status](CarlMotionFlaskStatus.png?raw=true)
  

 -  CPU Temperature on GoPiGo3 RPi3B was 59degC when home air cooling active  
    and rose to 72degC when cooling not active (Home at 77degF)

 - CPU Load steady state at 1.7  

 - Ran for 2h10m took battery from 9.5v to 8.4v  

 - Reduced FRAMERATE to 10 fps to limit load and temp stays between 59-71 degC  

 - Full speed 32 fps will climb to throttling point (80degC)  

![CPU Temperature Profile](CarlMotionFlaskTemperature.png?raw=true)

![CPU Load Profile](CarlMotionFlaskCPULoad.png?raw=true)
