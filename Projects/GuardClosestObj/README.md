## GCO.py </br>   

GUARD CLOSEST OBJECT

This program performs the following plan:
1) Perform 360 degree scan (Spin GoPiGo3 one complete revolution taking distance measurements,
2) Print 360 degree view to console
3) Turn toward closest object
4) Move to "Guard Spot" (wheels 8 inches from object: 1.5" baseboards, 5.5" turning radius, 1.5" safety)
5) Rotate 180 to "Guarding Direction"
6) Repeatedly perform 160 degree sector servo scan
  - If something moves closer, announce "I saw that"
  - If something moves within Guard Area, announce "Back off.  I am protecting this area"


# Required Elements:

- [ DI Distance sensor ](https://www.dexterindustries.com/shop/distance-sensor/)
- [ Pan Servo or DI Servo Package] (https://www.dexterindustries.com/shop/servo-package/)
- [ GoPiGo3 ](https://www.dexterindustries.com/gopigo3/)
- printmaps.py   contains the view360() and view180() functions to print scan information
- servoscan.py   contains the ds_map() distance sensor servo sector scan function
- scan360.py     contains the spin_and_scan() method

# Usage:
- Run ./GCO.py  or </br>
      python GCO.py

# 

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

See <http://www.gnu.org/licenses/gpl-3.0.txt>.
