# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python I2C drivers

# Deprecated module - use the one in github.com/DexterInd/RFR_Tools instead that's called di_i2c.py

from __future__ import print_function
from __future__ import division

import time


# Enabling one of the communication libraries
# This is not meant to change on a regular basis
# If Periphery doesn't work for you, uncomment either pigpio or smbus
#RPI_1_Module = "pigpio"
#RPI_1_Module = "smbus"
RPI_1_Module = "periphery"

if RPI_1_Module == "pigpio":
    import pigpio
elif RPI_1_Module == "smbus":
    import smbus
elif RPI_1_Module == "periphery":
    from periphery import I2C
else:
    raise IOError("RPI_1 module not supported")


import time
import fcntl
import os
import atexit


class Dexter_Mutex(object):
    """ Dexter Industries mutex """

    def __init__(self, name, loop_time = 0.0001):
        """ Initialize """

        self.Filename = "/run/lock/Dexter_Mutex_" + name
        self.LoopTime = loop_time
        self.Handle = None

        try:
            open(self.Filename, 'w')
            if os.path.isfile(self.Filename):
                os.chmod(self.Filename, 0o777)
        except Exception as e:
            pass

        # Register the exit method
        atexit.register(self.__exit_cleanup__) # register the exit method

    def __exit_cleanup__(self):
        """ Called at exit to clean up """

        self.release()

    def acquire(self):
        """ Acquire the mutex """

        while True:
            try:
                self.Handle = open(self.Filename, 'w')
                # lock
                fcntl.lockf(self.Handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return
            except IOError: # already locked by a different process
                time.sleep(self.LoopTime)
            except Exception as e:
                print(e)

    def release(self):
        """ Release the mutex """

        if self.Handle is not None and self.Handle is not True:
            self.Handle.close()
            self.Handle = None
            time.sleep(self.LoopTime)


# for RPI bus 1 SW I2C
## pip install wiringpi
#import wiringpi
import RPi.GPIO as GPIO
import time
import atexit


class Dexter_I2C_RPI_1SW(object):
    """Dexter Industries I2C bit-bang drivers for the Raspberry Pi"""

    '''
    Currently the bus runs at about 100kbps. Tested with an RPi 3B+ with minimal CPU load.


    Code for using RPi.GPIO for GPIO control
        # setup
        GPIO.setmode(GPIO.BCM) # set up the GPIO with BCM numbering
        GPIO.setup(2, GPIO.IN) # set SDA pin as input
        GPIO.setup(3, GPIO.IN) # set SCL pin as input

        GPIO.setup(3, GPIO.IN) # SCL High
        GPIO.setup(3, GPIO.OUT) # SCL Low
        GPIO.setup(2, GPIO.IN) # SDA High
        GPIO.setup(2, GPIO.OUT) # SDA Low
        GPIO.input(3) # SCL Read
        GPIO.input(2) # SDA Read

    Code for using wiringpi for GPIO control
        # setup
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(8, 0) # set SDA pin as input
        wiringpi.pinMode(9, 0) # set SCL pin as input
        wiringpi.digitalWrite(8, 0)
        wiringpi.digitalWrite(9, 0)

        wiringpi.pinMode(9, 0) # SCL High
        wiringpi.pinMode(9, 1) # SCL Low
        wiringpi.pinMode(8, 0) # SDA High
        wiringpi.pinMode(8, 1) # SDA Low
        wiringpi.digitalRead(9) # SCL Read
        wiringpi.digitalRead(8) # SDA Read


    '''

    SUCCESS = 0
    ERROR_NACK = 1
    ERROR_CLOCK_STRETCH_TIMEOUT = 2
    ERROR_DATA_STRETCH_TIMEOUT  = 3
    ERROR_DATA_AND_CLOCK_STRETCH_TIMEOUT  = 4

    # timeout if stretched for more than this long (in seconds)
    STRETCH_TIMEOUT = 0.001

    def __init__(self):
        """ Initialize """

        # Set up the GPIO pins
        GPIO.setmode(GPIO.BCM) # set up the GPIO with BCM numbering
        GPIO.setup(3, GPIO.IN) # set SCL pin as input
        GPIO.setup(2, GPIO.IN) # set SDA pin as input

        self.BusActive = False

        # Register the exit method
        atexit.register(self.__exit_cleanup__) # register the exit method

    def __exit_cleanup__(self):
        """ Called at exit to clean up """

        if self.BusActive:
            # Set GPIOs as inputs
            GPIO.setup(3, GPIO.IN) # set SCL pin as input
            GPIO.setup(2, GPIO.IN) # set SDA pin as input

        self.BusActive = False

    def transfer(self, addr, outArr, inBytes):
        """ Write and/or read I2C """

        if(len(outArr) > 0): # bytes to write?
            self.BusActive = True
            if self.__write__(addr, outArr, inBytes) != self.SUCCESS:
                self.BusActive = False
                raise IOError("[Errno 5] Input/output error")

        if(inBytes > 0): # read bytes?
            self.BusActive = True
            result, value = self.__read__(addr, inBytes)
            self.BusActive = False
            if result != self.SUCCESS:
                raise IOError("[Errno 5] Input/output error")
            return value
        else:
            self.BusActive = False

    def __delay__(self):
        """ Delay called for slowing down the I2C clock to around 100kbps """

        #time_start = time.time()
        #while (time.time() - time_start) < 0.000005:
        #    pass

        #time.sleep(0.000005)

        pass # Already enough time overhead. Return ASAP.

    def __scl_high_check__(self):
        """ Allow SCL to go high, and wait until it's high. Timeout. """

        GPIO.setup(3, GPIO.IN) # SCL High
        if not GPIO.input(3): # SCL Read
            return self.__scl_check_timeout__()
        return self.SUCCESS

    def __scl_check_timeout__(self):
        """ Wait until SCL is high, and timeout if it takes too long """

        time_start = time.time()
        while not GPIO.input(3): # SCL Read
            if (time.time() - time_start) > self.STRETCH_TIMEOUT:
                return self.ERROR_CLOCK_STRETCH_TIMEOUT # timeout waiting for SCL to go high
        #self.__delay__() # SCL is already high, just make sure it's high enough
        return self.SUCCESS

    def __sda_high_check__(self):
        """ Allow SDA to go high, and wait until it's high """

        GPIO.setup(2, GPIO.IN) # SDA High
        result = 0
        time_start = time.time()
        while not GPIO.input(2): # SDA Read
            if time.time() - time_start > self.STRETCH_TIMEOUT:
                return self.ERROR_DATA_STRETCH_TIMEOUT # timeout waiting for SDA to go high
        #self.__delay__() # SDA is already high, just make sure it's high enough
        return self.SUCCESS

    def __write__(self, addr, outArr, restart = False):
        """ Write bytes """

        outBuffer = [(addr << 1)] # left-shift I2C address and clear read bit
        outBuffer.extend(outArr) # outBuffer now contains the address and outArr
        self.__start__() # issue bus start
        for b in range(len(outBuffer)): # for each byte
            result = self.__write_byte__(outBuffer[b]) # write the byte
            if result != self.SUCCESS: # if an error
                if result == self.ERROR_NACK: # if NACK
                    self.__stop__()
                else: # other error. Probably ERROR_CLOCK_STRETCH_TIMEOUT
                    GPIO.setup(3, GPIO.IN) # SCL High
                    GPIO.setup(2, GPIO.IN) # SDA High
                return result # return error
        if restart: # if a read is immediately following, issue a restart
            # SDA high then SCL high, with provisions for timeout
            if self.__sda_high_check__():
                if self.__scl_high_check__():
                    return self.ERROR_DATA_AND_CLOCK_STRETCH_TIMEOUT
                return self.ERROR_DATA_STRETCH_TIMEOUT
            if self.__scl_high_check__():
                return self.ERROR_CLOCK_STRETCH_TIMEOUT

            #self.__start__() # This doesn't seem to be necessary # issue bus start
            return self.SUCCESS
        else:
            return self.__stop__() # issue bus stop

    def __read__(self, addr, inBytes):
        """ Read bytes """

        addr = (addr << 1) | 0x01 # left-shift I2C address and set read bit
        inBuffer = []

        self.__start__() # issue bus start
        result = self.__write_byte__(addr) # write the address and read bit
        if result != self.SUCCESS: # check for error
            if result == self.ERROR_NACK: # if NACK
                self.__stop__()
            else: # other error. Probably ERROR_CLOCK_STRETCH_TIMEOUT
                GPIO.setup(3, GPIO.IN) # SCL High
                GPIO.setup(2, GPIO.IN) # SDA High
            return result, inBuffer

        for b in range(inBytes): # for each byte to read
            result, value = self.__read_byte__((inBytes - 1) - b) # read a byte, and ack all except the last
            if result != self.SUCCESS: # check for error
                GPIO.setup(3, GPIO.IN) # SCL High
                GPIO.setup(2, GPIO.IN) # SDA High
                return result, inBuffer # return error
            inBuffer.append(value) # append the read byte to inBuffer

        result = self.__stop__() # issue bus stop
        return result, inBuffer # return the read byte array

    def __start__(self):
        """ Issue bus start sequence """

        GPIO.setup(2, GPIO.OUT) # SDA Low
        self.__delay__()

    def __stop__(self):
        """ Issue bus stop sequence """

        GPIO.setup(2, GPIO.OUT) # SDA Low
        self.__delay__()

        # SCL high then SDA high, with provisions for timeout
        if self.__scl_high_check__():
            if self.__sda_high_check__():
                return self.ERROR_DATA_AND_CLOCK_STRETCH_TIMEOUT
            return self.ERROR_CLOCK_STRETCH_TIMEOUT
        if self.__sda_high_check__():
            return self.ERROR_DATA_STRETCH_TIMEOUT

        return self.SUCCESS

    def __write_byte__(self, val):
        """ Write a byte """

        for b in range(8):
            GPIO.setup(3, GPIO.OUT) # SCL Low
            if (0x80 >> b) & val:
                GPIO.setup(2, GPIO.IN) # SDA High
            else:
                GPIO.setup(2, GPIO.OUT) # SDA Low
            #self.__delay__()
            GPIO.setup(3, GPIO.IN) # SCL High
            if not GPIO.input(3): # SCL Read
                if self.__scl_check_timeout__():
                    return self.ERROR_CLOCK_STRETCH_TIMEOUT
            #self.__delay__()
        GPIO.setup(3, GPIO.OUT) # SCL Low
        GPIO.setup(2, GPIO.IN) # SDA High
        self.__delay__()
        if self.__scl_high_check__():
            return self.ERROR_CLOCK_STRETCH_TIMEOUT

        result = self.SUCCESS
        if GPIO.input(2): # SDA Read. check for ACK
            result = self.ERROR_NACK
        GPIO.setup(3, GPIO.OUT) # SCL Low
        return result

    def __read_byte__(self, ack):
        """ Read a byte """

        GPIO.setup(2, GPIO.IN) # SDA High
        data = 0
        GPIO.setup(3, GPIO.OUT) # SCL Low
        for b in range(8):
            self.__delay__()
            GPIO.setup(3, GPIO.IN) # SCL High
            if not GPIO.input(3): # SCL Read
                if self.__scl_check_timeout__():
                    return self.ERROR_CLOCK_STRETCH_TIMEOUT
            if GPIO.input(2): # SDA Read
                data |= (0x80 >> b)
            #self.__delay__()
            GPIO.setup(3, GPIO.OUT) # SCL Low
        if ack != 0: # send ack?
            GPIO.setup(2, GPIO.OUT) # SDA Low
        else:
            self.__delay__()
        if self.__scl_high_check__():
            return self.ERROR_CLOCK_STRETCH_TIMEOUT, 0
        GPIO.setup(3, GPIO.OUT) # SCL Low
        return self.SUCCESS, data


class Dexter_I2C(object):
    """Dexter Industries I2C drivers for hardware and software I2C busses"""

    def __init__(self, bus, address, big_endian = True):
        """Initialize I2C

        Keyword arguments:
        bus -- The I2C bus. "RPI_1", "GPG3_AD1", or "GPG3_AD2".
        address -- the slave I2C address
        big_endian (default True) -- Big endian?"""
        if bus == "RPI_1":
            self.bus_name = bus

            if RPI_1_Module == "pigpio":
                self.i2c_bus = pigpio.pi()
                self.i2c_bus_handle = None
            elif RPI_1_Module == "smbus":
                self.i2c_bus = smbus.SMBus(1)
            elif RPI_1_Module == "periphery":
                self.bus_name = bus
                self.i2c_bus = I2C("/dev/i2c-1")
        elif bus == "RPI_1SW":
            self.bus_name = bus
            self.i2c_bus = Dexter_I2C_RPI_1SW()
        elif bus == "GPG3_AD1" or bus == "GPG3_AD2":
            self.bus_name = bus

            self.gopigo3_module = __import__("gopigo3")
            self.gpg3 = self.gopigo3_module.GoPiGo3()
            if bus == "GPG3_AD1":
                self.port = self.gpg3.GROVE_1
            elif bus == "GPG3_AD2":
                self.port = self.gpg3.GROVE_2
            self.gpg3.set_grove_type(self.port, self.gpg3.GROVE_TYPE.I2C)
            time.sleep(0.01)
        elif bus == "BP3_1" or bus == "BP3_2" or bus == "BP3_3" or bus == "BP3_4":
            self.bus_name = bus

            self.brickpi3_module = __import__("brickpi3")
            self.bp3 = self.brickpi3_module.BrickPi3()
            if bus == "BP3_1":
                self.port = self.bp3.PORT_1
            elif bus == "BP3_2":
                self.port = self.bp3.PORT_2
            elif bus == "BP3_3":
                self.port = self.bp3.PORT_3
            elif bus == "BP3_4":
                self.port = self.bp3.PORT_4
            self.bp3.set_sensor_type(self.port, self.bp3.SENSOR_TYPE.I2C, [0, 0])
            time.sleep(0.01)
        else:
            raise IOError("I2C bus not supported")

        self.mutex = Dexter_Mutex(name = ("I2C_Bus_" + bus))

        self.set_address(address)

        self.big_endian = big_endian

    def reconfig_bus(self):
        """Reconfigure I2C bus

        Reconfigure I2C port. If the port configuration got reset, call this method to reconfigure it."""
        if self.bus_name == "GPG3_AD1" or self.bus_name == "GPG3_AD2":
            self.gpg3.set_grove_type(self.port, self.gpg3.GROVE_TYPE.I2C)

    def set_address(self, address):
        """Set I2C address

        Keyword arguments:
        address -- the slave I2C address"""
        self.address = address
        if self.bus_name == "RPI_1" and RPI_1_Module == "pigpio":
            if self.i2c_bus_handle:
                self.i2c_bus.i2c_close(self.i2c_bus_handle)
            self.i2c_bus_handle = self.i2c_bus.i2c_open(1, address, 0)

    def transfer(self, outArr, inBytes = 0):
        """Conduct an I2C transfer (write and/or read)

        Keyword arguments:
        outArr -- list of bytes to write
        inBytes (default 0) -- how many bytes to read

        Returns list of bytes read"""

        # Make sure all bytes are in the range of 0-255
        for b in range(len(outArr)):
            outArr[b] &= 0xFF

        self.mutex.acquire() # acquire the bus mutex

        try:
            if self.bus_name == "RPI_1":
                if RPI_1_Module == "pigpio":
                    if(len(outArr) >= 2 and inBytes == 0):
                        self.i2c_bus.i2c_write_i2c_block_data(self.i2c_bus_handle, outArr[0], outArr[1:])
                    elif(len(outArr) == 1 and inBytes == 0):
                        self.i2c_bus.i2c_write_byte(self.i2c_bus_handle, outArr[0])
                    elif(len(outArr) == 1 and inBytes >= 1):
                        return self.i2c_bus.i2c_read_i2c_block_data(self.i2c_bus_handle, outArr[0], inBytes)
                    elif(len(outArr) == 0 and inBytes >= 1):
                        return self.i2c_bus.i2c_read_byte(self.i2c_bus_handle)
                    else:
                        raise IOError("I2C operation not supported")
                elif RPI_1_Module == "smbus":
                    if(len(outArr) >= 2 and inBytes == 0):
                        self.i2c_bus.write_i2c_block_data(self.address, outArr[0], outArr[1:])
                    elif(len(outArr) == 1 and inBytes == 0):
                        self.i2c_bus.write_byte(self.address, outArr[0])
                    elif(len(outArr) == 1 and inBytes >= 1):
                        return self.i2c_bus.read_i2c_block_data(self.address, outArr[0], inBytes)
                    elif(len(outArr) == 0 and inBytes == 1):
                        return self.i2c_bus.read_byte(self.address)
                    else:
                        raise IOError("I2C operation not supported")
                elif RPI_1_Module == "periphery":
                    # for repeated starts
                    # seems to fail regularly. RPi does not recognize clock stretching during repeated starts.
                    #msgs = []
                    #offset = 0
                    #if(len(outArr) > 0):
                    #    msgs.append(self.i2c_bus.Message(outArr))
                    #    offset = 1
                    #if(inBytes):
                    #    r = [0 for b in range(inBytes)]
                    #    msgs.append(self.i2c_bus.Message(r, read = True))
                    #if(len(msgs) >= 1):
                    #    self.i2c_bus.transfer(self.address, msgs)
                    #if(inBytes):
                    #    return msgs[offset].data

                    # for independent messages (no repeated starts)
                    # there is a small delay between messages, but it doesn't fail to recognize clock stretching between the messages
                    if(len(outArr) > 0):
                        msg = [self.i2c_bus.Message(outArr)]
                        self.i2c_bus.transfer(self.address, msg)
                    if(inBytes):
                        r = [0 for b in range(inBytes)]
                        msg = [self.i2c_bus.Message(r, read = True)]
                        self.i2c_bus.transfer(self.address, msg)
                        return msg[0].data
                    return

            elif self.bus_name == "RPI_1SW":
                return self.i2c_bus.transfer(self.address, outArr, inBytes)

            elif self.bus_name == "GPG3_AD1" or self.bus_name == "GPG3_AD2":
                try:
                    return self.gpg3.grove_i2c_transfer(self.port, self.address, outArr, inBytes)
                except self.gopigo3_module.I2CError:
                    raise IOError("[Errno 5] Input/output error")

            elif self.bus_name == "BP3_1" or self.bus_name == "BP3_2" or self.bus_name == "BP3_3" or self.bus_name == "BP3_4":
                try:
                    return self.bp3.i2c_transfer(self.port, self.address, outArr, inBytes)
                except self.brickpi3_module.I2CError:
                    raise IOError("[Errno 5] Input/output error")
        except:
            self.mutex.release() # release before raising the exception
            raise # still raise the exception for user-code to deal with

        self.mutex.release() # release the bus mutex

    def write_8(self, val):
        """Write an 8-bit value

        Keyword arguments:
        val -- byte to write"""
        val = int(val)
        self.transfer([val])

    def write_reg_8(self, reg, val):
        """Write an 8-bit value to a register

        Keyword arguments:
        reg -- register to write to
        val -- byte to write"""
        val = int(val)
        self.transfer([reg, val])

    def write_reg_16(self, reg, val, big_endian = None):
        """Write a 16-bit value to a register

        Keyword arguments:
        reg -- register to write to
        val -- data to write
        big_endian (default None) -- True (big endian), False (little endian), or None (use the pre-defined endianness for the object)"""
        val = int(val)
        if big_endian == None:
            big_endian = self.big_endian
        if big_endian:
            self.transfer([reg, ((val >> 8) & 0xFF), (val & 0xFF)])
        else:
            self.transfer([reg, (val & 0xFF), ((val >> 8) & 0xFF)])

    def write_reg_32(self, reg, val, big_endian = None):
        """Write a 32-bit value to a register

        Keyword arguments:
        reg -- register to write to
        val -- data to write
        big_endian (default None) -- True (big endian), False (little endian), or None (use the pre-defined endianness for the object)"""
        val = int(val)
        if big_endian == None:
            big_endian = self.big_endian
        if big_endian:
            self.transfer( [reg, ((val >> 24) & 0xFF), ((val >> 16) & 0xFF), ((val >> 8) & 0xFF), (val & 0xFF)])
        else:
            self.transfer([reg, (val & 0xFF), ((val >> 8) & 0xFF), ((val >> 16) & 0xFF), ((val >> 24) & 0xFF)])

    def write_reg_list(self, reg, list):
        """Write a list of bytes to a register

        Keyword arguments:
        reg -- regester to write to
        list -- list of bytes to write"""
        arr = [reg]
        arr.extend(list)
        self.transfer(arr)

    def read_8(self, reg = None, signed = False):
        """Read a 8-bit value

        Keyword arguments:
        reg (default None) -- Register to read from or None
        signed (default False) -- True (signed) or False (unsigned)

        Returns the value
        """
        # write the register to read from?
        if reg != None:
            outArr = [reg]
        else:
            outArr = []

        val = self.transfer(outArr, 1)

        value = val[0]

        # signed value?
        if signed:
            # negative value?
            if value & 0x80:
                value = value - 0x100

        return value

    def read_16(self, reg = None, signed = False, big_endian = None):
        """Read a 16-bit value

        Keyword arguments:
        reg (default None) -- Register to read from or None
        signed (default False) -- True (signed) or False (unsigned)
        big_endian (default None) -- True (big endian), False (little endian), or None (use the pre-defined endianness for the object)

        Returns the value
        """
        # write the register to read from?
        if reg != None:
            outArr = [reg]
        else:
            outArr = []

        val = self.transfer(outArr, 2)

        if big_endian == None:
            big_endian = self.big_endian

        # big endian?
        if big_endian:
            value = (val[0] << 8) | val[1]
        else:
            value = (val[1] << 8) | val[0]

        # signed value?
        if signed:
            # negative value?
            if value & 0x8000:
                value = value - 0x10000

        return value

    def read_32(self, reg = None, signed = False, big_endian = None):
        """Read a 32-bit value

        Keyword arguments:
        reg (default None) -- Register to read from or None
        signed (default False) -- True (signed) or False (unsigned)
        big_endian (default None) -- True (big endian), False (little endian), or None (use the pre-defined endianness for the object)

        Returns the value
        """
        # write the register to read from?
        if reg != None:
            outArr = [reg]
        else:
            outArr = []

        val = self.transfer(outArr, 4)

        if big_endian == None:
            big_endian = self.big_endian

        # big endian?
        if big_endian:
            value = (val[0] << 24) | (val[1] << 16) | (val[2] << 8) | val[3]
        else:
            value = (val[3] << 24) | (val[2] << 16) | (val[1] << 8) | val[0]

        # signed value?
        if signed:
            # negative value?
            if value & 0x80000000:
                value = value - 0x100000000

        return value

    def read_list(self, reg, len):
        """Read a list of bytes from a register

        Keyword arguments:
        reg -- Register to read from or None
        len -- Number of bytes to read

        Returns a list of the bytes read"""

        # write the register to read from?
        if reg != None:
            outArr = [reg]
        else:
            outArr = []
        return self.transfer(outArr, len)
