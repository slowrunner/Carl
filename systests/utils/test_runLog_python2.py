#!/usr/bin/env python

# test program for run.log utils WITH PYTHON2 programs
#    @runLog.logRun decorator
#    runLog.entry(msg)

import sys
sys.path.append('/home/pi/Carl/plib')
import runLog

def test_entry_from_func():
    runLog.entry("executed")

@runLog.logRun
def main():
    print("test_runLog.py: main() executed")
    test_entry_from_func()
    runLog.entry("test entry from main()")

if __name__ == '__main__':
    main()
