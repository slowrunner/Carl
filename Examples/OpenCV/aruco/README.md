# ArUco Markers

Generate at https://fodi.github.io/arucosheetgen/

REF:  https://pyimagesearch.com/2020/12/21/detecting-aruco-markers-with-opencv-and-python/

Requires:
- pip3 install imutils

```
./aruco_image.py --image images/ArUco_4x4.jpg --type DICT_4X4_50  
```


# Pi Camera Calibration on Raspberry Pi (Python)  

Ref: https://www.youtube.com/watch?v=XFBKwme5HYk  
Raspberry Pi Camera Calibration for ArUco marker detection  

Use https://calib.io/pages/camera-calibration-pattern-generator 
- Checkerboard 279w x 215h, 8 rows x 10 col, 25mm Checker Width  
Print  
- Scale to fit - Fill Entire Paper (94% scaled)  
- Boarderless  
- Paper Handling: Turn off Scale to Fit paper size  

Measure size:  
- 19.4mm high / 8 = 24.25mm  
- 243mm wide / 10 = 24.3 mm  

Paste onto board to make sure it stays flat  

VNC into pi:  
- run cam_cal.py  
- Slowly move board around frame, while:  
  -  changing vertical angle,  
  -  changing horizontal angle,  
  -  changing distance from camera  
  -  changing rotation angle  
  -  in corners, upper, lower, left, and right sides  

View images, delete out of focus, blurred, or not complete board  


Edit process.py  
- set number of squares in width  
- set number of squares in height  
- set width of square in mm (nn.n)  

run process.py to output camera_cal.npy   

Process run on 129 calibration images:  
```
$ ./process.py 
Starting Camera Calibration - may take a while ..
Calibration completed in 780 seconds


Calibration Matrix: 
[[571.56532287   0.         294.09865949]
 [  0.         572.77403431 228.00153078]
 [  0.           0.           1.        ]]
Distortion:  [[ 0.12088869 -0.57149446  0.0009136  -0.00747103  0.62406545]]

Calibration rms: 1.7818430444546303
Calibration/Distortion matrices written to camera_cal.npy
Process Complete

```

# Using camera_cal.npy for ArUco marker Pose Estimation

Run detect.py to detect with camera_calibration  

Run locate.py to get distance from marker normal, distance from marker, and heading to marker  
- configured for 88mm ArUco DICT_4X4_50 marker  
- Uses 40FPS 640x480 video   
- Uses camera_cal.npy from process.py step  

# Video showing process and results

https://player.vimeo.com/video/723422779


