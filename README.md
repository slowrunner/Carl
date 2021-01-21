# Carl
Robot Carl based on Dexter Industries GoPiGo3

![Carl The GoPiGo3 Based Robot](/Graphics/Carl_the_GoPiGo3_robot.jpg?raw=true)
![Carl The GoPiGo3 Based Robot](/Graphics/2020_Carl_With_Toys.jpg?raw=true)

Carl Specs:

- Platform: GoPiGo3 from DexterIndustries.com

- Processor: Raspberry Pi 3 B
  * 1.2 GHz Max
  * Four Cores
  * 1GB Memory
  * Onboard WiFi

- OS: Raspbian For Robots
  * version: 17 Oct 2020 (beta) PiOS based
 
- Control Interfaces: 
  * ssh over WiFi
  * TightVNC (Mac Remote Desktop)
  * apache2 VNC in browser
  * apache2 console

- Sensors (GoPiGo3 Intrinsic)
  * Battery_Voltage (GoPiGo3 intrinsic)
  * Regulated_5v_Voltage (GoPiGo3 intrinsic)
  * Magnetic Wheel Encoders 720 cnt/rev (GoPiGo3 intrinsic)

- Sensors (Raspberry Pi Intrinsic)  
  * Processor Temperature 
  * Processor Low Voltage Throttling Active / Latched
  * Processor Temperature Throttling Active / Latched
  
- Sensors (Added):
  * DI Distance Sensor (VL53L0X Infrared Time-Of-Flight)
    25 deg beam width, About 4% accuracy to 7.5 feet (2.3m) 
    Mounted on Tilt/Pan
  * Pi-Camera v1.3
  * USB Microphone
  * DI Inertial Measurement Unit (BNO055 9DOF Fusion IMU)
    also provides ambient temperature 
  
- Actuators/Effectors (GoPiGo3 Intrinsic)
  * Wheel Motors
  * Multi-color programmable LED (x3)
  * Program controlled Red LED (x2)
  * Tri-color Battery Voltage Indicator

- Actuators/Effectors 
  * Two Servo Tilt/Pan Assembly
  * MonkMakes 2.5W Audio Speaker (draws 9.5mA 5v at idle)
  * [USB WiFi Dongle draws additonal 100mA at 5v] 
  
- Available GoPiGo3 Ports
  * I2C: Distance Sensor
  * I2C: Unused
  * Grove Analog/Digital I/O AD1: Unused
  * Grove Analog/Digital I/O AD2: Unused (pwr/gnd for speaker)
  * SERVO1: Pan Servo
  * SERVO2: Tilt Servo

- Power Source: 8x 2000mAH NiMH AA cells (Eneloop)
  * Cliff at 7.4v (0.925 volts / cell)
  * Cycling to 8.1v allows two missed docking before safety shutdown
  * cycleConditioning to 7.9v four times to treat NiMH battery memory 
    when play-time drops off 10%
  * Charging at 0.9A for 4 hours ( 92degF max battery temp )
  * Provides around 8 hours "playtime"
  
- Run Time: 8 to 8.5 hours max 
  * "Thinking" 8 hours using 8.1v "need to dock" limit
  * "Wandering" 2-4 hours to 8.1v recharge point
  * About 9 hours to 7.4v voltage cliff

- Recharger:  
  * Tenergy 1005 7.2-12v Delta-Minus-V Peaking Charger
  * Set at 0.9A (Selectable 0.9A or 1.8A max rate)
    (1.8A rate causes 130degF max battery temp!)

- Physical:
  * 41.5 Ounces Total
  * 6" wide x 9" Long x 12" High

- First "Life": August 2018 
