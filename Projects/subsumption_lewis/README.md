# SUBSUMPTION ROBOT ARCHITECTURE IN PYTHON  

My first exposure to the Brooks 1984 Subsumption Behavior Based Robotics Architecture  
was via assembling the 6500 based RugWarrior Pro Robot and  
the book "Mobile Robots: Inspiration to Implementation", Joseph L. Jones, Anita M. Flynn, Bruce A. Seiger.  

In MR:I2I the authors present the subsumption architecture for a robot behavior named "Lewis and Clark"  
written in Interactive C programming language, consisting of a multi-processing set of behaviors that use  
a set of "global state and value variables" for interprocess communication.  

The Global Variables:
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
- mot_rotate   Current Motor Rotate Command  


The Behaviors:
- Cruise      Move forward always  
- Avoid       Detect obstacles and arc away  
- Escape      Detect collision/bump direction and react appropriately  
- Motor       Executes motor control  
- Arbitrate   Prioritize the behavior output commands  
- Report      Display Behavior states and current motor commands  


