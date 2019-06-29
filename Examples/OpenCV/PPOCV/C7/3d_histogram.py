# USAGE
# python 3d_histogram.py --image ../images/beach.png

# import the necessary packages
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image")
ap.add_argument("-s", "--size", required = False,
	help = "Size of largest color bin", default = 5000)
ap.add_argument("-b", "--bins", required = False,
	help = "Number of bins per color channel", default=4)
args = vars(ap.parse_args())

# store our largest bin size and number of bins in convenience
# variables for ease of use
image = cv2.imread(args["image"])
size = float(args["size"])
bins = int(args["bins"])

# compute the color histogram for the input image
hist = cv2.calcHist([image], [0, 1, 2],
	None, [bins, bins, bins], [0, 256, 0, 256, 0, 256])

# show the shape of the hostgram
print("3D histogram shape: %s, with %d values" % (
	hist.shape, hist.flatten().shape[0]))

# initialize our figure
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# find the largest value in our histogram and then compute the ratio
# of our largest size bin to the largest in the histogram
ratio = size / np.max(hist)

# loop over the histogram planes
for (x, plane) in enumerate(hist):
	for (y, row) in enumerate(plane):
		for (z, col) in enumerate(row):
			# ensure that there is a value in the current bin
			if hist[x][y][z] > 0.0:
				# plot the bin
				siz = ratio * hist[x][y][z]
				rgb = (z / (bins - 1), y / (bins - 1), x / (bins - 1))
				ax.scatter(x, y, z, s = siz, facecolors = rgb)

# show the figures 
plt.show()