
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import fitting


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
    
def histogram(image, x, y, radius):
    
    image = grayscale(image)*cut_out(grayscale(image),x,y,radius)
    im = image.ravel()
    img = im[np.nonzero(im)]
    bins = plt.hist(img,100, color='black')
    return bins

def fit_histogram(arr):
    """
    takes input array with gray scale histogram and fits a gaussian.
    returns a value that lies two standard deviations off to brighter values
    """
    p0,fitfunc = fitting.gauss(np.max(arr),np.argmax(arr),10) ## entries are amp,x0,sigma
    res = fitting.do_fit(range(len(arr)),arr,p0,fitfunc)
    cut_off = res['params_dict']['x0']+res['params_dict']['s']*2 # go 2 sigma away from the mean of the gaussian to get cutoff
    #cut_arr = arr[arr>cut_off]
    return cut_off

def calculate_area(arr,cut_off):
    """
    takes array of gray scale values and a cutoff value
    returns the fraction of entries that lie above the chosen cut_off.
    """
    return len(arr[arr>cut_off])/len(arr)
    
    

def find_circle_coords(img):
    """
    takes image returns three arrays
    x_coords, y_coords, radii
    """
    pass



def master_solver(img,xs=None):
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
    
    img = grayscale(img) ## gray scale
    
    if xs!=None:
        xs,ys,rs = find_circle_coords(img) ## find dishes
    
    for x,y,r in zip(xs,ys,rs):
        cut = cut_out(img,x,y,r)
        plt.imshow(cut*img) ### which petri dish are we checking? Need visualization
        h = histogram(img,x,y,r)
        brightness_cut_off = fit_histogram(h)
        area = calculate_area(img,)
        Print('bacterial area is '+str(np.round(area,3)))
    
    
