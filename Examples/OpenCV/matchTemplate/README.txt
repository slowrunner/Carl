# OpenCV cv2.matchTemplate Processing To Recognize Docking Sign


Config:  RPi 3B 320x240 32fps source, MATCH_METHOD = 5 TM_CCOEFF_NORMED

Result: 
  Frame taken from video at approach point to dock (17" camera to sign)
  Template converted to gray-scale and resized to width = 80
  Image converted to gray-scale
  cv2.matchTemplate() returns result map
  cv2.minMaxLoc() returns upper-left corner of template best match
                  and confidence around 88% for real docking sign
                  vs  confidence around 41% for not docking sign

Notes:
  matchTemplate is a fairly slow function
  matchTemplate is very dependent on the template width being close to the matching image area width

![Dock Sign Match 88%](/matchTemplate_CarlSign.jpg?raw=true)

![Not Dock Sign Match 41%](/matchTemplate_not_CarlSign.jpg)

For comparison matching with Docking Sign Target at width=20 pixels:

Dock Target Match was 72%
Not Dock Target Match was 55%

![Dock Sign Target Match 72%](/matchTemplate_Target.jpg?raw=true)





