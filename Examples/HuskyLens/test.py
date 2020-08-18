#!/usr/bin/env python3

import time
import huskylensPythonLibrary

test = huskylensPythonLibrary.HuskyLensLibrary("I2C","",address=0x32)

try:
    print("First request a knock: {}".format(test.command_request_knock()))
except:
    print("Failed to find HuskyLens at I2C address 0x32")
    exit(1)


# testcmd = "55AA11002C"
# testcksum = test.calculateChecksum(testcmd)
# print("cksum for {} is {}".format(testcmd,testcksum))

def print_menu():
    print("""
        Menu options:
        0) command_request_algorithm() ***format 0 ALG_VAL***
           0 = ALGORITHM_FACE_RECOGNITION
           1 = ALGORITHM_OBJECT_TRACKING
           2 = ALGORITHM_OBJECT_RECOGNITION
           3 = ALGORITHM_LINE_TRACKING
           4 = ALGORITHM_COLOR_RECOGNITION
           5 = ALGORITHM_TAG_RECOGNITION
           6 = ALGORITHM_OBJECT_CLASSIFICATION
        1) command_request()
        2) command_request_blocks() (cntrl-c to stop loop)
        3) command_request_arrows()
        4) command_request_learned()
        5) command_request_blocks_learned()
        6) command_request_arrows_learned()
        7) command_request_by_id() ***format 7 ID_VAL***
        8) command_request_blocks_by_id() ***format 8 ID_VAL***
        9) command_request_arrows_by_id() ***format 9 ID_VAL***
        10) Exit (or Cntrl-C)

        
        47) command_request_learn()   ***format 47 ID_VAL***
        48) command_request_forget()  
        """)

def print_blocks(blks):
    for blk in blks:
        print("center (x,y): ({:>3},{:>3}) width: {:>3} height: {:>3} ID: {:>2}".format(blk[0],blk[1],blk[2],blk[3],blk[4]))
    print("\n")

def print_arrows(arrows):
    for arrows in arrows:
        print("origin (x,y): ({:>3},{:>3}) target (x,y): ({:>3},{:>3}) ID: {:>2}".format(arrow[0],arrow[1],arrow[2],arrow[3],arrow[4]))
    print("\n")

# reverse the ID_by_algorithm dictionary to allow algorithm lookup by ID
algorithmsByValue = {v: k for k, v in huskylensPythonLibrary.algorithmsByteID.items()}

ex=1

try:
    while(ex==1):
        print_menu()
        v=input("Enter cmd number:")
        numEnter=v
        if(numEnter=="10"):
            ex=0
        vsplit = v.split()
        # print("vsplit:",vsplit)
        v=int(vsplit[0])
        if(v==0):
            try:
                f_alg = "{:04x}".format(int(numEnter[2:]))
                f_alg = f_alg[2:]+f_alg[0:2]
                if f_alg in algorithmsByValue:
                    alg_str = algorithmsByValue[f_alg]
                    print("Requesting {} mode".format(alg_str))
                    print(test.command_request_algorithm(alg_str))
                else:
                    print("{} not valid algorithm".format(numEnter[2:]))
            except Exception as e:
                print("Exception {}".format(str(e)))

        elif(v==1):
            print("command_request():")
            req = test.command_request()
            for r in req:
                print(r)

        elif(v==2):
            print("command_request_blocks(): press cntrl-c to stop")
            while True:
                try:
                    blks = test.command_request_blocks()
                    print_blocks(blks)
                    time.sleep(1)
                except KeyboardInterrupt:
                    print(" Exiting command_request_blocks()\n")
                    break
        elif(v==3):
            print("command_request_arrows(): press cntrl-c to stop")
            print(test.command_request_arrows())
            while True:
                try:
                    arrows = test.command_request_arrows()
                    print_arrows(arrows)
                    time.sleep(1)
                except KeyboardInterrupt:
                    print(" Exiting command_request_arrows()\n")
                    break
        elif(v==4):
            print("command_request_learned():")
            lrnd = test.command_request_learned()
            for id in lrnd:
                print(id)
        elif(v==5):
            print("command_request_blocks_learned():")
            blks = test.command_request_blocks_learned()
            print_blocks(blks)
        elif(v==6):
            print("command_request_arrows_learned():")
            arrows = test.command_request_arrows_learned()
            print_arrows(arrows)
        elif(v==7):
            print("command_request_by_id({})".format(int(vsplit[1])))
            ids = test.command_request_by_id(int(numEnter[2:]))
            for id in ids:
                print(id)
        elif(v==8):
            print("command_request_blocks_by_id({})".format(int(vsplit[1])))
            blks = test.command_request_blocks_by_id(int(numEnter[2:]))
            print_blocks(blks)
        elif(v==9):
            print("command_request_arrows_by_id({})".format(int(vsplit[1])))
            arrows = test.command_request_arrows_by_id(int(numEnter[2:]))
            print_arrows(arrows)
        elif(v==47):
            print("requesting learn id={}".format(int(vsplit[1])))
            print(test.command_request_learn(int(numEnter[3:])))
        elif(v==48):
            print("requesting forget")
            print(test.command_request_forget())

except KeyboardInterrupt:
    print("\nCtrl-C Detected: Exiting")
except Exception as e:
    print("Exception: {}".format(str(e)))

