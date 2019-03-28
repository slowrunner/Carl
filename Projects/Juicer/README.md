## juicer.py </br>   

Detect and Report Charge|Trickle|Discharge Status

This module performs the following:
1) Detect Charging by 
2) Detect Trickle by
3) Detect Discharging by
4) Maintain X minute min/max/average voltage
5) Demo main will 
 - instantiate juicer object
 - print "status" to console every 10 seconds
 - Announce and print charging status changes
 - Request juice progressively more aggressively
       if discharging and battery voltage average falls below 8.1v
 - Request removal from juice when trickle charging 
       and battery voltage average falls below 8.1v 
 - Shutdown if average battery voltage falls below 7.4v

# Required Elements:

- [ GoPiGo3 ](https://www.dexterindustries.com/gopigo3/)
- 8 AA cell rechargable battery pack (EBL 2800mAh AA NiMH x 8 = 12v -> 7.2v)
- 1 amp 6-12v deltaV peaking recharger (Tenergy 1025 1A-2A Smart Charger)

# Usage:
- Run ./juicer.py  or </br>
      python juicer.py

# 

## Notes: 
- Author: Alan McDonley Apr 2019 

## License
GoPiGo3 for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
Copyright (C) 2019  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See <http://www.gnu.org/licenses/gpl-3.0.txt>.
