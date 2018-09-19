#!/usr/bin/env python
# Example passing in args
# Complete Doc: https://docs.python.org/3/library/argparse.html


import argparse

argparser = argparse.ArgumentParser(description='Example of passing an argument to a python program.')
argparser.add_argument('foo', nargs='?', type=int, help="N (int 1-400) optional/default=300", default=300)
argparser.add_argument('-wd','--wheel_dia', dest='wd', type=float, help="x.y (in mm, default=66.5)", default=66.5)

# "foo"  is a positional argument name
# nargs-'?' makes it optional
# type=int or type=float adds type checking on the parameter
# default=300  gives value if parm is not present
# dest='wd'   tells name to give the argument




args = argparser.parse_args()
#print args

foo = args.foo
wd = args.wd

print("foo:{:d} wd:{:.1f}".format(foo,wd))
