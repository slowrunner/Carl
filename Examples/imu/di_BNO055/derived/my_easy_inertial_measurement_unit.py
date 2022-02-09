#!/usr/bin/env  python3

from di_sensors.easy_inertial_measurement_unit import EasyIMUSensor


class My_EasyIMUSensor(EasyIMUSensor):

  def __init__(self, port="AD1", use_mutex=True):

    print("\nMy_EasyIMUSensor.__init__(): self.__class__\n=",self.__class__)
    # super().__init__(port=port, use_mutex=use_mutex)    # Init the EasyIMUSensor (and InertialMeasurementUnit) base classes
    super(self.__class__, self).__init__(port=port, use_mutex=use_mutex)

def main():

    try:
        print("Creating EasyIMUSensor object")
        imu = EasyIMUSensor()
    except Exception as e:
        print("Exception: {}".format(str(e)))

    print("Attempting to create My_EasyIMUSensor object")
    myimu = My_EasyIMUSensor()



if __name__ == "__main__":
    main()
