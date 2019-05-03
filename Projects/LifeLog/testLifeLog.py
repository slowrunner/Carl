#!/usr/bin/python
#
# testLifeLog.py   log a test entry
#

import lifeLog

def testfunc():
    strToLog = "---- testLogLife.py.testfunc() executed"
    lifeLog.logger.info(strToLog)

# test main 
def main():
    strToLog = "---- testLogLife.py main() executed"
    lifeLog.logger.info(strToLog)
    testfunc()

if __name__ == "__main__":
    main()




