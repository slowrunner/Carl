# MultiProcessing Find Lane In PiCamera Frames


## Configuration 
- PiCamera v1.3 mounted on robot Carl (Dexter Industries GoPiGo3)  
- Raspberry Pi 3B Processor 1.2GHz 4-core 1GB memory  
- Raspbian For Robots (Dexter Industries Release of Raspian Stretch) 
  - Linux Carl 4.14.98-v7+ #1200 SMP Tue Feb 12 20:27:48 GMT 2019 armv7l GNU/Linux

## Demonstrate find_lane_in(image) using multiprocessing with PiCamera

* multiprocessing based on:  
   https://picamera.readthedocs.io/en/release-1.13/faq.html?highlight=multiprocess#camera-locks-up-with-multiprocessing
* find_lane_in(image) based on:  
         https://www.youtube.com/watch?v=eLTLtUVuuy4  
         "OpenCV Python Tutorial - Find Lanes for Self-Driving Cars"
* single-thread.py based on:  
  https://www.pyimagesearch.com/2016/08/29/common-errors-using-the-raspberry-pi-camera-module/  
  and https://github.com/waveform80/picamera/issues/195  for PiCameraValueError on ctrl-C


One process owns camera and fills a Queue with 320x240 images.  (Uncomment alternate for VGA 640x480.)  
Four processes each grab images from the Queue, and run find_lane_in(image)  
    (they do nothing with the result, unless the write-result-to-timestamped-file line is uncommented)  
    (they will write-input-frame-to-file if line is uuncommented)  

lanes.find_lane_in(image) performs the following:  

  1) create a grayscale image copy  
  2) blur the grayscale image  
  3) apply Canny edge detect to blurred grayscale image  
     return edge mask  
  4) crop edge mask to triangular region of interest  
  5) use Hough transform (binned r,theta normal to len/gap qualifed lines) to find lines  
  6) average left and right lane lines down to one left of lane, one right of lane line  
  7) create lane lines overlay  
  8) combine lane lines overlay over original image  
     returns image with lane lines drawn in bottom 40%

  (can uncomment write-edge-detect-image)



---
INPUT FRAME(S)  

![Input Image](./images/input_image.jpg?raw=true)

---
EDGE DETECTION (Gray, Blur, Canny, Trangular Region Of Interest Mask)  

![Edge Detection](./images/edge_detect.jpg?raw=true)

---
FIRST FRAME RESULT (No wait for camera to adjust exposure)  

![First Result](./images/first_result.jpg?raw=true)

---
NORMAL FRAME RESULT  

![Subsequent Results](./images/result.jpg?raw=true)

---
## MY CONCLUSIONS

**Using MultiProcessing for 640x480 image results in 2.5x higher frame rate (20 vs 8 fps)**

**Using MultiProcessing for 320x240 image results in (only) 20-30% higher frame rate (28 vs ~23)**  

**Utilizing the processing result of the single-threaded is much easier,   
  (multi needs interprocess result messaging)**

**Find_lane_in( frame) method needs a computation only mode, (no image result)  
  to further minimize computation time and improve performance for robot navigation**  

## Definitions  
* Frame Processing Time consists of 
  * dequeue or if single threaded, capture an image, 
  * find_lane_in(image), 
  * print statistics to stdout (redirected to file)

* Inter-frame Time
  * Time until next find_lane_in(image) results available 

## RESULTS

Multiprocessing of find_lane_in( 640x480 image) 
* In Order Average Inter-frame Time 48 ms or 20 fps
* By Process Average Frame Processing Time 193 ms
* "cpu load 80%"
* 307200 pixels per frame

Multiprocessing of find_lane_in( 320x240 image)
* In Order Average Inter-frame Time 35 ms or 28 fps
* By Process Average Frame Processing Time 142 ms
* "cpu load 57%"
* 76800 pixels per frame

Single-Thread.py Results of find_lane_in(640x480 image)
* Average Inter-frame Time (and Frame Processing Time) 125 ms for 7-9 fps  
* "cpu load 35%"
* 3 fps with imshow

Single-Thread.py Results of find_lane_in(320x240 image)
* Average Inter-frame Time (and Frame Processing Time)  ~40 ms or 21-26 fps  
* "cpu load 50%"
* 7 fps with imshow


