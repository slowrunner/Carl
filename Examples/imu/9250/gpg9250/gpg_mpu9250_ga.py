#!/usr/bin/python3

# Based on https://github.com/MarkSherstan/MPU-6050-9250-I2C-CompFilter/blob/master/RPi/main.py
# with smbus calls converted to di_i2c calls

# The MPU-9250 data is organized MSB,LSB which is "Little Endian"

# import smbus
import di_i2c
import math
import time
import numpy as np

I2C_BUS = "GPG3_AD1"  # "RPI_1"

DEV_ADDRESS      = 0x68
PWR_MGMT_1       = 0x6B  # Reg 107 POWER MANAGEMENT 1
CONFIG           = 0x1A  # Reg 26  CONFIGURATION
WHO_AM_I         = 0x75  # Reg 117 returns 0x71
WHO_AM_I_MPU9250 = 0x71


GYRO_CONFIG      = 0x1B  # Reg 27
ACCEL_CONFIG     = 0x1C
ACCEL_CONFIG_2   = 0x1D
I2C_MST_CTRL     = 0x24  # Reg 36


GYRO_XYZ_OUT     = 0x43  # Reg 67  Signed 16bit Hi Low
ACCEL_XYZ_OUT    = 0x3B  # Reg 59  Signed 16bit Hi Low


class MPU:
    def __init__(self, gyro, acc, tau):
        # Class / object / constructor setup
        self.gx = None; self.gy = None; self.gz = None;
        self.ax = None; self.ay = None; self.az = None;

        self.gyroXcal = 0
        self.gyroYcal = 0
        self.gyroZcal = 0

        self.gyroRoll = 0
        self.gyroPitch = 0
        self.gyroYaw = 0

        self.aXcal = 0
        self.aYcal = 0
        self.aZcal = 0

        self.dX = 0
        self.dY = 0
        self.dZ = 0

        self.roll = 0
        self.pitch = 0
        self.yaw = 0

        self.sumX = 0
        self.sumY = 0
        self.sumZ = 0

        self.dtTimer = 0
        self.tau = tau

        self.gyroScaleFactor, self.gyroConfigHex = self.gyroSensitivity(gyro)
        self.accScaleFactor, self.accConfigHex = self.accelerometerSensitivity(acc)

        self.bus = I2C_BUS 
        self.dev_address = DEV_ADDRESS

        # create an I2C bus object and set the address
        self.i2c_bus = di_i2c.DI_I2C(bus=self.bus, address = self.dev_address, big_endian = False)

    def checkWhoAmI(self):
        # Check to see if there is a good connection with the MPU 9250
        whoAmI = self.i2c_bus.read_8(WHO_AM_I)
        return whoAmI

    def gyroSensitivity(self, x):
        # Create dictionary with standard value of 500 deg/s
        return {
            250:  [131.0, 0x00],
            500:  [65.5,  0x08],
            1000: [32.8,  0x10],
            2000: [16.4,  0x18]
        }.get(x,  [65.5,  0x08])

    def accelerometerSensitivity(self, x):
        # Create dictionary with standard value of 4 g
        return {
            2:  [16384.0, 0x00],
            4:  [8192.0,  0x08],
            8:  [4096.0,  0x10],
            16: [2048.0,  0x18]
        }.get(x,[8192.0,  0x08])

    def setUp(self):

        # Check to see if there is a good connection with the MPU 9250
        whoAmI = self.checkWhoAmI()

        if (whoAmI == WHO_AM_I_MPU9250):
            # Activate the MPU-6050
            # self.bus.write_byte_data(self.address, 0x6B, 0x00)  # set PWR_MGMT_1 to internal oscillator
            self.i2c_bus.write_reg_8(PWR_MGMT_1, 0x00)

            # Configure the accelerometer
            #self.bus.write_byte_data(self.address, 0x1C, self.accHex)
            self.i2c_bus.write_reg_8(ACCEL_CONFIG, self.accConfigHex)

            # Configure the gyro
            #self.bus.write_byte_data(self.address, 0x1B, self.gyroHex)
            self.i2c_bus.write_reg_8(GYRO_CONFIG, self.gyroConfigHex)


            # Display message to user
            print("MPU-9250 set up:")
            print('\tAccelerometer: config {} scalefactor {}'.format(str(self.accConfigHex), str(self.accScaleFactor)))
            print('\tGyro: ' + str(self.gyroConfigHex) + ' ' + str(self.gyroScaleFactor))
            print('\tMag: ' + 'Not Active' + "\n")
            time.sleep(2)
        else:
            # bad connection or something went wrong
            print("IMU WHO_AM_I was: " + hex(whoAmI) + ". Should have been " + hex(WHO_AM_I_MPU9250))

    def _read_vector(self, reg, count = 3, big_endian = None):
        # Read count number of 16-bit signed values starting from the provided
        # register. Returns a tuple of the values that were read.
        # Alan: From DI BNO055.py, dded endian awareness
        data = self.i2c_bus.read_list(reg, count*2)
        result = [0]*count
        for i in range(count):
            if ((big_endian == None) | (big_endian == True)):
                 result[i] = (((data[(i * 2) + 1] & 0xFF) << 8) | (data[(i * 2)] & 0xFF)) & 0xFFFF
            else:
                 result[i] = (((data[(i * 2)] & 0xFF) << 8) | (data[(i * 2)+1] & 0xFF)) & 0xFFFF
            if result[i] & 0x8000: #> 32767:
                result[i] -= 0x10000 #65536
        return result


    # replaced all single calls to self.i2c_bus.read_16(register, signed=True)
    # replaced all xyz calls to self._read_vector(register)
    def eightBit2sixteenBit(self, reg):
        # Reads high and low 8 bit values and shifts them into 16 bit
        h = self.bus.read_byte_data(self.address, reg)
        l = self.bus.read_byte_data(self.address, reg+1)
        val = (h << 8) + l
        return val

        # Make 16 bit unsigned value to signed value (0 to 65535) to (-32768 to +32767)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def getRawData(self):
        # self.gx = self.i2c_bus.read_16(signed=True,0x43)
        # self.gy = self.i2c_bus.read_16(signed=True,0x45)
        # self.gz = self.i2c_bus.read_16(signed=True,0x47)
        self.gx, self.gy, self.gz = self._read_vector(GYRO_XYZ_OUT)

        # self.ax = self.i2c_bus.read_16(signed=True,reg=0x3B)
        # self.ay = self.i2c_bus.read_16(signed=True,reg=0x3D)
        # self.az = self.i2c_bus.read_16(signed=True,reg=0x3F)
        self.ax, self.ay, self.az = self._read_vector(ACCEL_XYZ_OUT)

        print("Raw Readings: gxyz: {:6d} {:6d} {:6d} axyz: {:6d} {:6d} {:6d}".format(self.gx, self.gy, self.gz, self.ax, self.gy, self.gz))

    def calibrateGyro(self, N):
        # Display message
        print("Calibrating gyro with " + str(N) + " points. Do not move!")

        # Take N readings for each coordinate and add to itself
        for ii in range(N):
            self.getRawData()
            self.gyroXcal += self.gx
            self.gyroYcal += self.gy
            self.gyroZcal += self.gz

        # Find average offset value
        self.gyroXcal /= N
        self.gyroYcal /= N
        self.gyroZcal /= N

        # Display message and restart timer for comp filter
        print("Calibration complete")
        print("\tX axis offset: " + str(round(self.gyroXcal,1)))
        print("\tY axis offset: " + str(round(self.gyroYcal,1)))
        print("\tZ axis offset: " + str(round(self.gyroZcal,1)) + "\n")
        time.sleep(2)
        self.dtTimer = time.time()

    def calibrateAccel(self, N):
        aXReadings = []
        aYReadings = []
        aZReadings = []
        # Display message
        print("Calibrating accel with " + str(N) + " points. Do not move!")

        # Take N readings for each coordinate and add to itself
        for ii in range(N):
            self.getRawData()
            self.aXcal += self.ax
            self.aYcal += self.ay
            self.aZcal += self.az

            aXReadings += [self.ax]
            aYReadings += [self.ay]
            aZReadings += [self.az]

        # Find average offset value
        self.aXcal /= N
        self.aYcal /= N
        self.aZcal /= N

        # Print stats
        print("aX std:"+ str(round(np.std(aXReadings))) + " min:" + str(round(np.amin(aXReadings))) + " max:" + str(round(np.amax(aXReadings))) )
        print("aY std:"+ str(round(np.std(aYReadings))) + " min:" + str(round(np.amin(aYReadings))) + " max:" + str(round(np.amax(aYReadings))) )
        print("aZ std:"+ str(round(np.std(aZReadings))) + " min:" + str(round(np.amin(aZReadings))) + " max:" + str(round(np.amax(aZReadings))) )


        # Display message and restart timer for comp filter
        print("\nCalibration complete")
        print("\tX accel offset: " + str(round(self.aXcal,1)))
        print("\tY accel offset: " + str(round(self.aYcal,1)))
        print("\tZ accel offset: " + str(round(self.aZcal,1)) + "\n")
        time.sleep(2)
        self.dtTimer = time.time()

    def processIMUvalues(self):
        # Update the raw data
        self.getRawData()

        # Subtract the offset calibration values
        self.gx -= self.gyroXcal
        self.gy -= self.gyroYcal
        self.gz -= self.gyroZcal

        # Convert to instantaneous degrees per second
        self.gx /= self.gyroScaleFactor
        self.gy /= self.gyroScaleFactor
        self.gz /= self.gyroScaleFactor

        # Convert to g force
        self.ax /= self.accScaleFactor
        self.ay /= self.accScaleFactor
        self.az /= self.accScaleFactor

    def compFilter(self):
        # Get the processed values from IMU
        self.processIMUvalues()

        # Get delta time and record time for next call
        dt = time.time() - self.dtTimer
        self.dtTimer = time.time()

        # Acceleration vector angle
        accPitch = math.degrees(math.atan2(self.ay, self.az))
        accRoll = math.degrees(math.atan2(self.ax, self.az))

        # Acceleration vector magnitude
        # accMagnitude = sqrt(self.ax ** 2 + self.ay ** 2 + self.az ** 2)

        # Gyro integration angle
        self.gyroRoll -= self.gy * dt
        self.gyroPitch += self.gx * dt
        self.gyroYaw += self.gz * dt
        self.yaw = self.gyroYaw

        # Accellerometer integration 
        self.dX += self.ax * dt
        self.dY += self.ay * dt
        self.dZ += self.az * dt

        # Comp filter
        self.roll = (self.tau)*(self.roll - self.gy*dt) + (1-self.tau)*(accRoll)
        self.pitch = (self.tau)*(self.pitch + self.gx*dt) + (1-self.tau)*(accPitch)

        # Print data
        #print(" R: " + str(round(self.roll,1)) \
        #    + " P: " + str(round(self.pitch,1)) \
        #    + " Y: " + str(round(self.yaw,1))  \
        #    + " dXYZ: [" + str(round(self.dX,1)) + ", " + str(round(self.dY,1)) + ", " + str(round(self.dZ,1)) + "]"  \
        #     )

        print(" R: {:<8.1f} {:<8.1f} {:<8.1f} |  dXYZ: {:<8.1f} {:<8.1f} {:<8.1f}".format( \
                      self.roll, self.pitch, self.yaw,  \
                      self.dX, self.dY, self.dZ  \
             ))
    def noFilter(self):
        # Get the processed values from IMU
        self.processIMUvalues()

        # Get delta time and record time for next call
        dt = time.time() - self.dtTimer
        self.dtTimer = time.time()

        # Acceleration vector angle
        accPitch = math.degrees(math.atan2(self.ay, self.az))
        accRoll = math.degrees(math.atan2(self.ax, self.az))
        accYaw  = math.degrees(math.atan2(self.ay, self.ax))

        # Acceleration vector magnitude
        # accMagnitude = sqrt(self.ax ** 2 + self.ay ** 2 + self.az ** 2)

        # Gyro integration angle
        self.gyroRoll = self.gy
        self.gyroPitch = self.gx
        self.gyroYaw = self.gz


        print(" gRPY: {:<8.1f} {:<8.1f} {:<8.1f} | aRPY: {:<8.1f} {:<8.1f} {:<8.1f} |  accXYZ: {:<8.1f} {:<8.1f} {:<8.1f}".format( \
                      self.gyroRoll, self.gyroPitch, self.gyroYaw,  \
                      accRoll, accPitch, accYaw,  \
                      self.ax, self.ay, self.az  \
             ))

def main():
    # Set up class
    gyro = 250      # 250, 500, 1000, 2000 [deg/s]
    acc = 2         # 2, 4, 7, 16 [g]
    tau = 0.98
    mpu = MPU(gyro, acc, tau)

    # Set up sensor and calibrate gyro with N points
    mpu.setUp()

    # for i in range(200):
        # print("WHO_AM_I: {}".format(hex(mpu.checkWhoAmI())))
        # print("ax {:8.1f}".format(mpu.i2c_bus.read_16(ACCEL_XYZ_OUT,signed=True)))

    # mpu.getRawData()
    # exit()

    mpu.calibrateGyro(500)
    # mpu.calibrateGyro(500)
    # mpu.calibrateGyro(500)
    mpu.calibrateAccel(500)
    # mpu.calibrateAccel(500)
    # mpu.calibrateAccel(500)


    # Run for 20 secounds
    startTime = time.time()
    while(time.time() < (startTime + 20)):
        # mpu.compFilter()
        # mpu.noFilter()
        mpu.getRawData()

    # End
    print("Closing")

# Main loop
if __name__ == '__main__':
	main()
