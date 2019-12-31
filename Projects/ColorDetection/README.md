# GoPiGo Color Detection
GoPiGo can react to colors as seen via the Pi Camera

This program has two modes:  
1. Learning Mode:  will learn user-named colors (and save <color>.jpg)	
```
./colors.py LEARN
```

2. Identify Mode:  will print and speak color it sees
```
./colors.py
```


For expanded color naming, use an underscore between words: e.g. light_green, dark_blue

The colors are stored in a file named knowncolors.csv  
(A color line can be manually removed to enable relearning that color.)

Tuning:  
- Editing camera setting statements allows for incandescent lighting  
  as well as lower light levels that might be seen in a home setting.  
  Comment them out for bright, florescent lit settings.
- First try with only primary and secondary colors: red, orange, yellow, green, blue, purple/violet
- Gray, Black, and White are particularly challenging for this program

This program was originally created by CleoQc of Dexter Industries.

Modifications made:
- Tolerant of non-existent or empty knowncolors.csv
- Control-C aborts program anywhere without error tracebacks
- Identification loop sleep added to make experience less hectic sounding
- <color>.jpg saved for each learned color to give insight into learned colors
- changed to use espeak-ng (the supported version of espeak)
