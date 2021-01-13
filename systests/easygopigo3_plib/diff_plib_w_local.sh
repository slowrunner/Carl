#!/bin/bash

echo "Checking local easygopigo3.py against ~/Carl/plib/easygopigo3.py"
diff easygopigo3.py ~/Carl/plib/easygopigo3.py
echo "Same if nothing listed"

echo "Checking local gopigo3.py against ~/Carl/plib/gopigo3.py"
diff easygopigo3.py ~/Carl/plib/easygopigo3.py
echo "Same if nothing listed"
