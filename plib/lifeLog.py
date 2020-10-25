#!/usr/bin/python3
#
# lifeLog.py   allow user scripts to 
#              log to Carl's /home/pi/Carl/life.log
#
# Formats message as:
# YYYY-MM-DD HH:MM|[<script.py>.<funcName>]<message>
#
# USAGE:
#    import sys
#    sys.path.append('/home/pi/Carl/plib')
#    import lifeLog
#
#
#    def somefunc():
#        strToLog = "message"
#        lifeLog.logger.info(strToLog)  or
#        lifeLog.logger.info("message") 
#

from __future__ import print_function

import sys
import logging


# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

loghandler = logging.FileHandler('/home/pi/Carl/life.log')

logformatter = logging.Formatter('%(asctime)s|[%(filename)s.%(funcName)s]%(message)s',"%Y-%m-%d %H:%M")
loghandler.setFormatter(logformatter)
logger.addHandler(loghandler)



def testfunc():
    strToLog = "---- lifeLog.py testfunc() executed"
    logger.info(strToLog)
    print("lifeLog.py testfunc() logged:",strToLog)

# test main 
def main():

    testfunc()


if __name__ == "__main__":
    main()




