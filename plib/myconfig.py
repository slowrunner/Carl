from math import pi

# Carl specific parameters

# Wheel Dia and Wheel Base for Carl
#    HP Speaker mounted on rear apron
CARLS_WHEEL_DIAMETER    = 64.0
CARLS_WHEEL_BASE_WIDTH  = 115.1
CARLS_CONFIG_SPEED      = 150    # speed Carl was configured to be most accurate

def setParameters(egpg, wd=CARLS_WHEEL_DIAMETER, wbw=CARLS_WHEEL_BASE_WIDTH, verbose=False):
    egpg.WHEEL_DIAMETER = wd
    egpg.WHEEL_CIRCUMFERENCE = wd * pi
    egpg.WHEEL_BASE_WIDTH = wbw
    egpg.WHEEL_BASE_CIRCUMFERENCE = wbw * pi
    egpg.set_speed(CARLS_CONFIG_SPEED)
    if verbose:
        print("Carl's WHEEL_DIAMETER   set to {}".format(wd))
        print("Carl's WHEEL_BASE_WIDTH set to {}".format(wbw))
        print("Carl's SPEED set to {} for best accuracy".format(CARLS_CONFIG_SPEED))

