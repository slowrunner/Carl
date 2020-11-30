#!/usr/bin/env python3

# decorator doit definition
#
# Usage:
# import doitdecorator
# @doit
# ...

import functools

def doit(func):
  #set metadata to the wrapped func not the wrapper
  @functools.wraps(func)

  def doitwrapper(*args,**kwargs):
      print("doit decorator started")
      print("positional args:", args)
      print("keyword args are:", kwargs)
      func(*args)
      print("doit decorator finished")
  return doitwrapper

