OpenCV License Plate Recognition In Python

From https://github.com/MicrocontrollersAndMore/OpenCV_3_License_Plate_Recognition_Python
by Chris Dahms MicrocontrollersAndMore

This video explains code and processing well:  https://www.youtube.com/watch?v=fJcl6Gw1D8k

I added to Main.py
         [-f "filepath"]  defaults to "LicPlateImages/1.png"
         [-a , --all ]    show all plates - defaults to False
        Changed original image display to scaled down to 30%

I added [-2:] to the end of findContours() in 
    DetectPlates.py line 138  
    DetectChars.py line 239
to correct ValueError: too many values to unpack
    based on https://stackoverflow.com/a/56142875/2367230)
    Suggestion RETR_CCOMP to fix in issues did not work for Python3

RESULTS:

Pretty good on license plates, but not acceptable on Carl's Docking Station Sign
