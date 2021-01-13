#!/bin/bash

echo "Checking local easygopigo3.py against backup easygopigo3_plib.py.bak"
diff easygopigo3.py easygopigo3_plib.py.bak
echo "Same if nothing listed"

echo "Checking local gopigo3.py against backup gopigo3_plib.py.bak"
diff gopigo3.py gopigo3_plib.py
echo "Same if nothing listed"
