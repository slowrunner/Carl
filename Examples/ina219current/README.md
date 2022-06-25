# ina219 I2C Current Sensor for Robot Carl

== INSTALLATION ==  
```
sudo pip3 install pi-ina219
i2cdetect -y 1
 (should see at 0x40)
```

== DRIVER REFERENCE ==  

https://pypi.org/project/pi-ina219/  

https://github.com/chrisb2/pi_ina219


== DATASHEET ==  

https://cdn-shop.adafruit.com/datasheets/ina219.pdf  

Typical Current Measurement Error: +/- 0.2% or  
    roughly +/- 4mA measuring 2A

== AUTO GAIN MODE == 
```
#!/usr/bin/env python
from ina219 import INA219
from ina219 import DeviceRangeError

SHUNT_OHMS = 0.1


def read():
    ina = INA219(SHUNT_OHMS)
    ina.configure()

    print("Bus Voltage: %.3f V" % ina.voltage())
    try:
        print("Bus Current: %.3f mA" % ina.current())
        print("Power: %.3f mW" % ina.power())
        print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print(e)


if __name__ == "__main__":
    read()
```

== AUTO GAIN, HIGHER RESOLUTION MODE ==  
* By setting the maximum current expected and voltage range achieves the best possible current and power resolution.  
  The library will calculate the best gain to achieve the highest resolution based on the maximum expected current.  

* If current exceeds the maximum specified, gain is automatically increased, for a valid reading at a lower resolution. 

* When the maximum gain is reached, an exception is thrown to avoid invalid readings being returned.  


```
#!/usr/bin/env python
from ina219 import INA219
from ina219 import DeviceRangeError
import logging

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 1.0   # 12v at 0.75 expected


def read():
    # ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, log_level=logging.INFO)
    ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, log_level=logging.DEBUG)
    # ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
    ina.configure(ina.RANGE_16V)   # Choose lower voltage range 

    print("Bus Voltage: %.3f V" % ina.voltage())
    try:
        print("Bus Current: %.3f mA" % ina.current())
        print("Power: %.3f mW" % ina.power())
        print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print(e)


if __name__ == "__main__":
    read()
```

== AVERAGING, AUTO GAIN, HIGHER RESOLUTION MODE ==
*  Average over multiple readings to achieve higher accuracy
*  64 samples at 12 bit, conversion time 35ms 

```
#!/usr/bin/env python
from ina219 import INA219
from ina219 import DeviceRangeError
import logging


SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 1.0   # 12v at 0.75 expected
AVE_SAMPLES = INA219.ADC_64SAMP  # ~35ms update  sample range 2-128


def read():
    # ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, log_level=logging.INFO)
    ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, log_level=logging.DEBUG)
    # ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)

    # Choose lower voltage range, average over multiple samples
    ina.configure(ina.RANGE_16V, shunt_adc=AVE_SAMPLES) 

    print("Bus Voltage: %.3f V" % ina.voltage())
    try:
        print("Bus Current: %.3f mA" % ina.current())
        print("Power: %.3f mW" % ina.power())
        print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print(e)


if __name__ == "__main__":

    print("AVERAGE OVER 64 SAMPLES, AUTO GAIN - MAX RESOLUTION using 16V RANGE")
    print("MAX_EXPECTED_AMPS = {:1.3f}A".format(MAX_EXPECTED_AMPS))
    read()
```



== SENSOR LOW POWER MODE - wake for 1 reading every minute ==  
```
ina.configure(ina.RANGE_16V)
while True:
    print("Voltage : %.3f V" % ina.voltage())
    ina.sleep()
    time.sleep(60)
    ina.wake()
```

