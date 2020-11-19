# HW and SW I2C Stress Suite

Suite consists of:
- HWDistanceSensor.py         requests DI Distance Sensor I2C-mutex-protected reading roughly 10 times a second
- SW_I2C_Stress_with_IMU.py   requests set of four DI IMU I2C-mutex-protected component readings roughly 10 times a second
- test_HW_and_SW_I2C.sh       starts both test programs as background processes, with known log file names
- monitor_HW_and_SW_logs.sh   tails both test logs with {uptime, processor temperature, and soft I2C error count} in a loop

REQUIREMENTS:
- GoPiGo3
- DI Distance Sensor wired to IC1 or IC2 connector
- DI Inertial Measurement Unit wired to AD1 connector

USAGE:

1) ./test_HW_and_SW_I2C.sh
2) ./monitor_HW_and_SW_logs.sh

3) cntrl-c to stop monitor log loop

4) ps -ef | grep -v grep | grep -E "SW_I2C_Stress_with_IMU|HWDistanceSensor"

  Note the process numbers, then kill the listed python3 processes with"
  - kill <left_most_PID>"
  - kill <left_most_PID>"

NOTES:
- SW I2C soft errors will be noted in the log and count displayed in the monitor script
- SW I2C program issues four separate I2C-mutex-protected requests (mag, gyro, accel, euler) roughly 10 times per second
- Log Files:
  - HW_I2C_during_SW_I2C_Stress.log  logs every tenth distance reading
  - SW_I2C_Stress.log                logs every tenth set of four component readings

On my (unaspirated) Pi3B, the tests result:
- 0.8 to 1.0 15 minute usage (4 = all four cores busy)
- around 55 degC 
- approximately 10 HW and 10 (x4) SW I2C requests every 2-3 seconds
- roughly 16 soft SW I2C errors in a combined 3.2 million HW and SW I2C readings
