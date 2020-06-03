OpenCV QR Code and BarCodes For GoPiGo3 


To Generate QR Codes:  http:/goqr.me

QR Code graphics are able to store over 3000 characters.  The information is encoded according to ISO/IEC 18004:2006

"QR Code" is a trademark of DENSO WAVE INCORPORATED


PyZBar:  https://pypi.org/project/pyzbar/
( nice demo https://github.com/ChiHsuChen/pyQRCodeScanner/blob/master/qrcode.py )

    Install PyZBar:
        sudo pip3 install pyzbar



# RESULTS

- Reliable at 18 inches (target to camera)
- Processing:
  - fixTiltOCV only  
- Camera
  - CAMERA_RESOLUTION = (640, 480)
  - CAMERA_BRIGHTNESS = 60  # 50 default
  - CAMERA_CONTRAST = 60    # 0 default
  - CAMERA_SHARPNESS = 25   # 0 default
  - CAMERA_AWB_MODE = 'incandescent'
  - CAMERA_FRAMERATE = 32


- 1280x960 gets 24 inches reliably
- 2560x1920 no recognitions at any distance


