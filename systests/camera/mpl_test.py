#!/usr/bin/env python3

# file: mpl_test.py

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from time import sleep

print("matplotlib.get_backend():", plt.get_backend())
print("reading images/motion_capture.jpg")
img = mpimg.imread('images/motion_capture.jpg')
print("image.shape:", img.shape)

imgplot = plt.imshow(img)
plt.show()   # or pause(1)
sleep(1)

