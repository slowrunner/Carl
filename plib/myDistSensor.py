#!/usr/bin/python
#
# myDistSensor.py    DISTANCE SENSOR 
#
#
# Methods:
#     adjustReadingInMMForError(reading)  returns corrected reading
#     ds = init(egpg) initialize distance sensor
"""
```
# Usage:
#
import sys
sys.path.append('/home/pi/Carl/plib')
import easygopigo3
import myconfig
import myDistSensor

egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
myconfig.setParameters(egpg)
ds = myDistSensor.init(egpg)

correctedDistance = myDistSensor.adjustReadingInMMForError(ds.read_mm())

```
"""

import easygopigo3
import numpy as np

# ### MEASURED DATA POINTS
Y1 = 100  # actual
X1 = 106  # reading  (varied from 105-112)

Y2 = 1508  # actual line on floor 59.4" # 1219  # ~48" actual
X2 = 1524  # reading                    # 1247  # ~48" reading

xl = [X1,X2]
yl = [Y1,Y2]
mbl = np.polyfit(xl,yl,1)
m = mbl[0]
b = mbl[1]

def adjustReadingInMMForError(reading):
    if reading != 3000:        # No Distance Returns 3000
        adjusted = (m * reading + b)
    else:
        adjusted = reading
    return adjusted



def init(egpg):
    try:
        ds = egpg.init_distance_sensor(port='RPI_1')  # use HW I2C only!
    except:
        print("myDistSensor.init: Could not init distance sensor")
        ds = None
    return ds


# #### MAIN ####
def main():
    import tiltpan
    import myconfig
    from time import sleep
    import numpy as np

    print("*** myDistSensor.py main() ****")
    print("\nTesting adjustReadingInMMForError()")
    print("Polyfit Formula: Adjusted_Actual = %.5f * Reading + %.4f" % (m,b) )
    print("\nFor reference_reading of %.1f and reference_actual of %.1f, adjustReadingInMMForError returns %.1f" % (X1,Y1,adjustReadingInMMForError(X1) ))
    print("\nFor reference_reading of %.1f inches (in MM) and reference_actual of %.1f inches (in MM), adjustReadingInMMForError returns %.1f inches (in MM)" % (X2/25.4,Y2/25.4,adjustReadingInMMForError(X2)/25.4 ))


    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    myconfig.setParameters(egpg)
    ds = init(egpg)
    tp = tiltpan.TiltPan(egpg)


    print("\n\nPlace Carl at known distance from wall")
    sleep(5)
    print("Taking Measurement")
    mDl=[]
    for i in xrange(0,100):
        mDl+=[ds.read_mm()]
        sleep(0.1)
    measuredDistance = np.mean(mDl)
    correctedDistance = adjustReadingInMMForError(measuredDistance)
    print("average of %d measured_readings: %.1f mm = adjusted_distance: %.1f mm" % (len(mDl),measuredDistance,correctedDistance))


if __name__ == "__main__":
    main()
