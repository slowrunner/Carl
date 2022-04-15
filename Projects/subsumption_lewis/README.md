# SUBSUMPTION ROBOT ARCHITECTURE IN PYTHON FOR GOPIGO3  

My first exposure to the Brooks 1984 Subsumption Behavior Based Robotics Architecture  
was via assembling the 68HC11 based RugWarrior Pro Robot and  
the book "Mobile Robots: Inspiration to Implementation", Joseph L. Jones, Anita M. Flynn, Bruce A. Seiger.  

In MR:I2I p314, the authors present a subsumption architecture for a robot behavior named "Lewis and Clark"  
written in Interactive C programming language, consisting of a multi-processing set of 
behavior finite-state machines that use  
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
- BUMP_DISTANCES =     { "front":  5, "right front":  7, "right":  5, "left front":   7, "left":   5 }
- OBSTACLE_DISTANCES = { "front": 20, "right front": 28, "right": 20, "left front":  28, "left":  20 }
- PAN_ANGLES =         { "front": 90, "right": 0, "right front":  45, "left front": 135, "left": 180 }

- obstacles =         { "front": False, "right front": False, "right":  False, "left front": False, "left": False }
- bumps     =         { "front": False, "right front": False, "right":  False, "left front": False, "left": False }

- CW = 1              Positive mot_rot causes Clockwise rotation
- CCW = -1            Negative mot_rot causes Counter Clockwise rotation

- cruise_trans                Cruise translational velocity command (percent -100 to +100)  
- cruise_rot                  Cruise rotational velocity command (percent)
- cruise_behavior_active      Cruise active state flag  
- cruise_default_trans        Cruise default forward velocity percent   
- CRUISE_RATE                 Approx. Cruise Loop Rate per second

- avoid_trans                 Avoid translational velocity command (percent)  
- avoid_rot                   Avoid rotational velocity command (percent)  
- avoid_behavior_active       Avoid active state flag  
- avoid_default_trans         Avoid default translation velocity percent  
- avoid_default_rot           Avoid default rotational velocity percent
- AVOID_RATE                  Approximate Avoid Loop Rate per second

- escape_trans                Escape translational velocity command  
- escape_rot                  Escape rotational velocity command  
- escape_behavior_active      Escape active state flag  
- escape_default_trans        Escape default translation velocity  
- escape_default_rot          Escape default rotational velocity  
- escape_trans_time           Escape Backward/Forward Duration  
- escape_spin_time            Escape Spin Duration  
- escape_stop_time            Escape stop duration before executing escape action
- ESCAPE_RATE                 Approx. Escape Loop Rate per second

- mot_trans        Current Motor Translation Command  
- mot_rot          Current Motor Rotate Command  
- MOTORS_RATE      Approx. Motors Loop Rate per second

- ARBITRATE_RATE              Approx. Subsumption Arbitration Loop Rate per second

- SCAN_DWELL                  Time to dwell at each of the five scan directions before taking a distance reading

- inhibit_drive               Inhibit movement of motor commands
- inhibit_scan                Inhibit panning servo and distance readings
- inhibit_escape              Ignore bumps
- inhibit_avoid               Ignore obstacles
- inhibit_cruise              Turn off default behavior of driving forward
- inhibit_arbitrate           Turn off the subsumption arbitration into mot_trans and mot_rot commands

- TALK                        True: report actions with TTS, False: quietly execute behaviors
               
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
