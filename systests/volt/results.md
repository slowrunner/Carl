# with sleep(0.001) after the ds.read_mm() before the second volt() call:
  
```
pi@Carl : ~/Carl/systests/volt $ ./volt_test.py
loop:100
RESULTS
Sleep after ds.read_mm() before 2nd reading:0.001 Sleep at end of loop:1
First Readings - mean:9.475 max:9.500 min:9.440 std:0.011
Second Readings - mean:9.408 max:9.466 min:9.354 std:0.023
``` **Difference - mean:0.067** ``` max:0.120 min:-0.009 std:0.024
time 1st to 2nd - mean:0.176 max:0.354 min:0.113 std:0.040
time 2nd to 1st - mean:1.002 max:1.002 min:1.002 std:0.000
`` `**times1stGreater: 99** ```
times2ndGreater: 1

pi@Carl : ~/Carl/systests/volt $ ./volt_test.py
loop:100
RESULTS
Sleep after ds.read_mm() before 2nd reading:0.001 Sleep at end of loop:1
First Readings - mean:9.465 max:9.491 min:9.389 std:0.014
Second Readings - mean:9.401 max:9.466 min:9.320 std:0.025
<b>Difference - mean:0.064</b> max:0.120 min:-0.017 std:0.028
time 1st to 2nd - mean:0.166 max:0.318 min:0.119 std:0.035
time 2nd to 1st - mean:1.002 max:1.002 min:1.002 std:0.000
``` **times1stGreater: 96** ```
times2ndGreater: 2
```
    
# With sleep(1) after read_mm(), before second volt() call =================
```
pi@Carl : ~/Carl/systests/volt $ ./volt_test.py
loop:100
RESULTS
Sleep after ds.read_mm() before 2nd reading:1 Sleep at end of loop:1
First Readings - mean:9.431 max:9.457 min:9.371 std:0.013
Second Readings - mean:9.429 max:9.457 min:9.363 std:0.016
``` **Difference - mean:0.002** ``` max:0.068 min:-0.060 std:0.020
time 1st to 2nd - mean:1.171 max:1.319 min:1.120 std:0.042
time 2nd to 1st - mean:1.002 max:1.002 min:1.002 std:0.000
times1stGreater: 46
times2ndGreater: 34

pi@Carl : ~/Carl/systests/volt $ ./volt_test.py
loop:100
RESULTS
Sleep after ds.read_mm() before 2nd reading:1 Sleep at end of loop:1
First Readings - mean:9.410 max:9.431 min:9.346 std:0.014
Second Readings - mean:9.411 max:9.440 min:9.303 std:0.017
``` **Difference - mean:-0.001** ``` max:0.111 min:-0.068 std:0.023
time 1st to 2nd - mean:1.160 max:1.317 min:1.111 std:0.029
time 2nd to 1st - mean:1.002 max:1.002 min:1.001 std:0.000
times1stGreater: 42
times2ndGreater: 46
```
  
  
#  No dist reading, only sleep(0.001) between first and second volt() calls
(A2D has 7mv precision so this result might not be significant)
```
loop:100
RESULTS
No readDist: Sleep before 2nd reading:0.001 Sleep at end of loop:1
First Readings - mean:9.373 max:9.397 min:9.329 std:0.014
Second Readings - mean:9.367 max:9.397 min:9.311 std:0.017
``` **Difference - mean:0.007** ``` max:0.043 min:-0.009 std:0.012
time 1st to 2nd - mean:0.002 max:0.002 min:0.002 std:0.000
time 2nd to 1st - mean:1.002 max:1.002 min:1.002 std:0.000
times1stGreater: 31
times2ndGreater: 2

loop:100
RESULTS
No readDist: Sleep before 2nd reading:0.001 Sleep at end of loop:1
First Readings - mean:9.366 max:9.389 min:9.337 std:0.010
Second Readings - mean:9.361 max:9.389 min:9.311 std:0.013
Difference - mean:0.005 max:0.060 min:0.000 std:0.011
time 1st to 2nd - mean:0.002 max:0.002 min:0.001 std:0.000
time 2nd to 1st - mean:1.002 max:1.003 min:1.002 std:0.000
times1stGreater: 17
times2ndGreater: 0
pi@Carl:~/Carl/systests/volt $ nano volt_test.py
```
  
  
#  no distance sensor read, but with the ave time a reading would take 0.166s
```
  
loop:100
RESULTS
No readDist: Sleep before 2nd reading:0.166 Sleep at end of loop:1
First Readings - mean:9.357 max:9.380 min:9.329 std:0.011
Second Readings - mean:9.357 max:9.380 min:9.311 std:0.012
``` **Difference - mean:-0.000** ``` max:0.035 min:-0.026 std:0.016
time 1st to 2nd - mean:0.167 max:0.167 min:0.167 std:0.000
time 2nd to 1st - mean:1.002 max:1.002 min:1.001 std:0.000
times1stGreater: 43
times2ndGreater: 40

pi@Carl:~/Carl/systests/volt $ ./volt_test.py
loop:100
RESULTS
No readDist: Sleep before 2nd reading:0.166 Sleep at end of loop:1
First Readings - mean:9.347 max:9.371 min:9.311 std:0.011
Second Readings - mean:9.347 max:9.363 min:9.320 std:0.011
Difference - mean:-0.000 max:0.026 min:-0.034 std:0.016
time 1st to 2nd - mean:0.167 max:0.167 min:0.167 std:0.000
time 2nd to 1st - mean:1.002 max:1.002 min:1.002 std:0.000
times1stGreater: 39
times2ndGreater: 41
```
