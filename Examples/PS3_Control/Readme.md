## PS3 Controller Example
### This example controls the GoPiGo3 and using a PS3 Dualshock 3 controller

Based on this article for the original GoPiGo:
![PS3 Controller and the Raspberry Pi Robot](https://raw.githubusercontent.com/DexterInd/GoPiGo/master/Software/Python/Examples/PS3_Control/PS3-controller-for-raspberry-pi.jpg "GoPiGo Raspberry Pi Robot controlled with a Playstation3 controller")


**Files:**
- ps3.py : Python library for getting values from the PS3 controller
- ps3_egpg_example.py :Example for using the PS3 controller with the GoPiGo3
- sixpair: used to pair the PS3 controller using bluetooth

**Usage**
- Connect the PS3 controller with the Raspberry Pi using a USB cable and run sixpair

>./sixpair

- Now disconnect the USB cable an press the **PS** button on the PS3 controller a few times and the run the ps3_egpg_example.py

>python ps3_egpg_example.py

**Note:**
This code is only targeted for GoPiGo3 with Dexter Industries Image Raspbian For Robots


![ GoPiGo ](https://raw.githubusercontent.com/DexterInd/GoPiGo3/master/GoPiGo3_Raspberry_Pi_Robot_With_Eyes.jpg)

# See Also

- [Dexter Industries](http://www.dexterindustries.com/gopigo3)
- [Raspberry Pi](http://www.raspberrypi.org/)


## License
GoPiGo3 for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
Copyright (C) 2020  Dexter Industries

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
