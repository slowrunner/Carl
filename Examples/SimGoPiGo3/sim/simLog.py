#!/usr/bin/python
#
# simLog.py   log to sim.log
#
# Formats message as:
# YYYY-MM-DD HH:MM|[<script.py>.<funcName>]<message>
#
# USAGE:
#    import simLog
#
#
#    def somefunc():
#        strToLog = "message"
#        simLog.logger.info(strToLog)  or
#        simLog.logger.info("message") or
#

from __future__ import print_function

import sys
import logging




# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

loghandler = logging.FileHandler('sim.log')

logformatter = logging.Formatter('%(asctime)s|[%(filename)s.%(funcName)s]%(message)s',"%Y-%m-%d %H:%M")
loghandler.setFormatter(logformatter)
logger.addHandler(loghandler)



def testfunc():
    strToLog = "---- simLog.py testfunc() executed"
    logger.info(strToLog)
    print("simLog.py testfunc() logged:",strToLog)

# test main 
def main():

    strToLog = "---- simLog.main()  executed"
    logger.info(strToLog)
    print("simLog.py main() logged:",strToLog)
    testfunc()


if __name__ == "__main__":
    main()




