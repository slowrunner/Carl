# DI IMU EasyIMUSensor Class instantiation test

The chip seems to get configured twice:

```
pi@Carl:~/Carl/Examples/imu/di_BNO055/tests/instantiation $ ./create.py
create.py: Example instantiating a Dexter Industries IMU Sensor on GoPiGo3 AD1 port.
EasyIMUSensor().__init__() exec
InertialMeasurementUnit.__init__() exec
BNO055().__init__() exec
_config_mode() exec
set_mode(0) exec
_operation_mode() exec
set_mode(12) exec
BNO055.__init__() complete
InertialMeasurementUnit.__init__() complete
_config_mode() exec                           <---- why a second time
set_mode(0) exec
_operation_mode() exec
set_mode(12) exec
EasyIMUSensor().__init__() complete
create.py complete
```

create.py instantiates an 
- EasyIMUSensor subclass
  - of InitialMeasurementUnit superclass
    - instantiates a BNO055 class object

 


