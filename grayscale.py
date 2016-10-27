
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from imp import reload
import alexREPO.fitting as fitting
reload(fitting)
import alexREPO.circlefinder as circlefinder

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
    print('give the following parameters')
    print(np.amax(n),x[np.argmax(n)])
    p0,fitfunc = fitting.gauss(np.max(n),x[np.argmax(n)],10) ## entries are amp,x0,sigma
    res = fitting.do_fit(x[:-1],n,p0,fitfunc)
    #plt.plot(np.array(range(250)),fitfunc(np.array(range(250))),'b--') # in case you want to plot your guess
    cut_off = res['params_dict']['x0']+res['params_dict']['s']*3 # go 5 sigma away from the mean of the gaussian to get cutoff
    plt.plot(np.array(range(250)),res['fitfunc'](np.array(range(250))),'r-',zorder=100)
    plt.show()
    print('x0 and s '+ str(res['params_dict']['x0'])+' ' + str(res['params_dict']['s']))
    print('cut off found at '+str(np.round(cut_off,3)) )
    return cut_off

def calculate_area(img,cut_off):
    """
    takes array of gray scale values, their respective and a cutoff value
    returns the fraction of entries that lie above the chosen cut_off.
    """
    return len(img[img>cut_off])/len(img[img>0])
    

def master_solver(filename,xs=None,ys = None, rs = None, radmin=80, radmax=110, houghaccumulator=0.6, searchrad=190, radiusreduction=0):
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
    

    if xs==None:
        circles = circlefinder.find_circle_coords(filename, radmin, radmax, houghaccumulator, searchrad) ## find dishes
        xs = circles[:,1] # Note, different convention for x and y for Norbert and James...
        ys = circles[:,0]
        rs = circles[:,2]

        rs = rs-radiusreduction
    
    img = gray_img
    areas = np.zeros(len(xs))
    for i,x,y,r in zip(range(len(xs)),xs,ys,rs):
        cut = cut_out(img,x,y,r)
        fig = plt.figure()
        ax = plt.subplot()
        plt.imshow(cut*img) ### which petri dish are we checking? Need visualization
        plt.show()
        [n,bins] = histogram(img,x,y,r)
        brightness_cut_off = fit_histogram(bins,n)
        area = calculate_area(cut*img,brightness_cut_off)
        print('bacterial area is '+str(np.round(area,3)))
        areas[i] = np.round(area,3)
        
    ### finally return the initial image and add our text at the right coordiantes (centre of the circles)
    fig = plt.figure()
    ax = plt.subplot()
    plt.imshow(img,cmap='gray')
    for x,y,area in zip(xs,ys,areas):
        
        ax.text(y,x, str(area*100)+' %', style='italic',
                bbox={'facecolor':'red', 'alpha':0.5, 'pad':1})
    plt.show()
    
    
