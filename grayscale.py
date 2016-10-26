#%matplotlib inline

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

image = mpimg.imread('img/results_L3.jpg')
#plt.imshow(image)

def grayscale(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

gray = grayscale(image)
plt.imshow(gray, cmap = plt.get_cmap('gray'))
