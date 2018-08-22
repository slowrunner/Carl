#!/usr/bin/python
#
# myPyLib.py   SUPPLIMENTAL PYTHON FUNCTIONS
#
# v0.1	19June2016  

import time
import sys
import signal



# ######### CNTL-C #####
# Callback and setup to catch control-C and quit program

_funcToRun=None

def signal_handler(signal, frame):
  print '\n** Control-C Detected'
  if (_funcToRun != None):
     _funcToRun()
  sys.exit(0)     # raise SystemExit exception

# Setup the callback to catch control-C
def set_cntl_c_handler(toRun=None):
  global _funcToRun
  _funcToRun = toRun
  signal.signal(signal.SIGINT, signal_handler)

# #########
# INTERPOLATED ARRAY OBJECT
# (instead of polynomial estimation)
#
# http://www.zovirl.com/2008/11/04/interpolated-lookup-tables-in-python/
class InterpolatedArray(object):

  """An array-like object that provides
  interpolated values between set points."""

  def __init__(self, points):
    self.points = sorted(points)

  def __getitem__(self, x):
    if x < self.points[0][0] or x > self.points[-1][0]:
      raise ValueError
    lower_point, upper_point = self._GetBoundingPoints(x)
    return self._Interpolate(x, lower_point, upper_point)

  def _GetBoundingPoints(self, x):
    """Get the lower/upper points that bound x."""
    lower_point = None
    upper_point = self.points[0]
    for point  in self.points[1:]:
      lower_point = upper_point
      upper_point = point
      if x <= upper_point[0]:
        break
    return lower_point, upper_point

  def _Interpolate(self, x, lower_point, upper_point):
    """Interpolate a Y value for x given lower & upper
    bounding points."""
    slope = (float(upper_point[1] - lower_point[1]) /
             (upper_point[0] - lower_point[0]))
    return lower_point[1] + (slope * (x - lower_point[0]))
# You use it like this:

# points = ((1, 0), (5, 10), (10, 0))
# table = InterpolatedArray(points)
# print table[1]
# print table[3.2]
# print table[7]

# ######## CLAMP #####
def clamp(n, minn, maxn):
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n

# ####### SIGN #####
def sign(n):    # returns -1 if <0, 0 if 0, +1 if positive
    return cmp(n,0)

# ###########################
# TESTS

def main():
  # TEST CMP
  print "sign(-60): %d" % sign(-60)
  print "sign(0): %d" % sign(0)
  print "sign(60): %d" % sign(60)

  
  # test clamp(n,min,max)
  for i in range(-120,120,19):
      print "n: %d clamp(n, 1, 100): %d" % (i, clamp(i,1,100))
      print "n: %d clamp(n,-100,-1): %d" % (i, clamp(i,-100,-1))


if __name__ == "__main__":
    main()
