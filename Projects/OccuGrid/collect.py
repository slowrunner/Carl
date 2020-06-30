#!/usr/bin/env python3

import subprocess
from time import sleep

def main():
    # pCollect = subprocess.Popen(["ps", "-ef"])
    pCollect = subprocess.Popen(["/home/pi/Carl/Projects/OccuGrid/carlDataLogger.py", "-fps", "1"])
    print("carlDataLogger.py started with pid: {}".format(pCollect.pid))
    while True:
       try:
           sleep(1)
       except KeyboardInterrupt:
          pCollect.terminate()
          returncode = pCollect.wait()
          print("Returncode of subprocess:",returncode)
          break



if __name__ == '__main__':  main()
