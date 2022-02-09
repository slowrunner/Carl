#!/usr/bin/env  python3

from easygopigo3 import EasyGoPiGo3



class My_EasyGoPiGo3(EasyGoPiGo3):

  def __init__(self, use_mutex=True):
    super().__init__(use_mutex=use_mutex)    # Init the EasyGoPiGo3 (and GoPiGo3) base classes
    print("speed from base EasyGoPiGo3() class:", self.speed)
    self.speed = 200
    print("speed from My_EasyGoPiGo3() class:", self.speed)

  def forward(self):
    print("CAUTION!  forward() at {} called".format(self.speed))

def main():
  megpg = My_EasyGoPiGo3()
  print("megpg.volt():",megpg.volt())
  megpg.forward()


if __name__ == "__main__":
    main()
