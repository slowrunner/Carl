# Carl
Robot Carl based on Dexter Industries GoPiGo3

![Carl The GoPiGo3 Based Robot](/Graphics/Carl_the_GoPiGo3_robot.jpg?raw=true)

Carl Specs:

- Platform: GoPiGo3 from DexterIndustries.com

- Processor: Raspberry Pi 3 B
  * 1.2 GHz Max
  * Four Cores
  * 1GB Memory
  * Onboard WiFi (Sometimes Flakey..)

- OS: Raspbian For Robots
 
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
    About 4% accuracy to 7.5 feet (2.3m) 
    Mounted on Tilt/Pan
  * Pi-Camera v1.3
  * USB Microphone
  * (Planned: Battery_Current - ACS712 to "Grove" AD Port)
  
- Actuators/Effectors (GoPiGo3 Intrinsic)
  * Wheel Motors
  * Multi-color programmable LED (x3)
  * Program controlled Red LED (x2)
  * Tri-color Battery Voltage Indicator

- Actuators/Effectors 
  * Two Servo Tilt/Pan Assembly
  * USB Wired Audio Speaker (draws 50mA)
  * USB WiFi Dongle 
  
- Available GoPiGo3 Ports
  * I2C: Distance Sensor
  * I2C: Unused
  * Grove Analog/Digital I/O AD1: Unused
  * Grove Analog/Digital I/O AD2: Unused
  * SERVO1: Pan Servo
  * SERVO2: Tilt Servo

- Power Source: 8x 2800mAH NiMH AA cells (EBL)
  * Cliff at 7.4v (0.925 volts / cell)
  * Cycling to 15% capacity (8.5v) for max cycles
  * cycleConditioning to 7.9v four times to treat NiMH battery memory 
    when play-time drops off 10%
  * Charging at 1A
  
- Run Time:  up to 9 hours 
  * "Thinking" 6 hours using 8.5v "max cycles" limit
  * Cycle Conditioning 7 hours to 7.9v 
  * "Wandering" 2-3 hours to 8.5v recharge point
  * About 8 hours to 7.4v voltage cliff

- Recharger:  
  * Tenergy 6-12v Delta-Minus-V Peaking Charger
  * Set at 1A (Selectable 1A or 2A max rate)

- Physical:
  * 41.5 Ounces Total
  * 6" wide x 9" Long x 12" High

- First "Life": August 2018 
