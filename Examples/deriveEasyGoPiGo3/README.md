# DERIVING FROM EasyGoPiGo3() class

A while back I tried deriving from the EasyGoPiGo3 class and ran into some problem  
where something DexterIndustries wrote actually checked that the base class was GoPiGo3  
and failed because the base class of the passed object was EasyGoPiGo3 class object.  


This is a very simple case of deriving a My_EasyGoPiGo3 class from the EasyGoPiGo3 class.
It works for this simple case.

```
$ python3 use_my_easygopigo3.py 
speed from base EasyGoPiGo3() class: 300
speed from My_EasyGoPiGo3() class: 200
megpg.volt(): 10.93
CAUTION!  forward() at 200 called
```
