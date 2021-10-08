# Unofficial "Safe" Python2 BNO055 IMU Interface and Utiliites For GoPiGo3

The BNO055 Inertial Measurement Unit requires "clock stretching I<sup>2</sup>C which the GoPiGo3 robot supports on ports AD1 and AD2.  Breakthrough transfer errors still occur occasionaly.  

This package offers "safe" (mutex protected) I<sup>2</sup>C access to the Dexter Industries / Modular Robotics BNO055 Inertial Measurement Unit, in the presence of other I<sup>2</sup>C sensors on the GoPiGo3 robot (such as the DI Distance Sensor).

```
CHIRALITY:

        Note that by default the axis orientation of the BNO chip looks like
        the following (taken from section 3.4, page 24 of the datasheet).  Notice
        the dot in the corner that corresponds to the dot on the BNO chip:

                           | Z axis
                           |
                           |   / X axis
                       ____|__/____
          Y axis     / *   | /    /|
          _________ /______|/    //
                   /___________ //
                  |____________|/


        NOTE: DI IMU
          - Y is direction of arrow head
          - X is toward right side when head up looking at the chip side
          - Z is coming at you when looking at the chip side

        DI IMU For ROS On GoPiGo3 (No axis remap needed if mounted like this)
          - Mount with chip side up, arrow head pointing to left side of bot
          - X is forward
          - Y is toward left side
          - Z is up


Features
  * EASIER WRAPPERS FOR IMU SENSOR
  * MUTEX SUPPORT WHEN NEEDED
  * HANDLES "Breakthrough" I<sup>2</sup>C ERRORS
  * Allow non NDOF modes
  * Allow SW Obj init without HW initialization
  * Defaults to no axis remap
  * Supports Python2.7

Utilities:

  * startIMU - Put the IMU in NDOF or IMUPLUS (no mags) mode
    usage: startIMU [-h] [-i] [-v] [-p {AD1,AD2}]

    optional arguments:
      -h, --help            show this help message and exit
      -i, --imuplus         start in imuplus mode (no mags)
      -v, --verbose         detailed output
      -p {AD1,AD2}, --port {AD1,AD2}
                            port 'AD1' (default) or 'AD2' only

  * resetIMU - Reset the IMU without changing mode

  * readIMU - continuous read of IMU without changing mode

  * calibrateIMU - Walk user through NDOF mode calibration
    (no motion, then perform tilting figure-eight in air)

  * logIMU - logs GoPiGo3 heading changes to ./imu.log
    useage:  logIMU &  (note process id to use in kill nnn later)



Installation:

For Python2
$ sudo pip install imu4gopigo3ros

Test:

* startIMU
* readIMU
* resetIMU
* calibrateIMU
* startIMU -i
* python3  

  >>>import ros_safe_inertial_measurement_unit as imupkg  
  
  >>>imu=imupkg.SafeIMUSensor()  
  
  >>>imu.readAndPrint()  
  
  ctrl-c  
  
  ctrl-d  
 



Remove:

$ sudo pip uninstall imu4gopigo3ros


=============

API:

DI Methods Implemented (Unchanged from easy_inertial_measurement_unit.py)
 - imu.reconfig_bus()
 - imu.safe_calibration_status()
 - imu.convert_heading(in_heading)
 - imu.safe_read_euler()
 - imu.safe_read_magnetometer()
 - imu.safe_north_point()

Expanded mutex protected Methods Implemented:
 - SafeIMUSensor()                        # EasyIMUSensor() that allows all operation modes
 - imu.resetExceptionCount()              # Reset count of recent I2C exceptions
 - imu.getExceptionCount()                # get number of recent I2C exceptions
 - imu.printCalStatus()                   # prints sys, gyro, acc, mag status 0=not cal, 3=fully calibrated`
 - imu.dumpCalDataJSON()                  # writes out calibration data to ./calData.json
 - imu.loadCalDataJSON()                  # returns calibration data from file ./calData.json
 - imu.loadAndSetCalDataJSON()            # Resets calibrarion from data in file ./calData.json
 - imu.safe_resetBNO055()                 # reset the IMU and print calibration status
 - imu.safe_axis_remap()                  # remap axis for actual chip orientation (default GoPiGo3)
 - imu.safe_calibrate()                   # uses the NDOF SYS value instead of just mags value as in DI easy_i_m_u
 - imu.safe_sgam_calibration_status()     # returns all four cal status: sys, gyro, accels, mags
 - imu.safe_read_quaternion()             # returns the quaternian values x, y, z, w
 - imu.safe_read_gyroscope()              # returns the gyroscope values x, y, z
 - imu.safe_read_accelerometer()          # returns the accels values x, y, z
 - imu.safe_read_linear_acceleration()    # returns the linear accel values x, y, z
 - imu.safe_read_temperature()            # returns the chip temp degC
 - imu.safe_set_mode()                    # change operation mode
 - imu.sefe_get_mode()                    # check current operation mode
 - imu.safe_get_system_status()           # opt run self test and return system status
 - imu.safe_get_operation_mode()          # returns operating mode of hardware
 - imu.safe_get_op_mode_str()             # returns string name of hardware operating mode
 - imu.safe_read_imu()                    # returns tuple of all readings
 - imu.safe_print_imu_readings()          # prints tuple of all readings passed in
 - imu.readAndPrint()                     # read and print with options for num times, delay, and EOL

```
