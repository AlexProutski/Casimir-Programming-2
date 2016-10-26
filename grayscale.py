
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

image = mpimg.imread('img/results_L3.jpg')
#plt.imshow(image)

def grayscale(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray


def cut_out(img,x,y,r):
    """
    takes x,y coordinates in terms of pixels and a radius in pixels. 
    Cuts a boolean array that acts as cutout on the actual image.
    """
    [lenx,leny] = img.shape
    xcoords = np.outer(np.array(range(lenx)),np.ones(leny))
    ycoords = np.outer(np.ones(lenx),np.array(range(leny)))
    distancetoXY = np.sqrt((xcoords-x)**2 + (ycoords-y)**2)
    return distancetoXY < r
    




