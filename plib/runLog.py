#!/usr/bin/env python3
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

import logging


# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

loghandler = logging.FileHandler('/home/pi/Carl/run.log')

logformatter = logging.Formatter('%(asctime)s|[%(filename)s.%(funcName)s]%(message)s',"%Y-%m-%d %H:%M")
loghandler.setFormatter(logformatter)
logger.addHandler(loghandler)


# to test run Carl/systests/utils/test_runLog.py




