# Follow The Light
Robot Carl based on Dexter Industries GoPiGo3 and Raspberry Pi 3B 
using OpenCV to follow the beam of a flashlight shown on the floor

Based on an example at https://botforge.wordpress.com/2016/07/25/torchflashlight-tracker-using-python-and-opencv/



<iframe src="https://player.vimeo.com/video/350441698" width="640" height="360" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>
<p><a href="https://vimeo.com/350441698">Carl Wants To Play A Game</a> from <a href="https://vimeo.com/user2287375">Alan McDonley</a> on <a href="https://vimeo.com">Vimeo</a>.</p>

- Processing:

* Carl captures a frame from the PiCamera,  
* the frame is corrected for tilt,  
* a grayscale copy is created,  
* the top 70% is masked off (only interested in light on floor),  
* blurred to remove noise, 
* evaluated for intensity of the brightest area, 
* thresholded to eliminate less bright areas, 
* processed with Canny edge detector, 
* a list of contours (bright areas) is extracted, 
* roughly circular contours are enumerated, 
* the largest (bright) circular contour is chosen, 
* the center and enclosing circle are determined, 
* the center is drawn on the picamera image, 
* a circle is drawn around the chosen contour, 
* the horizontal angle from center of image to the chosen contour is computed, 
* the tiltpan is pointed toward the light, 
* wait a second for the view to update on the display if desired

Performance is approximately 1 frame per second with or without showing the image on the display.

- Platform: GoPiGo3 from DexterIndustries.com

- Processor: Raspberry Pi 3 B
  * 1.2 GHz Max
  * Four Cores, but only one in use for program
  * 1GB Memory

- Python
- OpenCV


