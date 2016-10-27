
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from imp import reload
import alexREPO.fitting as fitting
reload(fitting)
#import circlefinder


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
    

def histogram(img,x,y,r):
    #Plot Histogram of cut-out and calculate the area
    image_2 = img*cut_out(img,x,y,r)
    im = image_2.ravel()
    img = im[np.nonzero(im)]
    n,bins,patches = plt.hist(img,100, color='black')
    return n,bins

def fit_histogram(x,n):
    """
    takes input array with gray scale histogram and fits a gaussian.
    returns a value that lies two standard deviations off to brighter values
    """
    #print('give the following parameters')
    #print(np.amax(n),x[np.argmax(n)])
    p0,fitfunc = fitting.gauss(np.max(n),x[np.argmax(n)]+20,10) ## entries are amp,x0,sigma
    res = fitting.do_fit(range(len(n)),n,p0,fitfunc)
    cut_off = res['params_dict']['x0']+res['params_dict']['s']*2 # go 2 sigma away from the mean of the gaussian to get cutoff
    plt.plot(np.array(range(250)),res['fitfunc'](np.array(range(250))),'r-')
    plt.show()
    print('cut off found at '+str(np.round(cut_off,3)) )
    return cut_off

def calculate_area(img,cut_off):
    """
    takes array of gray scale values, their respective and a cutoff value
    returns the fraction of entries that lie above the chosen cut_off.
    """
    return len(img[img>cut_off])/len(img)
    
    

def find_circle_coords(img):
    """
    takes image returns three arrays
    x_coords, y_coords, radii
    """
    pass



def master_solver(filename,xs=None,ys = None, rs = None):
    """
    input: takes image
    converts to gray
    finds dishes
    cuts out dishes
    evaluates color histogram
    fits gaussian to find cut-off of the background
    calculates area per circle
    prints results (how much area is occupied by bacteria?)
    output: None
    """
    img  = mpimg.imread(filename)
    gray_img = grayscale(img) ## gray scale
    
    #if xs!=None:
     #   xs,ys,rs = circlefinder.find_circle_coords(filename) ## find dishes
    
    img = gray_img
    for x,y,r in zip(xs,ys,rs):
        cut = cut_out(img,x,y,r)
        fig = plt.figure()
        ax = plt.subplot()
        plt.imshow(cut*img) ### which petri dish are we checking? Need visualization
        plt.show()
        [n,bins] = histogram(img,x,y,r)
        brightness_cut_off = fit_histogram(bins,n)
        area = calculate_area(img,brightness_cut_off)
        print('bacterial area is '+str(np.round(area,3)))
    
    
