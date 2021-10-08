import setuptools

try:
    with open("package_description.rst", "r") as fh:
        pkg_description = fh.read()

except IOError:
        pkg_description = "Error - Contact Author"


setuptools.setup(
     name='imu4gopigo3ros',
     version='0.6',
     description="Safe Python2 BNO055 IMU interface and utilities for ROS on GoPiGo3",
     long_description=pkg_description,
     long_description_content_type="text/markdown",

     author="Cyclical_Obsessive",
     author_email="tovli@hotmail.com",

     scripts=['readIMU', 'resetIMU', 'startIMU', 'calibrateIMU', 'logIMU' ] ,
     url="https://github.com/slowrunner/rosbot-on-gopigo3/tree/main/imu4gopigo3ros",

     license = 'MIT',
     classifiers=[
         "Development Status :: 3 - Alpha",
         "Programming Language :: Python :: 2",
         "License :: OSI Approved :: MIT License",
         "Operating System :: POSIX :: Linux",
     ],
     keywords = ['robot', 'gopigo', 'gopigo3', 'dexter industries', 'modular robotics', 'ros', 'bno055'],
     packages=setuptools.find_packages(),
     py_modules = ['rosBNO055', 'ros_inertial_measurement_unit', 'ros_safe_inertial_measurement_unit'],
     install_requires = ['di_sensors']
 )
