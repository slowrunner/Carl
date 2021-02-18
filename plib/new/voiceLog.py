#!/usr/bin/env python3
#
# voiceLog.py   Utils for the voice interaction log located in /home/pi/Carl/voice.log
#
# decorator @voiceLog.logRun will log a start and end entry:
#          "YYYY-MM-DD HH:MM|<file>.<func>: Started"
#          "YYYY-MM-DD HH:MM|<file>.<func>: Finished"
#
# method   voiceLog.entry(msg) will log the msg:
#          "YYYY-MM-DD HH:MM|<file>.<func>: <msg>"
#
#
# Usage:
# import sys
# sys.path.insert(1,"/home/pi/Carl/plib")
# import voiceLog
#
# @voiceLog.logRun
# def main():
# ...
#    voiceLog.entry("Put this in voice.log)

import functools
import inspect
import logging


# Set up the start-finished logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
loghandler = logging.FileHandler('/home/pi/Carl/voice.log')
logformatter = logging.Formatter('%(asctime)s|%(message)s',"%Y-%m-%d %H:%M:%S")
loghandler.setFormatter(logformatter)
logger.addHandler(loghandler)



# Note - decorator cannot use standard logging print string:
# line_logformatter = logging.Formatter('%(asctime)s|[%(filename)s.%(funcName)s]: %(message)s',"%Y-%m-%d %H:%M")


# to test run Carl/systests/utils/test_runLog.py


def logRun(func):
  #set metadata to the wrapped func not the wrapper
  @functools.wraps(func)

  def logRunWrapper(*args,**kwargs):
      # print("logRun decorator started")
      # print("positional args:", args)
      # print("keyword args are:", kwargs)
      frame = inspect.stack()[1]
      module = inspect.getmodule(frame[0]).__name__.replace("__","")
      try:
          filename = frame.filename.replace("./","")
      except:
          filename = inspect.getmodule(frame[0]).__file__
      # filename = frame[0].f_code.co_filename  # also works if inspect.getmodule() returns None
      # code_context = frame.code_context
      # print("filename:", frame.filename)
      # print("module:", module)
      # print("frame:", frame.frame)
      # print("code_context:", frame.code_context)
      logger.info(filename+"."+module+": Started")
      func(*args)
      logger.info(filename+"."+module+": Finished")
      # print("logRun decorator finished")
  return logRunWrapper

def entry(msg):
    frame = inspect.stack()[1]
    try:
        filename = frame.filename.replace("./","")
    except:
        filename = inspect.getmodule(frame[0]).__file__
    try:
        caller = frame.function
    except:
        caller = inspect.getmodule(frame[0]).__name__.replace("__","")

    # print("calling func:",caller)
    logger.info(filename+"."+caller+": "+msg)
