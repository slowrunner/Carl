#!/usr/bin/env python3

# test program for the doit decorator

from doitdecorator import *
import argparse


# ARGUMENT PARSER
ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--file", required=True, help="path to input file")
ap.add_argument("-n", "--num", type=int, default=5, help="number")
# ap.add_argument("-l", "--loop", default=False, action='store_true', help="optional loop mode")
args = vars(ap.parse_args())
# print("Started with args:",args)
# filename = args['file']
# loopFlag = args['loop']
number = args['num']

@doit
def main(x,y=5):
    print("test_doitecorator.py: main() executed")


if __name__ == '__main__':
    main(number, y=number*3)
