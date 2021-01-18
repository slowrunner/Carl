#!/bin/bash

echo "diff local with Carl/plib/ versions"
file="my_safe_inertial_measurement_unit.py"
echo "Comparing: "$file
diff $file ~/Carl/plib/$file
file="my_inertial_measurement_unit.py"
echo "Comparing: "$file
diff $file ~/Carl/plib/$file
file="myBNO055.py"
echo "Comparing: "$file
diff $file ~/Carl/plib/$file
file="imulog.py"
echo "Comparing: "$file
diff $file ~/Carl/plib/$file
echo "No Differences If Nothing listed"
