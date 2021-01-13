#!/bin/bash

echo "Moving locals to _plib.py files"
mv easygopigo3.py easygopigo3_plib.py
mv gopigo3.py gopigo3_plib.py
echo "Releasing easygopigo3_plib.py to Carl/plib/easygopigo3.py"
cp easygopigo3_plib.py ~/Carl/plib/easygopigo3.py
echo "Releasing gopigo3_plib.py to Carl/plib/gopigo3.py"
cp gopigo3_plib.py ~/Carl/plib/gopigo3.py
echo "Removing di_easy and di_gopigo versions"
rm di_*
echo "Removing __pycache__"
rm -r __pycache__
echo "Done"

