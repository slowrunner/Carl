#!/usr/bin/python3
#
# center.py    Center Tilt and Pan Servos
#

#
from __future__ import print_function
from __future__ import division

# import the modules

import sys
sys.path
sys.path.append('/home/pi/Carl/plib')
import tiltpan
from time import sleep
import easygopigo3
import myconfig
import runLog

# ##### MAIN ######
@runLog.logRun
def main():
  egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
  myconfig.setParameters(egpg)
  tp = tiltpan.TiltPan(egpg)

  tp.tiltpan_center()
  print("tiltpan centered")
  sleep(0.2)
  tp.off()
  print("tiltpan off")

if __name__ == "__main__":
    main()

