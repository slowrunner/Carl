# Deriving from EasyIMUSensor failure

The DI di_sensors.easy_inertial_measurement_unit.EasyIMUSensor class 
does not allow for super-classing.  

It also was only published for Python2.7.

This is why I created the "unofficial Python3 BNO055 IMU For GoPiGo3" package 
and published it to PyPi.

Although the title has ROS in it, it has nothing to do with ROS,  
just that I needed it when building a ROS2 GoPiGo3 node.

See: https://github.com/slowrunner/rosbot-on-gopigo3/tree/main/imu4gopigo3ros2

Available on PyPi:  
Python2: https://pypi.org/project/imu4gopigo3ros/  
Python3: https://pypi.org/project/imu4gopigo3ros2/  


