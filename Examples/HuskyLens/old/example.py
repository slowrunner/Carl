# USAGE: python3 example.py

import time
from huskylensPythonLibrary import HuskyLensLibrary  

# setup HuskyLensLibrary object with I2C interface
huskyLens = HuskyLensLibrary("I2C","",address=0x32)

print("Commanding Face Recognition Mode")
huskyLens.command_request_algorithm("ALGORITHM_FACE_RECOGNITION")

# loop getting faces
while True:
    try:
        time.sleep(1)
        data=huskyLens.command_request_blocks()
        x=0
        for i in data:
            x += 1
            print("Face {}: [ctr_x,ctr_y,w,h,id] {}".format(x,i))
    except KeyboardInterrupt:
        print("\n")
        break
    except Exception as e:
        print("Exception:",str(e))
        break
