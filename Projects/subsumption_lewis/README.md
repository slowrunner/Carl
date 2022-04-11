# SUBSUMPTION ROBOT ARCHITECTURE IN PYTHON  

My first exposure to the Brooks 1984 Subsumption Behavior Based Robotics Architecture  
was via assembling the 68HC11 based RugWarrior Pro Robot and  
the book "Mobile Robots: Inspiration to Implementation", Joseph L. Jones, Anita M. Flynn, Bruce A. Seiger.  

In MR:I2I p314, the authors present a subsumption architecture for a robot behavior named "Lewis and Clark"  
written in Interactive C programming language, consisting of a multi-processing set of behaviors that use  
a set of "global state and value variables" for interprocess communication.  

The physical robot had sensors:
```
- front located "45 degree cross eyed" IR obstacle detector
  left
  front (left and right)
  right

- 360 degree bumper that detected contact from  
  left  
  front (left and right)
  right
  right rear (right and rear) 
  rear
  left rear  (left and rear)
```


The Global Variables:
```
- cru_trans    Cruise translational velocity command  
- cru_rot      Cruise rotational velocity command  
- cru_act      Cruise active state flag  
- cru_def_vel  Cruise default velocity   

- av_trans     Avoid translational velocity command  
- av_rot       Avoid rotational velocity command  
- av_act       Avoid active state flag  
- av_def_trans Avoid default translation velocity  
- av_def_rot   Avoid default rotational velocity  

- es_trans     Escape translational velocity command  
- es_rot       Escape rotational velocity command  
- es_act       Escape active state flag  
- es_def_trans Escape default translation velocity  
- es_def_rot   Escape default rotational velocity  
- es_bf        Escape Backward/Forward Duration  
- es_spin      Escape Spin Duration  

- mot_trans    Current Motor Translation Command  
- mot_rot      Current Motor Rotate Command  
```

The Behaviors:
```
- Cruise      Move forward always  
- Avoid       Detect obstacles and arc away  
- Escape      Detect collision/bump direction and react appropriately  
- Motor       Executes motor control  
- Arbitrate   Prioritize the behavior output commands  
- Report      Display Behavior states and current motor commands  
```

# subsumption.py

Provides a subsumption robot architecture with the following API:
```
setup()              instantiates an EasyGoPiGo3 with Pan Servo and Distance Sensor
                     and starts the following behaviors
                     - Motors behavior
                     - Scan behavior
                     - Arbitrate Motors
                     - Escape behavior
                     - Avoid behavior
                     - Cruise behavior
                     - Report behavior

if_obstacle()        returns list of keys of detected obstacles (Python treats empty list as False)
if_bump()            returns list of keys of detected "bumps"   (Python treats empty list as False)

teardown()           Stops all behavior threads gracefully, centers and turns off pan servo

inhibit_drive        Set True to inhibit Motors behavior from actually driving the robot
inhibit_scan         Set True to inhibit the five direction distance scanning 
inhibit_escape       Set True to inhibit reacting to bumps 
inhibit_avoid        Set True to inhibit reacting to obstacles 
inhibit_cruise       Set True to inhibit driving as the default behavior
 
mot_trans            Motors Behavior Input: Translate +100 pct to -100 pct
mot_rot              Motors Behavior Input: Rotate    +100 pct to -100 pct
```

# gopigo3_lewis.py

Implements the MR:I2I p314 Lewis and Clark Program using the subsumption.py module


Will drive forward until obstacle or bump
  - Set GoPiGo3 Eyes Green

Will avoid obstacles: (something within 20 cm of robot)
  - Set GoPiGo3 Eyes YELLOW
  - left front or right front obstacle: stop, turn away from obstacle 
  - front obstacle: stop, spin left or right 

Will escape "bumps": (something within 5 cm of robot)
  - Set GoPiGo3 Eyes RED
  - front: stop, backup for clearance, spin 90 left
  - front left: stop, spin toward bump, backup for clearance, turn 90 right
  - left: stop, spin toward bump, backup for clearance, turn 90 right
  - front right: stop, spin toward bump, backup for clearance, turn 90 left
  - right: stop, spin toward bump, backup for clearance, turn 90 left

# test_subsumption.py
