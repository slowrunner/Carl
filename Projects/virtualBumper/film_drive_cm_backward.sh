#!/bin/bash

echo Start Filming Drive CM Backward Test
sleep 3
espeak-ng -s150 -ven+f5 -a125 "Drive CM Backward Bump Tests"
sleep 2

espeak-ng -s150 -ven+f5 -a125 "No Bump"
echo NO BUMP
./drive_cm_backward_test.py

echo Test Continues in 3 seconds
sleep 3s

espeak-ng -s150 -ven+f5 -a125 "Bump After Ramp Up"
echo BUMP AFTER RAMP UP
./drive_cm_backward_test.py

echo Test Continues in 3 seconds
sleep 3s

espeak-ng -s150 -ven+f5 -a125 "Bump From Start"
echo BUMP AT START UP
./drive_cm_backward_test.py

echo Stop Filming

