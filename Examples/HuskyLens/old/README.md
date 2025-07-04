HuskyLens For GoPiGo3

https://github.com/HuskyLens/HUSKYLENSPython

WIKI: https://wiki.dfrobot.com/HUSKYLENS_V1.0_SKU_SEN0305_SEN0336  

# HUSKYLENS INFO
- I2C addr: 0x32  (50 decimal)
- Processor: Kendryte K210
- Image Sensor: OV2640 (2.0Megapixel Camera)
- Supply Voltage: 3.3~5.0V
- "Specified"Current Consumption (TYP): 320mA@3.3V, 230mA@5.0V 
  (face recognition mode; 80% backlight brightness; fill light off)
- Connection Interface: UART, I2C
- Display: 2.0-inch IPS screen with 320*240 resolution

- Built-in Algorithms:  (measured current consumption, default screen brightness) 
  - Face Recognition, (210ma @ 5.16v) 
  - Object Tracking, (170ma @ 5.16v) 
  - Object Recognition, (218ma @ 5.16v)
  - Line Tracking, (164ma @ 5.16v)
  - Color Recognition, (165ma @ 5.16v)
  - Tag Recognition   (162ma @ 5.16v)

- Dimension: 52mm * 44.5mm / 2.05 x 1.75inch

- Object Classifications
  - aeroplane  - bus     - dining-table   - potted-plant
  - bicycle    - car     - dog            - sheep
  - bird       - cat     - horse          - sofa
  - boat       - chair   - motorbike      - train
  - bottle     - cow     - person         - TV

- HUSKYLENS Connector ("Grove connector" but different pin assignment) 
  (Left to Right, **Tabs DOWN**) 
  - T: connect to SDA
  - R: connect to SCL
  - -: Gnd
  - +: +5v  (or 3.3v)

- GoPiGo3 Connectors (True Grove Connector): 
  (Left to Right, **Tabs UP** )
  - Gnd
  - 5v
  - SDA
  - SCL

- HUSKYLENS to GoPiGo3 Cable - Mod one end and mark "HuskyLens":
  - swap Pin 1 and Pin 2
  - swap Pin 3 and Pin 4


# Select i2c Protocol (Either Perform this or execute hl.command_request_knock() )
 - dial right until "General Settings"
 - press dial downward
 - [dial right/left till] "Protocol Type"
 - press dial downward
 - dial right till "i2c"
 - press dial downward
 - dial left to "Save & Return"
 - press dial downward to select
 - press dial downward to save ("Yes")


 - After setting Protocol to I2C or defining HuskyLens("I2C",0x32) object and executing knock()
   
   sudo i2cdetect -y 1

pi@Carl:~/Carl $ sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- 08 -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- 2a -- -- -- -- -- 
30: -- -- 32 -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --              

0x08 is GoPiGo3 Arduino Slave Address
0x2a is ToF Distance Sensor
0x32 is HuskyLens


# Bring Software to Raspbian For Robots RPi
mkdir Carl/Examples/HuskyLens
cd HuskyLens
git clone https://github.com/HuskyLens/HUSKYLENSPython.git


# API Returns:

command_request()
     => Return all data 
     
command_request_blocks()
     => Return all blocks on the screen

command_request_arrows()
     => Return all arrows on the screen

command_request_learned()
     => Return all learned objects on screen

command_request_blocks_learned()
     => Return all learned blocks on screen

command_request_arrows_learned() 
     => Return all learned arrows on screen 

command_request_by_id(idVal)
     *idVal is an integer
     => Return the object with id of idVal

command_request_blocks_by_id(idVal) *idVal is an integer
     *idVal is an integer
     => Return the block with id of idVal

command_request_arrows_by_id(idVal) *idVal is an integer
     *idVal is an integer
     => Return the arrow with id of idVal

command_request_algorthim(ALG_NAME)
    * ALG_NAME is a string whose value can be the following
        "ALGORITHM_OBJECT_TRACKING"
        "ALGORITHM_FACE_RECOGNITION"
        "ALGORITHM_OBJECT_RECOGNITION"
        "ALGORITHM_LINE_TRACKING"
        "ALGORITHM_COLOR_RECOGNITION"
        "ALGORITHM_TAG_RECOGNITION"
        "ALGORITHM_OBJECT_CLASSIFICATION"

command_request_knock()
    => Returns "Knock Recieved" on success


