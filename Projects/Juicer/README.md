## juicer.py </br>   

juicer.py manages Carl's batteries by 
detecting current power mode of Charging, Trickle Charging, or Discharging, 
and taking required actions of Dock, UnDock, Request Manual Assistance 
or Shut Down (for memory card safety), 
based on a set of rules for mode transitions. 

This module performs the following: 
1) Maintains last one minute and last 5 minute battery voltage peak,mean,min stats 
2) Maintains charging status of Unknown, Charging, Trickling, Not Charging 
3) Detect charging status transitions by empirical rules for 
   8x AA NiMH cells with 
   Tenergy 1025 6-12v peaking charger on 1A 
   or Tenergy 1005 7.2-12v "RC Battery Charger" on 1.8A setting 
4) Safety Shutdown if average battery voltage falls below 7.1v 
5) Records important events to ~/Carl/life.log 
6) Maintains docking count and docking state in /home/pi/Carl/carlData.json 

# Required Elements:

- [ GoPiGo3 ](https://www.dexterindustries.com/gopigo3/)
- 8 AA cell rechargable battery pack (EBL 2800mAh AA NiMH x 8 = 12v -> 7.2v)
- deltaV peaking recharger (Tenergy 1025 1A-2A or Tenergy 1005 0.9-1.8A Smart Charger)
- Library Modules: (Carl/plib/) speak.py, status.py, battery.py, tiltpan.py

# Usage:
- crontab-e runs /home/pi/Carl/nohup_juicer.sh
- which runs /home/pi/Carl/plib/juicer.py  
```
#!/bin/bash
LOGFILE=/home/pi/Carl/juicer.out

if test -f "$LOGFILE"; then
    mv $LOGFILE $LOGFILE".bak"
fi

nohup /home/pi/Carl/plib/juicer.py > $LOGFILE &
```
# 

## Notes: 
- Author: Alan McDonley Nov 2020, Apr 2019 

## License
GoPiGo3 for the Raspberry Pi: "an open source robotics platform for the Raspberry Pi."
GoPiGo3 - Copyright Modular Robotics 2020

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See <http://www.gnu.org/licenses/gpl-3.0.txt>.
