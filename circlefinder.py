import cv2
import matplotlib
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageFilter, Image


def find_circle_coords(imagefile, radmin=80, radmax=110, houghaccumulator=0.6, searchrad=190):
	''' Pass a raw image, and it will return a list of the identified circles
	for further processing.

	image - image file (tested to work with jpg)
	radmin - minimum circle radius to accept
	radmax - maximumc circles radius to accept
	houghaccumulator - value used in the Hough gradient estimation function to identify circles
		a higher value gives more aggressive circle finding


	'''

	image = cv2.imread(imagefile)
	# converting to grayscale
	output = image.copy()
	gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

	# identifying circles
	rawcircles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, houghaccumulator, searchrad)[0] #removing dimens.

	# applying filter function to found circles
	circles = radfilter(rawcircles, radmin, radmax)

	# returning filter circle array
	return circles


def radfilter(rawcircles, radmin, radmax):
    '''Filter function to take an array of circles and filter out circles which are larger or smaller than
    two given radii'''
    
    newcircles = rawcircles[(rawcircles[:,2]>radmin)&(rawcircles[:,2]<radmax)]
    return newcircles

def plot_circle_coords(image, circles):
	''' Pass an array of identified circles, and the image they were found in,
	and produce an overlay that shows the circle positions.'''
	# ensure at least some circles were found
	if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers

    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles.astype("int"):
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    # show the output image
    cv2.imshow("output", np.hstack([image, output]))
    cv2.waitKey(10000)
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    cv2.waitKey(1)

