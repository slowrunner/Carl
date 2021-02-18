#!/usr/bin/env python3
#
# logIMU.py

"""
Documentation:
  logIMU.py enters the arguments into the imu.log with format:
  YYYY-MM-DD HH:MM:SS|[logIMU.main]|<string>
"""

# from __future__ import print_function # use python 3 syntax but make it compatible with python 2
# from __future__ import division       #                           ''

import sys
try:
    sys.path.append('/home/pi/Carl/plib')
    import imulog
    Carl = True
except:
    Carl = False

from time import sleep


def main():
    args = sys.argv
    if (len(args) == 1):
          print('USAGE: ./imuLog.py "log this message to imu.log"')
    else:
          strToLog = "** " + args[1] + " **"
          if Carl:
              imulog.imuLog.info(strToLog)
              print("'{}' added to imu.log".format(strToLog))
          else:
              print("Not Carl - string not logged")
    sleep(1)


if (__name__ == '__main__'):  main()
