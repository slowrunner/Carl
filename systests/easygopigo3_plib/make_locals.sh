#!/bin/bash


echo "Making local copy from  easygopigo3_plib.py as easygopigo3.py"
cp easygopigo3_plib.py easygopigo3.py
echo "Making local copy from  gopigo3_plib.py as gopigo3.py"
cp gopigo3_plib.py gopigo3.py

echo "Moving _plib.py files to _plib.py.bak"
mv easygopigo3_plib.py easygopigo3_plib.py.bak
mv gopigo3_plib.py gopigo3_plib.py.bak

echo "Done"

