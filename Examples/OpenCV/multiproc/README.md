# MultiProcessing Find Lane In PiCamera Frames


## Configuration 
PiCamera v1.3 mounted on robot Carl (Dexter Industries GoPiGo3)
Raspberry Pi 3B Processor 1.2GHz 4-core 1GB memory 
Raspbian For Robots (Dexter Industries Release of Raspian Stretch) 
    Linux Carl 4.14.98-v7+ #1200 SMP Tue Feb 12 20:27:48 GMT 2019 armv7l GNU/Linux

## Demonstrate find_lane_in(image) using multiprocessing with PiCamera

multiprocessing based on https://picamera.readthedocs.io/en/release-1.13/faq.html?highlight=multiprocess#camera-locks-up-with-multiprocessing

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




![Input Image](./images/input_image.jpg?raw=true)

![Edge Detection](./images/edge_detect.jpg?raw=true)

![First Result](./images/first_result.jpg?raw=true)

![Subsequent Results](./images/result.jpg?raw=true)

List Example
1. Item
2. Item

   indented text note blank line

   text with line break w/o paragraph, use two spaces at end of line  
   text without line break

* Unordered list items can use asterisks, or
+ plus, or
- minus

[I'm an inline-style link](https://www.google.com)

[I'm an inline-style link with title](https://www.google.com "Google's Homepage")

[I'm a reference-style link][Arbitrary case-insensitive reference text]

[I'm a relative reference to a repository file](../blob/master/LICENSE)


Code example:
```python
s = "Python syntax highlighting"
print s
```

Horizontal Rule: three or more hyphens, asterisks, underscores

***

YouTube Video:
<a href="http://www.youtube.com/watch?feature=player_embedded&v=YOUTUBE_VIDEO_ID_HERE
" target="_blank"><img src="http://img.youtube.com/vi/YOUTUBE_VIDEO_ID_HERE/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>




