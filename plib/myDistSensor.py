#!/usr/bin/python
#
# myDistSensor.py    DISTANCE SENSOR 
#
#
# Methods:
#     adjustReadingInMMForError(reading)  returns corrected reading
#
"""
```
# Usage:
import sys
sys.path.append('/home/pi/Carl/plib')
import myDistSensor

correctedDistance = myDistSensor.adjustReadingInMMForError(ds.read_mm())

```
"""
# ### MEASURED DATA POINTS
Y1 = 266  # actual   about 10.25"
X1 = 279  # reading

Y2 = 48.0*25.4  # actual  (difficult to measure accurately)
X2 = 48.7*25.4  # reading

M = (Y2-Y1) / (X2-X1)
B = Y2 - M * X2


def adjustReadingInMMForError(reading):
    return (M * reading + B)

# #### MAIN ####
def main():
    print("*** myDistSensor.py main() ****")
    print("Actual = %.5f * Reading + %.4f" % (M,B) )
    print("\nFor reading of %.1f and actual of %.1f, adjustReadingInMMForError returns %.1f" % (X1,Y1,adjustReadingInMMForError(X1) ))
    print("\nFor reading of %.1f inches (in MM) and actual of %.1f inches (inMM), adjustReadingInMMForError returns %.1f inches (inMM)" % (X2/25.4,Y2/25.4,adjustReadingInMMForError(X2)/25.4 ))

if __name__ == "__main__":
    main()
