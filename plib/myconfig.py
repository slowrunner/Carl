from math import pi

# Carl specific parameters

# Wheel Dia and Wheel Base for Carl 
#    HP Speaker mounted on rear apron
CARLS_WHEEL_DIAMETER    = 64.0
CARLS_WHEEL_BASE_WIDTH  = 115.1


def setParameters(egpg, wd=CARLS_WHEEL_DIAMETER, wbw=CARLS_WHEEL_BASE_WIDTH):
    egpg.WHEEL_DIAMETER = wd
    egpg.WHEEL_CIRCUMFERENCE = wd * pi
    egpg.WHEEL_BASE_WIDTH = wbw
    egpg.WHEEL_BASE_CIRCUMFERENCE = wbw * pi
    print("Carl's WHEEL_DIAMETER   set to {}".format(wd))
    print("Carl's WHEEL_BASE_WIDTH set to {}".format(wbw))

