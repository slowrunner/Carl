# file: myimutils.py
#

import cv2


def display(windowname, image, scale_percent=30):
    #print('Original Dimensinos : ', image.shape)

    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    imagesmall = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    #print('Resized Dimensions : ',imagesmall.shape)
    cv2.imshow(windowname, imagesmall)

