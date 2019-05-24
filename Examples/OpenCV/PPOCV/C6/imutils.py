# ##########
#
# file: imutils.py
#
# DOCUMENTATION:
#    PPOCV C6 local module for study
#

import numpy as np
import cv2

def translate(image, x, y):
    M = np.float32([[1, 0, x], [0, 1, y]])
    shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    return shifted


def rotate(image, angle, center = None, scale = 1.0):
    (h, w) = image.shape[:2]

    if center is None:
        center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated


def resize(image, width = None, height = None, interp = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)

    # Alan change from else:
    elif height is None:
        r = width / float(w)
        dim = (width, int(h * r))

    # Alan added
    else:
        dim = (width, height)

    resized = cv2.resize(image, dim, interpolation = interp)
    return resized

