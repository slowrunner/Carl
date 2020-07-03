#!/usr/bin/env python3


import subprocess
from time import sleep

def main():
    p1 = subprocess.Popen(["/home/pi/Carl/Examples/ProcessLauncher/proc1.py"])
    p2 = subprocess.Popen(["/home/pi/Carl/Examples/ProcessLauncher/proc2.py"])
    print("p1 started with pid: {}".format(p1.pid))
    print("p2 started with pid: {}".format(p2.pid))

    while True:
       try:
           sleep(1)
       except KeyboardInterrupt:
          p1.terminate()
          returncode = p1.wait()
          print("p1 Returncode of subprocess:",returncode)

          p2.terminate()
          returncode = p2.wait()
          print("p2 Returncode of subprocess:",returncode)
          break



if __name__ == '__main__':  main()
