HuskyLens For GoPiGo3

https://github.com/HuskyLens/HUSKYLENSPython

WIKI: https://wiki.dfrobot.com/HUSKYLENS_V1.0_SKU_SEN0305_SEN0336  

# HUSKYLENS INFO
- I2C addr: 0x32  (50 decimal)
- Processor: Kendryte K210
- Image Sensor: OV2640 (2.0Megapixel Camera)
- Supply Voltage: 3.3~5.0V
- Current Consumption (TYP): 320mA@3.3V, 230mA@5.0V 
  (face recognition mode; 80% backlight brightness; fill light off)
- Connection Interface: UART, I2C
- Display: 2.0-inch IPS screen with 320*240 resolution
- Built-in Algorithms: 
  - Face Recognition, 
  - Object Tracking, 
  - Object Recognition, 
  - Line Tracking, 
  - Color Recognition, 
  - Tag Recognition 
- Dimension: 52mm * 44.5mm / 2.05 x 1.75inch
- HUSKYLENS Connector ("Grove connector, different pin assignment) 
  (left to right, tabs down) 
  - T: connect to SDA
  - R: connect to SCL
  - -: Gnd
  - +: +5v  (or 3.3v)

- GoPiGo3 (True) Grove Connectors: (right to left, tabs up)
  - SCL
  - SDA
  - 5v
  - Gnd

- HUSKYLENS to GoPiGo3 Cable - Mod one end:
  - swap Pin 1 and Pin 2
  - swap Pin 3 and Pin 4


sudo i2cdetect -y 1

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


