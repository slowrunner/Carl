#!/usr/bin/env python3

# test program for runLog.py

import sys
sys.path.append('/home/pi/Carl/plib')
import runLog

def main():
    runLog.logger.info("Did this one work?")
    print("test_runLog.py: test main for runLog")

if __name__ == '__main__':
    main()
