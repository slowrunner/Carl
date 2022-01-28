#!/usr/bin/env python3

import threading
import time
import traceback
import datetime



class Singleton():

    # CLASS VARS  (Desire available to all instances)
    #   Access as Singleton.class_var_name

    singleThreadHandle=None   # the single thread for all objects of Singleton() class
    tSleep=0.1
    execPerSec=10
    execCounter=0
    singletonExecCounter=0
    debugLevel=99

    def __init__(self,execPerSec=10):
        if (Singleton.singleThreadHandle!=None):
            print("Second Singleton Class Object, not starting singleThread")
            return None

        # INITIALIZE FIRST CLASS INSTANCE

        # START THE THREAD
        # threading target must be an instance
        print("Singleton: worker thread execPerSec=10")
        Singleton.tSleep=1.0/execPerSec    # compute needed sleep time
        Singleton.execPerSec=execPerSec
        Singleton.singleThreadHandle = threading.Thread( target=self.threadWorker,
                                                       args=(Singleton.tSleep,))
        Singleton.singleThreadHandle.start()
        if (self.debugLevel >0):  print("Singleton worker thread told to start",datetime.datetime.now())
        time.sleep(0.01)   # give time for pollThread to start

    #end __init__()



    # Singleton THREAD WORKER
    def threadWorker(self, tSleep=0.1):
        print("Singleton: threadWorker started with %f at %s" % (tSleep,datetime.datetime.now()))
        t = threading.currentThread()   # get handle to self  (threadWorker thread)
        while getattr(t, "do_run", True):   # check the do_run thread attribute
            # Do the thread work here
            self.execCounter +=1
            Singleton.execCounter +=1
            if (self.debugLevel > 1):  print("threadWorker: executed ",self.execCounter)
            time.sleep(tSleep)
        if (self.debugLevel >0): print("do_run went false.  Stopping threadWorker thread at %s" % datetime.datetime.now())


    def cancel(self):
        print("Singleton.cancel() called")
        self.singleThreadHandle.do_run = False
        print("Waiting for Singleton.threadWorker to quit")
        self.singleThreadHandle.join()




# MAIN TEST

def main():
    singleton=Singleton(execPerSec=2)   # create instance and worker thread
    singleton2=Singleton(execPerSec=4)  # create second instance w/o worker thread

    try:
        while True:
            print("Main: singleton.execCounter: {}".format(singleton.execCounter))
            print("Main: singleton2.execCounter: {}".format(singleton2.execCounter))
            print("Main: sleeping for 5 seconds")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nCntl-C Detected, calling singleton.cancel()")
        singleton.cancel()
        singleton2.cancel()
    except SystemExit:
        print("\nSingleton Class Test: Bye Bye")
        singleton.cancel()
        singleton2.cancel()
    except:
        print("Main: Exeception Raised")
        singleton.cancel()
        singleton2.cancel()
        traceback.print_exc()





if __name__ == "__main__":
    main()


