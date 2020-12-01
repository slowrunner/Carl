#!/usr/bin/env python3

# decorator doit definition
#
# Usage:
# import doitdecorator
# @doit
# ...

import functools
import inspect


def doit(func):
  #set metadata to the wrapped func not the wrapper
  @functools.wraps(func)

  def doitwrapper(*args,**kwargs):
      print("doit decorator started")
      print("positional args:", args)
      print("keyword args are:", kwargs)
      frame = inspect.stack()[1]
      module = inspect.getmodule(frame[0])
      filename = frame.filename
      # filename = frame[0].f_code.co_filename  # also works if inspect.getmodule() returns None
      code_context = frame.code_context
      print("filename:", frame.filename)
      print("module:", module.__name__)
      print("frame:", frame.frame)
      print("code_context:", frame.code_context)
      func(*args)
      print("doit decorator finished")
  return doitwrapper

