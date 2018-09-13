## ds360scan.py </br>   

This example spins GoPiGo3 one complete revolution (360 degrees),
while taking distance sensor readings as fast as possible.

After collecting the distance readings with each corresponding direction (0 = left, 90 = forward),
a 360 degree LIDAR like map is printed showing the GoPiGo3 in the center,
and "how the world around looks."

This example program ds360scan.py uses the view360() function from the printmaps.py module 

# Required Elements:

- [ DI Distance sensor ](https://www.dexterindustries.com/shop/distance-sensor/)
- [ GoPiGo3 ](https://www.dexterindustries.com/gopigo3/)
- printmaps.py   contains the view360() function to print the scan values 

# Usage:
- Attach DI Distance Sensor (VL53L0X TOF infrared time-of-flight ranging sensor) to either of the GoPiGo3 I2C ports.
- Run ./ds360scan.py  or </br>
      python ds360scan.py

![ GoPiGo3 Board ](https://github.com/DexterInd/GoPiGo3/blob/master/docs/source/images/gpg3_ports.jpg)

This repository contains example source code for the GoPiGo3 platform.

![ GoPiGo3 ](https://github.com/DexterInd/GoPiGo3/blob/master/docs/source/images/gopigo3.jpg)

# See Also

- [Dexter Industries](http://www.dexterindustries.com/GoPiGo)
- [Raspberry Pi](http://www.raspberrypi.org/)

# Example Output:
```
SPIN 360 AND SCAN at speed=100

Map:                                  90 deg
 ----------------------------------------------------------------------------- 48 cm
|                                                                             |
|                                                                             |
|                                                                             |
|                                                                             |
|                                                 o                           |
|                                                                             |
|                                           o        o                        |
|                            o                                                |
|                        o        o    o                o                     |
|                                    o o                                      |
|                      o                                  o                   |
|                                                                             |
|                                                         o                   |
|                 o                                                           |
|                                                            o                |
|                                                              o              |
|             o                                                               |
|                  o                   +                         o            0  270 deg
|                                                                             |
|                 o                                                o          |
|                                                                             |
|                   o                                                         |
|                     o                                               o       |
|                                                                             |
|                      o                                                      |
|                                            o     o                    o     |
|                       o        o   o                           o            |
|                           o          o   o                                  |
|                                                                             |
|                                                                             |
|                                                                             |
|                                                                             |
|                                                                             |
|                                                                             |
|                                                                             |
 --------------------------------------0-------------------------------------- 48 cm
Each '-' is 1.3 cm      Each '|' is 2.7 cm
Closest Object: 23.5 cm  Farthest Valid Object: 48.1 cm
Farthest Reading: 300.0 cm
```



## Notes: 
- Author: Alan McDonley Sep 2018 

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
