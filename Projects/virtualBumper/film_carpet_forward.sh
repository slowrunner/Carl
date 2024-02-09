#!/bin/bash

echo Start Filming Forward Carpet Test
sleep 10

espeak-ng -s150 -ven+f5 -a125 "Forward On Carpet Bump Tests"
sleep 3

espeak-ng -s150 -ven+f5 -a125 "No Bump Test"
echo NO BUMP
./forward_test.py

echo Test Continues in 3 seconds
sleep 3s

espeak-ng -s150 -ven+f5 -a125 "Bump after ramp up"
echo BUMP AFTER RAMP UP
./forward_test.py

echo Test Continues in 3 seconds
sleep 3s

espeak-ng -s150 -ven+f5 -a125 "Bump from start up"
echo BUMP AT START UP
./forward_test.py

echo Stop Filming

