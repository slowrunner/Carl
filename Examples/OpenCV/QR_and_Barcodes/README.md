OpenCV QR Code and BarCodes For GoPiGo3 


To Generate QR Codes:  http:/goqr.me

QR Code graphics are able to store over 3000 characters.  The information is encoded according to ISO/IEC 18004:2006

"QR Code" is a trademark of DENSO WAVE INCORPORATED


PyZBar:  https://pypi.org/project/pyzbar/
( nice demo https://github.com/ChiHsuChen/pyQRCodeScanner/blob/master/qrcode.py )

    Install PyZBar:
        sudo pip3 install pyzbar



# RESULTS

My result is less than impressive. I had this hope of reading 2x2 inch QR codes from 8-10 feet away, but the best I can get is 24 inches.

- Processing:
  - color video frame
  - fixTiltOCV only  # fixes 1.5 degree camera tilt
- Camera
  - CAMERA_RESOLUTION = (320,240) or (640, 480) or (1280, 960) or (2560, 1920)
  - CAMERA_BRIGHTNESS = 60  # 50 default
  - CAMERA_CONTRAST = 60    # 0 default
  - CAMERA_SHARPNESS = 25   # 0 default
  - CAMERA_AWB_MODE = 'incandescent'
  - CAMERA_FRAMERATE = 32

- 320x240 gets 12 inches reliably
- 640x320 gets 18-20 inches reliably
- 1280x960 gets 24-29 inches reliably
- 1296x730 (16:9) gets 27 inches reliably
- 1920x1080 (16:9) gets 34 inches reliably (partial FOV)
- 2560x1920 no recognitions at any distance
- Best QR set reading was 11 out of 12 on the page, sometimes 6, sometimes 9…
- Frame rate as high as 4 fps if none found
- Frame rate for single QR as high as 2 fps
- Frame rate around 0.3 fps or 3 seconds per frame

Interestingly this pyzbar seems to be the best way to go for now:
Vikas Gupta at learnopencv.com writes:

#### Speed
The ZBar library is almost twice as fast as the OpenCV QR code detector.

#### Robustness
The ZBar library produces more robust results as compared to OpenCV on the following factors as shown in the above video :

- ZBar is better or comparable at various rotation
- ZBar is better at different image sizes as seen from the different zoom levels in the video
- ZBar is better at handling perspective distortions ( when the image is not upright w.r.t the camera.

#### Features
The ZBar library provides support for Bar codes as well, which is not yet there in OpenCV.

Overall, we can say that QR Code is launched recently in OpenCV and it might get better in future releases. Till then, if you want to use Bar code or QR Code in your application, stick with ZBar.
