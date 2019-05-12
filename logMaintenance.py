#!/usr/bin/env python3
#
# logMaintenance.py

"""
Documentation:
  logMaintenance.py enters the arguments into the life.log with format:
  YYYY-MM-DD HH:MM:SS|[logMaintenance.main]|<string>
"""

# from __future__ import print_function # use python 3 syntax but make it compatible with python 2
# from __future__ import division       #                           ''

import sys
try:
    sys.path.append('/home/pi/Carl/plib')
    import speak
    import lifeLog
    Carl = True
except:
    Carl = False

from time import sleep


def main():
    args = sys.argv
    if (len(args) == 1):
          print('USAGE: ./logMaintenance.py "log this message to life.log"')
    else:
          strToLog = "** " + args[1] + " **"
          if Carl:
              lifeLog.logger.info(strToLog)
              print("'{}' added to life.log".format(strToLog))
          else:
              print("Not Carl - string not logged")
    sleep(1)


if (__name__ == '__main__'):  main()
