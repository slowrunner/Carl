## ds_servo_scan.py </br>  ds_wServoPkg_scan.py 

This example creates LIDAR like maps, moving the GoPiGo3 robot forward until the closest
object is detected to be within PERSONAL_SPACE=10cm of the robot.

# Required Elements:

- [ DI Distance sensor ](https://www.dexterindustries.com/shop/distance-sensor/)
- [ DI servo package ](https://www.dexterindustries.com/shop/servo-package/) 
  (connected to "SERVO1", with 0=Left, 90=Center, 180=Right in degrees)
- [ GoPiGo3 ](https://www.dexterindustries.com/gopigo3/)

# Usage:
- Attach DI Distance Sensor (VL53L0X TOF infrared time-of-flight ranging sensor) to either of the GoPiGo3 I2C ports.
- Attach the DI Servo Package to "SERVO1" port of the GOPiGo3 board.
- Run ./ds_servo_scan.py  or </br>
  Run ./ds_wServoPkg_scan.py (if using Dexter Industries Servo Package per Installation Instructions)

![ GoPiGo3 Board ](https://github.com/DexterInd/GoPiGo3/blob/master/docs/source/images/gpg3_ports.jpg)

This repository contains example source code for the GoPiGo3 platform.

![ GoPiGo3 ](https://github.com/DexterInd/GoPiGo3/blob/master/docs/source/images/gopigo3.jpg)

# See Also

- [Dexter Industries](http://www.dexterindustries.com/GoPiGo)
- [Raspberry Pi](http://www.raspberrypi.org/)

** Note: 
- Based on [ GoPiGo us_servo_scan.py ](https://github.com/DexterInd/GoPiGo/blob/master/Software/Python/Examples/Ultrasonic_Servo/us_servo_scan.py)
- Update: For GoPiGo3, DI TOF Distance Sensor, ScaleFactor to farthest object, added debug - Alan McDonley

# Sample Output:
```
*** SCANNING ***

Map:                                  33 cm
 -----------------------------------------------------------------------------
|                                                                             |
|                                                                             |
|                                                                             |
|                                                                             |
|                                                                             |
|                                                  o     o       o            |
|              o       o   o    o   o     o    o                              |
|         o                            o                                      |
|                                                                             |
|                                                                             |
|          o                                                                  |
|                                                                             |
|                                                                             |
|          o                                                                  |
|                                                                             |
|         o                                                                   |
|                                                                             |
|                                      +                                      |
 --------------------------------------0-------------------------------------- 33 cm
Each '-' is 0.9 cm      Each '|' is 1.8 cm
Closest Object: 19 cm  Farthest Valid Object: 33 cm
Farthest Reading: 300 cm

*** PAUSING TO ENJOY THE VIEW ***
```

## License
GoPiGo3 for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
Copyright (C) 2018  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
