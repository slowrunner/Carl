#!/bin/bash
echo "Dexter easygopigo3.py sources version:"
grep "__version__"  ~/Dexter/GoPiGo3/Software/Python/easygopigo3.py

echo "Installed gopigo3 Python egg files"
find /usr/local/lib/python* -name *.egg | grep gopigo3
find /usr/local/lib/python* -name *.egg | grep DI_
find /usr/local/lib/python* -name *.egg | grep Dexter

echo "GoPiGo3 Python3 Software Version"
pip3 freeze | grep gopigo
