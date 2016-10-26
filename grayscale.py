
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
    
#Plot Histogram of the entire image
gh = gray.ravel()
ghn = gh[np.nonzero(gh)]

plt.figure(2)
bins = plt.hist(gh,1000)

#Plot Histogram of cut-out and calculate the area
plt.figure(1)
r = 90
plt.imshow(gray*gs.cut_out(gray,400,420,r), cmap = 'gray')

image_2 = gray*gs.cut_out(gray,410,410,r)
im = image_2.ravel()
img = im[np.nonzero(im)]
remove = img>125
img[remove]

frac = len(img[remove])/len(img)
area = frac*np.pi*r**2

print(area)

plt.figure(2)
bins_2 = plt.hist(img,100, color='black')


