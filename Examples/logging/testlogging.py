#!/usr/bin/python3

import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(funcName)s: %(message)s')

def main():
    x = 1
    while True:
      x+=1
      logging.info("x:{}".format(x))
      # logging.info("x:"+str(x))
      time.sleep(1)

if __name__ == "__main__":
    main()
