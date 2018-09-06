## ds_servo_scan.py
This example creates LIDAR like maps, moving the GoPiGo3 robot forward until the closest
object is detected to be within PERSONAL_SPACE=10cm of the robot.

#Required Elements:

- ![ DI Distance sensor ](https://www.dexterindustries.com/shop/distance-sensor/)
- ![ DI servo package ](https://www.dexterindustries.com/shop/servo-package/) 
  (connected to "SERVO1", with 0=Left, 90=Center, 180=Right in degrees)
- ![ GoPiGo3 ](https://www.dexterindustries.com/gopigo3/)

Attach DI Distance Sensor (VL53L0X TOF infrared time-of-flight ranging sensor) to either of the GoPiGo3 I2C ports.
Attach the DI Servo Package to "SERVO1" port of the GOPiGo3 board.

![ GoPiGo3 Board ](https://github.com/DexterInd/GoPiGo3/blob/master/docs/source/images/gpg3_ports.jpg)

This repository contains example source code for the GoPiGo3 platform.

![ GoPiGo3 ](https://github.com/DexterInd/GoPiGo3/blob/master/docs/source/images/gopigo3.jpg)

# See Also

- [Dexter Industries] (http://www.dexterindustries.com/GoPiGo)
- [Raspberry Pi] (http://www.raspberrypi.org/)

** Note: 
- Based on ![ GoPiGo us_servo_scan.py ](https://github.com/DexterInd/GoPiGo/blob/master/Software/Python/Examples/Ultrasonic_Servo/us_servo_scan.py), 
- Update to GoPiGo3 with the DI TOF Distance Sensor, ScaleFactor adjusts to farthest object, added debug:  Alan McDonley

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
