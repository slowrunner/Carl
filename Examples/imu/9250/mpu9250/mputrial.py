#!/usr/bin/python3 

#
# Based on https://github.com/scottmayberry/MPU9255/blob/master/MPUTRIAL.py
#
# (Prior to adding the reset I2C master/slave write,
#  If saw WHO_AM_I: 0x71 meaning I2C working to MPU9250, but get OSError: 121 writing to mag,
#  had to power down GoPiGo3 or disconnect/reconnect IMU cable, then try again)
#
# Tested on a lightly loaded RPi3B (juicer.py, RPI-Monitor)
#
# Direct Readings and threaded direct reeadings achieve 55 to 58 Hz, max 90 Hz
#
# OUTPUT VALUES ARE NOT CORRECT...
#

import time
from datetime import datetime as dt
from threading import Thread
import smbus
import signal
import sys

class MPU9255(Thread):
    USER_CTRL = 0x6A # [6]FIFO_EN [5]I2C_MST_EN [4]I2C_IF_DIS [2]FIFO_RST [1]I2C_MST_RST [0]SIG_COND_RST
    PWR_M = 0x6B  #  PWR_MGMT_1 Address - Register 107 H_RESET|SLEEP|CYCLE|GSTBY|PDPTAT|CLKSEL2:0
    DIV = 0x19  #    Sample Rate Divider - Register 25  rate = internal_sample_rate / (1 + DIV)
    CONFIG = 0x1A  # Config Reg 26: -|FIFO_MODE|EXT_SYNC_SET2:0|DLPF_CFG2:0
    GYRO_CONFIG = 0x1B  # Reg 27:  XG_Cten|YG_Cten|ZG_Cten|G_FS_SEL1:0|-|FCHOICE_B1:0
    ACCEL_CONFIG = 0x1C  # Reg 28: ax_st_en|ay_st_en|az_st_en|A_FS_SEL1:0
    INT_EN = 0x38   # Reg 56: Interrupt_Enable
    INT_PIN_CFG = 0x37 # Reg 55: Interrupt Pin Configuration
    I2C_MST_STATUS = 0x36 # Reg 54 Ronly

    ACCEL_X = 0x3B  # Reg 59-60  High byte, Low byte
    ACCEL_Y = 0x3D  # Reg 61-62
    ACCEL_Z = 0x3F  # Reg 63-64
    GYRO_X = 0x43   # Reg 67-68
    GYRO_Y = 0x45   # Reg 69-70
    GYRO_Z = 0x47   # Reg 71-72

    TEMP = 0x41     # Reg 65-66

    MAG_X = 0x03
    MAG_Y = 0x05
    MAG_Z = 0x07
    ST_1 = 0x02
    ST_2 = 0x09
    MAG_ADDRESS = 0x0C
    MAG_CNTL = 0x0A


    bus = smbus.SMBus(1)   # Current RPi use I2C bus 1
    Device_Address = 0x68  # MPU-9250 I2C device address
    WHO_AM_I = 0x75 # Reg 117
    FIFO_COUNT = 0x72 # Bytes in FIFO (0-512 readings * 16 bytes)


    XA_OFFS = 0x77 # Reg 119 X ACCEL Offset two bytes
    YA_OFFS = 0x7A # Reg 119 X ACCEL Offset two bytes
    ZA_OFFS = 0x7D # Reg 119 X ACCEL Offset two bytes
    XG_OFFS = 0x13 # Reg 19 X GYRO Offset two bytes
    YG_OFFS = 0x15 # Reg 21 X GYRO Offset two bytes
    ZG_OFFS = 0x17 # Reg 23 X GYRO Offset two bytes

    # Original
    AxCal = -2520
    AyCal = 4395
    AzCal = 1577
    GxCal = 130
    GyCal = 189
    GzCal = -17
    MxCal = 0
    MyCal = 0
    MzCal = 0

    # my calibration values (from prior run)
    AxCal =  0.03078125
    AyCal =  1.00831787109375
    AzCal =  -0.02070556640625
    GxCal =  -0.07358778625954199
    GyCal =  0.2364885496183206
    GzCal =  0.15908396946564884
    # Magnemometer Calibration
    MxCal =  11750
    MyCal =  -949
    MzCal =  -9461

    dT = .02     # Reading Loop delta time

    def __init__(self,dT=0.02):
        # pass
        super(MPU9255, self).__init__()
        self.dT = dT
        self.gyroAngle = 0
        self.magAngle = 0
        self.accelAngle = 0
        self.running = True
        self.data = []
        self.initMPU()
        self.calibrate()    # Gyros and Accelerometers only

    def run(self):
        while self.running:
            self.data.append(self.getInfo())
            time.sleep(self.dT) # 0.02 only gives 15Hz
            # time.sleep(0.0005)  # as fast as possible


    def initMPU(self):
        whoAmI = self.bus.read_byte_data(self.Device_Address, self.WHO_AM_I)
        print("WHO_AM_I: ",hex(whoAmI))
        # self.bus.write_byte_data(self.Device_Address, self.PWR_M, 0x80)  # reset registers
        self.bus.write_byte_data(self.Device_Address, self.USER_CTRL, 0x02) # reset I2C master/slave 
        self.bus.write_byte_data(self.Device_Address, self.DIV, 7)  # sample rate divider -
                                                                    # FIFO sample rate=(internal rate / (1+DIV)
        self.bus.write_byte_data(self.Device_Address, self.PWR_M, 1)  # tie clock source to Gyro X axis for best accuracy
        self.bus.write_byte_data(self.Device_Address, self.CONFIG, 0) # 0=Gyros 250 Hz, Delay 0.97ms Fs 8kHz
        # GYRO_CONFIG    [4:3]GYRO_FS_SEL:11=2000dps [2]0 [1:0]FCHOICE_b:00 (inverted FCHOICE)=Use DLPF
        self.bus.write_byte_data(self.Device_Address, self.GYRO_CONFIG, 24) #
        self.bus.write_byte_data(self.Device_Address, self.INT_EN, 1) # 0=disabled, 1=Enable Raw Sensor Data Ready to Interrupt pin
        # INT_PIN_CG: [7]ACTL [6]OPEN [5]LATCH_INT_EN [4]INT_ANYRD_2CLEAR [3]ACTL_FSYNC [2]FSYNC_INT_MODE_EN [1]BYPASS_EN [0]-
        self.bus.write_byte_data(self.Device_Address, self.INT_PIN_CFG, 0x22) #[7]ACT_Hi [5]LATCH_INT_EN=hold till clrd [1]BYPASS_EN
        self.bus.write_byte_data(self.Device_Address, self.I2C_MST_STATUS, 0x01) #[0]I2C_SLV0_NACK
        self.bus.write_byte_data(self.MAG_ADDRESS, self.MAG_CNTL, 0x00)  # Power-Down Mode
        time.sleep(.05)
        self.bus.write_byte_data(self.MAG_ADDRESS, self.MAG_CNTL, 0x0F)  # Fuse ROM access mode
        time.sleep(.05)
        self.bus.write_byte_data(self.MAG_ADDRESS, self.MAG_CNTL, 0x00)  # Power-Down Mode
        time.sleep(.05)
        self.bus.write_byte_data(self.MAG_ADDRESS, self.MAG_CNTL, 0x06)  # Continuous mode 2 (???)
        time.sleep(1)

    def readMPU(self, addr, dev_add=Device_Address):
        high = self.bus.read_byte_data(dev_add, addr)
        low = self.bus.read_byte_data(dev_add, addr + 1)
        value = ((high << 8) | low)
        if (value > 32768):
            value = value - 65536
        return value

    def readMPUAddress(self, addr, dev_add=Device_Address):
        return self.bus.read_byte_data(dev_add, addr)


    def accel(self):
        global AxCal
        global AyCal
        global AzCal
        x = self.readMPU(self.ACCEL_X, self.Device_Address)
        y = self.readMPU(self.ACCEL_Y, self.Device_Address)
        z = self.readMPU(self.ACCEL_Z, self.Device_Address)

        Ax = (x / 16384.0 - AxCal)
        Ay = (y / 16384.0 - AyCal)
        Az = (z / 16384.0 - AzCal)

        # print "X="+str(Ax)
        return {"AX": Ax, "AY": Ay, "AZ": Az}

    def gyro(self):
        global GxCal
        global GyCal
        global GzCal
        x = self.readMPU(self.GYRO_X, self.Device_Address)
        y = self.readMPU(self.GYRO_Y, self.Device_Address)
        z = self.readMPU(self.GYRO_Z, self.Device_Address)
        Gx = x / 131.0 - GxCal
        Gy = y / 131.0 - GyCal
        Gz = z / 131.0 - GzCal
        # print "X="+str(Gx)
        return {"GX": Gx, "GY": Gy, "GZ": Gz}

    def mag(self):
        global MxCal
        global MyCal
        global MzCal

        self.readMPUAddress(self.ST_1, self.MAG_ADDRESS)
        x = self.readMPU(self.MAG_X, self.MAG_ADDRESS)
        y = self.readMPU(self.MAG_Y, self.MAG_ADDRESS)
        z = self.readMPU(self.MAG_Z, self.MAG_ADDRESS)
        self.readMPUAddress(self.ST_2, self.MAG_ADDRESS)

        # calibration
        Mx = x / 0.6 - MxCal
        My = y / 0.6 - MyCal
        Mz = z / 0.6 - MzCal
        return {"MX": Mx, "MY": My, "MZ": Mz}

    def temp(self):
        tempRow = self.readMPU(self.TEMP, self.Device_Address)
        tempC = (tempRow / 340.0) + 36.53
        tempC = "%.2f" % tempC
        return {"TEMP": tempC}

    def reading_time(self):
        return {"TIME": dt.now().strftime("%H:%M:%S.%f")[:-3]}

    def calibrate(self):
        global AxCal
        global AyCal
        global AzCal
        x = 0
        y = 0
        z = 0
        ra = 100
        for i in range(ra):
            x = x + self.readMPU(self.ACCEL_X, self.Device_Address)
            y = y + self.readMPU(self.ACCEL_Y, self.Device_Address)
            z = z + self.readMPU(self.ACCEL_Z, self.Device_Address)
        x = x / ra
        y = y / ra
        z = z / ra
        AxCal = x / 16384.0
        AyCal = y / 16384.0
        AzCal = z / 16384.0

        print("AxCal: ", AxCal)
        print("AyCal: ", AyCal)
        print("AzCal: ", AzCal)

        global GxCal
        global GyCal
        global GzCal
        x = 0
        y = 0
        z = 0
        for i in range(ra):
            x = x + self.readMPU(self.GYRO_X, self.Device_Address)
            y = y + self.readMPU(self.GYRO_Y, self.Device_Address)
            z = z + self.readMPU(self.GYRO_Z, self.Device_Address)
        x = x / ra
        y = y / ra
        z = z / ra
        GxCal = x / 131.0
        GyCal = y / 131.0
        GzCal = z / 131.0
        print("GxCal: ", GxCal)
        print("GyCal: ", GyCal)
        print("GzCal: ", GzCal)

        # magnetometer calibration is separate


    def calibrateMag(self):
        # calibrate magnetometer
        global MxCal
        global MyCal
        global MzCal

        ra = 100

        x = 0
        y = 0
        z = 0

        for i in range(ra):
            self.readMPUAddress(self.ST_1, self.MAG_ADDRESS)
            x = x + self.readMPU(self.MAG_X, self.MAG_ADDRESS)
            y = y + self.readMPU(self.MAG_Y, self.MAG_ADDRESS)
            z = z + self.readMPU(self.MAG_Z, self.MAG_ADDRESS)
            self.readMPUAddress(self.ST_2, self.MAG_ADDRESS)

        x = x / ra
        y = y / ra
        z = z / ra

        # calibration
        MxCal = x / 0.6
        MyCal = y / 0.6
        MzCal = z / 0.6

        print("MxCal: ", MxCal)
        print("MyCal: ", MyCal)
        print("MzCal: ", MzCal)

    def getData(self):
        li = self.data.copy()
        self.data = []
        return li

    def getInfo(self):
        imu = IMU()
        imu.setTime(self.reading_time())
        imu.setTemp(self.temp())
        imu.setAccel(self.accel())
        imu.setGyro(self.gyro())
        imu.setMag(self.mag())
        return imu

class IMU:
    # class contains floating point values and reading time string
    def __init__(self):
        pass

    def setTime(self, t):
        self.tReading = t
    def setTime(self, data):
        self.tReading = data["TIME"]
    def setTemp(self, temp):
        self.temp = temp
    def setTemp(self, data):
        self.temp = float(data["TEMP"])
    def setGyro(self, gx, gy, gz):
        # print("setGyro(gx, gy, gz) called")
        self.gx = gx
        self.gy = gy
        self.gz = gz
    def setGyro(self, data):
        # print("setGyro(data) called")
        self.gx = float(data["GX"])
        self.gy = float(data["GY"])
        self.gz = float(data["GZ"])
    def setAccel(self, ax, ay, az):
        self.ax = ax
        self.ay = ay
        self.az = az
    def setAccel(self, data):
        self.ax = float(data["AX"])
        self.ay = float(data["AY"])
        self.az = float(data["AZ"])
    def setMag(self, mx, my, mz):
        self.mx = mx
        self.my = my
        self.mz = mz
    def setMag(self, data):
        self.mx = float(data["MX"])
        self.my = float(data["MY"])
        self.mz = float(data["MZ"])
    def getGyro(self):
        return [self.gx, self.gy, self.gz]
    def getAccel(self):
        return [self.ax, self.ay, self.az]
    def getMag(self):
        return [self.mx, self.my, self.mz]
    def getTemp(self):
        return self.temp
    def getTime(self):
        return self.tReading
    def getAll(self):
        li = self.getAccel()
        li.append(self.getGyro())
        li.append(self.getMag())
        li.append(self.getTemp())
        li.append(self.getTime())
        return li

# ######### CNTL-C #####
# Callback and setup to catch control-C and quit program

_funcToRun=None

def signal_handler(signal, frame):
  print('\n** Control-C Detected')
  if (_funcToRun != None):
     _funcToRun()
  sys.exit(0)     # raise SystemExit exception

# Setup the callback to catch control-C
def set_cntl_c_handler(toRun=None):
  global _funcToRun
  _funcToRun = toRun
  signal.signal(signal.SIGINT, signal_handler)




# ##### MAIN ######

def stop_it():
  global mpu

  mpu.running = False
  if mpu.is_alive():
      mpu.join(2.0)  # wait up to two seconds for thread to stop running
  print("stop_it() executed")

def direct_read(printit=False):
        global mpu

        dtNow = dt.now()
        mag   = mpu.mag()
        gyro  = mpu.gyro()
        accel = mpu.accel()
        temp  = mpu.temp()

        if printit:
            print_reading(mag, gyro, accel, temp, dtNow)

        return mag, gyro, accel, temp, dtNow

def print_reading(mag, gyro, accel, temp, dtNow=0):
        string_to_print = \
                      "MagXYZ:{: 7.1f} {: 7.1f} {: 7.1f} | " \
                      "GyroXYZ:{: 6.1f} {: 6.1f} {: 6.1f} | " \
                      "AccelXYZ:{: 6.1f} {: 6.1f} {: 6.1f} | " \
                      "Temp:{:3.1f}C | Time {} \n".format(float(mag['MX']), float(mag['MY']), float(mag['MZ']),
                                                    float(gyro['GX']), float(gyro['GY']), float(gyro['GZ']),
                                                    float(accel['AX']), float(accel['AY']), float(accel['AZ']),
                                                    float(temp['TEMP']),dtNow.strftime("%H:%M:%S.%f")[:-3])
        print(string_to_print)
        return string_to_print

def print_imu(i):
        tReading = i.getTime()
        mag = i.getMag()
        gyro = i.getGyro()
        accel = i.getAccel()
        temp = i.getTemp()
        string_to_print = \
                      "MagXYZ:{: 7.1f} {: 7.1f} {: 7.1f} | " \
                      "GyroXYZ:{: 6.1f} {: 6.1f} {: 6.1f} | " \
                      "AccelXYZ:{: 6.1f} {: 6.1f} {: 6.1f} | " \
                      "Temp:{:3.1f}C | Time {} \n".format(mag[0], mag[1], mag[2],
                                                    gyro[0], gyro[1], gyro[2],
                                                    accel[0], accel[1], accel[2],
                                                    temp,tReading)

        print(string_to_print)
        return string_to_print



def main():
    global mpu

    DELTA_T = 0.05

    mpu = MPU9255(DELTA_T)

    # #### SET CNTL-C HANDLER 
    set_cntl_c_handler(stop_it)

    print("Magnemometer Calibration")
    mpu.calibrateMag()
    print("Gyros and Accelerometers Calibration")
    for i in range(5):
        print(i)
        time.sleep(1)
    mpu.calibrate()

    # Take a few readings
    print("\n==== READ AND PRINT ====")
    for i in range(5):
        direct_read(printit=True)

    # Time direct reading
    numSamples = 100
    print("\n==== {} DIRECT READS AS FAST AS POSSIBLE ====".format(numSamples))
    readings = []
    tStart = time.time()
    for i in range(numSamples):
        readings += [direct_read()]
        time.sleep(0.001)  # Go as fast as possible
    tEnd = time.time()
    tDuration = tEnd - tStart
    hZ = 1.0 / (tDuration / numSamples)
    print("{} DIRECT READINGS TOOK {:.2f} SECONDS, ACHIEVED {:.0f} Hz \n".format(numSamples,tDuration, hZ))
    for i in readings:
        print_reading(i[0],i[1],i[2],i[3],i[4])


    #  NOW TEST THREADED READS
    mpu.start()
    time.sleep(1)
    mpu.getData() # clear data array
    tStart = time.time()
    time.sleep(1)
    print("\n==== THREADED DIRECT READS AS FAST AS POSSIBLE ====")
    readings = []
    # while True:
    for j in range(5):
        tEnd = time.time()
        imuList = mpu.getData()
        tDuration = tEnd - tStart
        tStart = time.time()
        numReadings = len(imuList)
        if (numReadings > 0):
            for i in imuList:
                # print_reading(i.getMag(), i.getGyro(), i.getAccel, i.getTemp(), i.getTime()  )
                print_imu(i)
        hZ = 1.0 / (tDuration/numReadings)
        print("{} THREADED READINGS ( {:.2f} SECONDS at {:.0f} Hz ) \n".format(numReadings,tDuration, hZ))

        tSleep = .9875 # - (time.clock() - tStart)
        print("/n==== SLEEPING  ====")
        time.sleep(tSleep)
    stop_it()

    # now just read and print
    while True:
        direct_read(printit=True)
        time.sleep(0.5)



if (__name__ == '__main__'): main()
