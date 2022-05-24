#!/usr/bin/env python3

import healthCheck

if healthCheck.juicerRunning():
    print("juicer is running")
else:
    print("juicer not running")

