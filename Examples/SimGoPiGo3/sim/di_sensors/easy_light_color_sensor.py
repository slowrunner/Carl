# https://www.dexterindustries.com
#
# Copyright (c) 2018 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#

# EASIER WRAPPERS FOR:
# IMU SENSOR,
# LIGHT AND COLOR SENSOR
# TEMPERATURE, HUMIDITY and PRESSURE SENSOR

# MUTEX SUPPORT WHEN NEEDED

# LJM: for rgb to hsv conversion (see usage below where it's mentioned)
import colorsys

from di_sensors import light_color_sensor
from di_sensors import VL53L0X
from time import sleep
from math import sqrt

'''
MUTEX HANDLING
'''
from di_sensors.easy_mutex import ifMutexAcquire, ifMutexRelease

'''
PORT TRANSLATION
'''
ports = {
    "AD1": "GPG3_AD1",
    "AD2": "GPG3_AD2"
}

class EasyLightColorSensor(light_color_sensor.LightColorSensor):
    """
    Class for interfacing with the `Light Color Sensor`_.
    This class compared to :py:class:`~di_sensors.light_color_sensor.LightColorSensor` uses mutexes that allows a given
    object to be accessed simultaneously from multiple threads/processes.
    Apart from this difference, there may also be functions that are more user-friendly than the latter.
    """
    
    #: The 8 colors that :py:meth:`~di_sensors.easy_light_color_sensor.EasyLightColorSensor.guess_color_hsv`
    #: method may return upon reading and interpreting a new set of color values.
    known_colors = {
        "black":   (0,0,0),
        "white":   (255,255,255),
        "red":     (255,0,0),
        "green":   (0,255,0),
        "blue":    (0,0,255),
        "yellow":  (255,255,0),
        "cyan":    (0,255,255),
        "fuchsia": (255,0,255)
    }

    known_hsv = {
        "black":   (0,0,0),
        "white":   (0,0,100),
        "red":     (0,100,100),
        "green":   (120,100,100),
        "blue":    (240,100,100),
        "yellow":  (60,100,100),
        "cyan":    (180,100,100),
        "fuchsia": (300,100,100)
    }

    def __init__(self, port="I2C", led_state = False, use_mutex=False):
        """
        Constructor for initializing a link to the `Light Color Sensor`_.
        
        :param str port = "I2C": The port to which the distance sensor is connected to. Can also be connected to ports ``"AD1"`` or ``"AD2"`` of the `GoPiGo3`_. If you're passing an **invalid port**, then the sensor resorts to an ``"I2C"`` connection. Check the :ref:`hardware specs <hardware-interface-section>` for more information about the ports.
        :param bool led_state = False: The LED state. If it's set to ``True``, then the LED will turn on, otherwise the LED will stay off. By default, the LED is turned off.
        :param bool use_mutex = False: When using multiple threads/processes that access the same resource/device, mutexes should be enabled.
        :raises ~exceptions.OSError: When the `Light Color Sensor`_ is not reachable.
        :raises ~exceptions.RuntimeError: When the chip ID is incorrect. This happens when we have a device pointing to the same address, but it's not a `Light Color Sensor`_.
        """

        self.use_mutex = use_mutex

        try:
            bus = ports[port]
        except KeyError:
            bus = "RPI_1SW"

        # in case there's a distance sensor that hasn't been instanciated yet
        # attempt to move it to another address
        ifMutexAcquire(self.use_mutex)
        try:
            VL53L0X.VL53L0X(bus = bus)
        except:
            pass
        ifMutexRelease(self.use_mutex)

        ifMutexAcquire(self.use_mutex)
        try:
            super(self.__class__, self).__init__(led_state = led_state, bus = bus)
        except Exception as e:
            raise
        finally:
            ifMutexRelease(self.use_mutex)

        self.led_state = led_state

    # LJM: This is not required if we import <colorsys> module and use <colorsys.rgb_to_hsv> function
    # for backwards compatibility with existing code, we could just make this function a wrapper for <colorsys.rgb_to_hsv>
    def translate_to_hsv(self, in_color):
        """
        Standard algorithm to switch from one color system (**RGB**) to another (**HSV**).
        
        :param tuple(float,float,float) in_color: The RGB tuple list that gets translated to HSV system. The values of each element of the tuple is between **0** and **1**.
        :return: The translated HSV tuple list. Returned values are *H(0-360)*, *S(0-100)*, *V(0-100)*.
        :rtype: tuple(int, int, int)
        
        .. important::
           For finding out the differences between **RGB** *(Red, Green, Blue)* color scheme and **HSV** *(Hue, Saturation, Value)*
           please check out `this link <https://www.kirupa.com/design/little_about_color_hsv_rgb.htm>`__.
        """
        r,g,b = in_color

        min_channel = min((r,g,b))
        max_channel = max((r,g,b))

        v = max_channel
        delta = max_channel - min_channel
        if delta < 0.0001:
            s = 0
            h = 0
        else:
            if max_channel > 0:
                s = delta / max_channel
                if r >= max_channel:
                    h = (g - b) / delta
                elif g >= max_channel:
                    h = 2.0 + (b - r) / delta
                else:
                    h = 4 + (r - g ) / delta

                h = h * 60
                if h < 0:
                    h = h + 360

            else:
                s = 0
                h = 0

        return (h,s*100,v*100)

    def safe_raw_colors(self):
        """
        Returns the color as read by the `Light Color Sensor`_.
        The colors detected vary depending on the lighting conditions of the nearby environment.
        
        :returns: The RGBA values from the sensor. RGBA = Red, Green, Blue, Alpha (or Clear). Range of each element is between **0** and **1**. **-1** means an error occured.
        :rtype: tuple(float,float,float,float)
        """
        ifMutexAcquire(self.use_mutex)
        try:
            self.set_led(True, True) # turn light on to take color readings
            r,g,b,c = self.get_raw_colors()
            self.set_led(self.led_state, True) # return to default setting
        except:
            r,g,b,c = [-1]*4
        finally:
            ifMutexRelease(self.use_mutex)
        return (r,g,b,c)

    def safe_rgb(self):
        """
        Detect the RGB color off of the `Light Color Sensor`_.
        
        :returns: The RGB color in 8-bit format.
        :rtype: tuple(int,int,int)
        """
        colors = self.safe_raw_colors()
        if colors != (-1,-1,-1,-1):
            r,g,b,c = list(map(lambda c: int(c*255/colors[3]), colors))
        else:
            r,g,b,c = colors
        return r,g,b
    
    # LJM: a new function that calibrates for a single color
    # (suggestion: for feedback, take a subsequent reading, identify color and illuminate eyes to prove it has worked)
    # Rather than devise rules for black and white as exceptions, which may not be applicable to all environments
    # it might be better instead to adjust the robot's view of a typical white or black for the current environment
    # You could also choose to run a calibration for all colors that you are interested in, using task & environment specific examples
    def calibrate(self, color):
        """
        Replace the HSV centroid for a given color with the sensor reading obtained from an example of that color in the current lighting environment
        <color> can be one of black | white | red | green | blue | yellow | cyan | fuschia
        """
        
        if color in self.known_hsv:
            r, g, b, c = self.safe_raw_colors()
            h, s, v = colorsys.rgb_to_hsv(r/c, g/c, b/c)
            self.known_hsv[color] = [360*h, 100*s, 100*v]
        else:
            print( "Invalid color name: [{}]".format(color))
            colorlist = ', '.join(self.known_hsv.keys())
            print( "color can only be one of {}".format(colorlist))
        
    def guess_color_hsv(self, in_color):
        """
        Determines which color `in_color` parameter is closest to in the :py:attr:`~di_sensors.easy_light_color_sensor.EasyLightColorSensor.known_colors` list.
        This method uses the euclidean algorithm for detecting the nearest center to it out of :py:attr:`~di_sensors.easy_light_color_sensor.EasyLightColorSensor.known_colors` list.
        It does work exactly the same as KNN (K-Nearest-Neighbors) algorithm, where `K = 1`.
        
        :param tuple(float,float,float,float) in_color: A 4-element tuple list for the *Red*, *Green*, *Blue* and *Alpha* channels. The elements are all valued between **0** and **1**.
        :returns: The detected color in string format and then a 3-element tuple describing the color in RGB format. The values of the RGB tuple are between **0** and **1**.
        :rtype: tuple(str,(float,float,float))
        
        .. important::
           For finding out the differences between **RGB** *(Red, Green, Blue)* color scheme and **HSV** *(Hue, Saturation, Value)*
           please check out `this link <https://www.kirupa.com/design/little_about_color_hsv_rgb.htm>`__.
        """

        r,g,b,c = in_color
        # print("incoming: {} {} {} {}".format(r,g,b,c))
        try:
            # divide by luminosity(clarity) to minimize variations
            # LJM: I've replaced code for HSV conversion but perhaps not necessary if we convert existing function to colorsys.rgb_to_hsv wrapper
            h, s, v = colorsys.rgb_to_hsv(r/c, g/c, b/c)
        except:
            print("division by 0; coping")
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
        
        min_distance = 255
        for color in self.known_hsv:
            # LJM: extra line for improved readability in calculation below
            centroid = self.known_hsv[color]
            #print ("Testing {}".format(color))
            # only <h> term in distance_to_hsv was previously used. I can see why when you had dealt with black and white separately. 
            # Added <s> and <v> terms back in to cater for black and white.
            distance_to_hsv = sqrt( ((360*h) - centroid[0])**2 + ((100*s) - centroid[1])**2 + ((100*v) - centroid[2])**2 )
            #print((h,s,v), distance_to_hsv)
            if distance_to_hsv < min_distance:
                min_distance = distance_to_hsv
                candidate = color

        return (candidate, self.known_colors[candidate])
