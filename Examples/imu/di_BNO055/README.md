# BNO055 Inertial Measurement Unit For GoPiGo3


Dexter Industries provides a very nice compass robot example for the GoPiGo3
which uses the BNO055 chip in the NDOF mode (Fusion using Gyros, Accels, and Mags).

After exploring the three DI interface modules:
- BNO055.py  # Hardware Interface Class BNO055()
- inertial_measurement_unit.py  # IMU abstraction class InertialMeasurementUnit()
- easy_inertial_measurement_unit.py  # multi-process/thread safe wrappers for most needed IMU functions

The InertialMeasurmentUnit() and EasyIMUSensor() classes perform HW initialization in NDOF mode
and offer calibration and value read methods.

From my investigations of IMU heading values:
- NDOF Mode: typ. +/- 2 deg, max +/- 10, drift 5-6 degrees per hour
- IMUPLUS Mode: typ. +/- 1 deg, max +/- 2, drift 3-6 degrees per day
 
What I needed beyond the DI provided modules:
- Initialization of HW in IMUPLUS mode (Fusion using only Gyros and Accels, no mags)
- Safe "reset and remap axes" method to set heading to 0
- Tracking of soft I2C exceptions
- Software Only Interface Object initialization to allow HW access/control without setting mode
- Multi-process safe program to read values from IMU without knowing current mode
- verbose options for greater visibility into IMU operations

My interface modules:

- myBNO55.py    # Hardware Interface Class BNO055() with verbose and "no init" options
- my_inertial_measurement_unit.py   # IMU abstraction class InertialMeasurementUnit()
  with verbose option, "init=False" option, mode option
- my_safe_inertial_measurement_unit.py  # multi-process/thread SafeIMUSensor() class with wrappers for most needed IMU functions

Example programs:
- startIMU_IMUPLUS_MODE.py  # Full HW and SW initialization in IMUPLUS mode
- startIMU_NDOF_MODE.py     # Full HW and SW initialization in NDOF mode
- resetIMU.py               # Reset HW and remap axes without changing mode
- calIMU.py                 # Perform mode respective calibration (IMUPLUS does not require calibration)
- safeReadIMU.py            # Initialize software object without affecting HW and perform periodic all value retrievals
- imulog.py                 # Watches GoPiGo3 wheel encoders for motion start/stop, 
  logs datetime, IMU heading, delta heading, time in motion, and software error count when motion ends
- noInitTest.py             # Test of SafeIMUSensor() Software only initialization

