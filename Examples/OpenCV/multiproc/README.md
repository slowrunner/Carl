# MultiProcessing Find Lane In PiCamera Frames


## Configuration 
- PiCamera v1.3 mounted on robot Carl (Dexter Industries GoPiGo3)  
- Raspberry Pi 3B Processor 1.2GHz 4-core 1GB memory  
- Raspbian For Robots (Dexter Industries Release of Raspian Stretch) 
  - Linux Carl 4.14.98-v7+ #1200 SMP Tue Feb 12 20:27:48 GMT 2019 armv7l GNU/Linux

## Demonstrate find_lane_in(image) using multiprocessing with PiCamera

* multiprocessing based on https://picamera.readthedocs.io/en/release-1.13/faq.html?highlight=multiprocess#camera-locks-up-with-multiprocessing
* find_lane_in(image) based https://www.youtube.com/watch?v=eLTLtUVuuy4  
         "OpenCV Python Tutorial - Find Lanes for Self-Driving Cars"



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
## MY CONCLUSION

**It is not obvious from this test that multi-processing will result in  
more frames processed per second.  

I would need to create a comparable resolution videos or  
create single-thread.py to put this to rest. **

## Definitionss  
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


For Reference Only: Running lanes.py -f lane_video.mp4 -n  
(Comparable video sizes were not immediately available)  

* Single-threaded find_lane_in( 720x1280 image)  
  * Average Inter-frame Time (and Frame Processing Time) 122 ms or 8 fps  
  * "cpu load 65%"
  * (Carl/Examples/find-lane/lane_video.mp4)
  * 921600 pixels per frame

* Single-threaded find_lane_in( 244x400 image)  
  * Average Inter-frame Time (and Frame Processing Time)  30 ms or 33 fps  
  * "cpu load 65%"
  * (Carl/Examples/find-lane/lane_video_400x240.mp4)
  * 117120 pixels per frame

