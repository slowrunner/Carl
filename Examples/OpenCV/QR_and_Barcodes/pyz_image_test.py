#!/usr/bin/env python3

# pyz_image_test.py
# based on https://github.com/ChiHsuChen/pyQRCodeScanner
# orig author: Chi-Hsu Chen 
# purpose: a simple python script for scanning and detecting QRCode in an image by PyZBarcode


import sys
import cv2
import numpy as np
from pyzbar.pyzbar import decode

# image
def showImg(title,img):
    cv2.imshow(title,img)

# bar code
def scanQRCode(img):
    barcodes=decode(img)
    print('{} barcodes found in this image'.format(len(barcodes)))
    index=0

    for barcode in barcodes:
        index=index+1

        # bar code
        decodetext=barcode.data.decode('utf-8')
        codetype=barcode.type
        text='['+codetype+']'+decodetext

        (x,y,width,height)=barcode.rect
        cv2.rectangle(img,(x,y),(x+width,y+height),(0,0,255),3)
        cv2.putText(img,text,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)

        print('#.{} ================= START ================='.format(index))
        print('x,y,w,h={} text={}'.format((x,y,width,height),text))
        print('#.{} ================= END ================='.format(index))


# main program

img=cv2.imread('pyz_image_test.jpg',cv2.IMREAD_COLOR)
scanQRCode(img)
showImg('QRCode detection',img)

cv2.waitKey(0)
cv2.destroyAllWindows()

