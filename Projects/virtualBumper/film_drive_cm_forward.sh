#!/bin/bash

echo Start Filming Drive CM Forward Test
sleep 3

espeak-ng -s150 -ven+f5 -a125 "Drive CM Bump Tests"
sleep 1

espeak-ng -s150 -ven+f5 -a125 "No Bump"
echo NO BUMP
./drive_cm_test.py

echo Test Continues in 3 seconds
sleep 3s

espeak-ng -s150 -ven+f5 -a125 "Bump after ramp up"
echo BUMP AFTER RAMP UP
./drive_cm_test.py

echo Test Continues in 3 seconds
sleep 3s

espeak-ng -s150 -ven+f5 -a125 "Bump at start up"
echo BUMP AT START UP
./drive_cm_test.py

echo Stop Filming

