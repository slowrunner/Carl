#!/usr/bin/env python3

# file:  pickleTest.py
#
# Serialize a value to a file, and deserialize it the next run
#

import pickle


try:
    chargeCycles = pickle.load(open('chargeCycles.pkl','rb'))

except:
    chargeCycles = 0


print("chargeCycles:",chargeCycles)

chargeCycles += 1
# strChargeCycles = str(chargeCycles)


pickle.dump( chargeCycles, open( 'chargeCycles.pkl', 'wb'))

print("pickled chargeCycles:",chargeCycles)

