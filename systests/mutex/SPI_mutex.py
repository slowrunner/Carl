
# Modeled after RFR_Tools/miscellaneous/I2C_Mutex.py
# https://www.dexterindustries.com
#
# Copyright (c) 2020 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md

import fcntl
import time
import os

class Mutex(object):

    DexterLockI2C_handle = None

    def __init__(self, debug = False):
        self.mutex_debug = debug
        self.DexterLockI2C_handle_filename = '/run/lock/DexterLockI2C'

        # putting the following file in /run/lock so any user can have access
        # putting it directly in /run requires sudo priviledges
        self.DexterOverallMutex_filename = '/run/lock/DexterOS_overall_mutex'
        
        try:
            open(self.DexterLockI2C_handle_filename, 'w')
            if os.path.isfile(self.DexterLockI2C_handle_filename):
                os.chmod(self.DexterLockI2C_handle_filename, 0o777)
        except Exception as e:
            pass

    def acquire(self):
        if self.mutex_debug:
            print("I2C mutex acquire")

        acquired = False
        while not acquired:
            try:
                self.DexterLockI2C_handle = open(self.DexterLockI2C_handle_filename, 'w')
                # lock
                fcntl.lockf(self.DexterLockI2C_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired = True
            except IOError: # already locked by a different process
                time.sleep(0.001)
            except Exception as e:
                print(e)
        if self.mutex_debug:
            print("I2C mutex acquired {}".format(time.time()))


    def release(self):
        if self.mutex_debug:
            print("I2C mutex release: {}".format(time.time()))
        if self.DexterLockI2C_handle is not None and self.DexterLockI2C_handle is not True:
            self.DexterLockI2C_handle.close()
            self.DexterLockI2C_handle = None
            time.sleep(0.001)

    def enableDebug(self):
        self.mutex_debug = True

    def disableDebug(self):
        self.mutex_debug = False

    def set_overall_mutex(self):
        try:
            self.overall_mutex_handle = open(self.DexterOverallMutex_filename, 'w')
            # debating whether we want to open up control of this file to any other process, 
            # or if control should be limited to the process that started it.
            # For now, open it up and let's see.
            os.chmod(self.DexterOverallMutex_filename, 0o777)
        except Exception as e:
            print(e)
            pass

    def release_overall_mutex(self):
        try:
            self.overall_mutex_handle.close()
            os.remove(self.DexterOverallMutex_filename)
        except:
            pass

    def overall_mutex(self):
        if os.path.isfile(self.DexterOverallMutex_filename):
            return True
        else:
            return False


    def __enter__(self):
        if self.mutex_debug:
            print("I2C mutex enter")
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.mutex_debug:
            print("I2C mutex exit")
        self.release()
