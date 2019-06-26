#!/usr/bin/python
#
# runLog.py   log to Carl's /home/pi/Carl/run.log
#
# Formats message as:
# YYYY-MM-DD HH:MM|[<script.py>.<funcName>]<message>
#
# USAGE:
#    import sys
#    sys.path.append('/home/pi/Carl/plib')
#    import runLog
#
#
#    def somefunc():
#        strToLog = "message"
#        runLog.logger.info(strToLog)  or
#        runLog.logger.info("message") or
#

from __future__ import print_function

import sys
import logging




# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

loghandler = logging.FileHandler('/home/pi/Carl/run.log')

logformatter = logging.Formatter('%(asctime)s|[%(filename)s.%(funcName)s]%(message)s',"%Y-%m-%d %H:%M")
loghandler.setFormatter(logformatter)
logger.addHandler(loghandler)



def testfunc():
    strToLog = "---- runLog.py testfunc() executed"
    logger.info(strToLog)
    print("runLog.py testfunc() logged:",strToLog)

# test main 
def main():

    strToLog = "---- runLog.main()  executed"
    logger.info(strToLog)
    print("runLog.py main() logged:",strToLog)
    testfunc()


if __name__ == "__main__":
    main()




