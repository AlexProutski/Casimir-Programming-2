import numpy as np
import matplotlib.pyplot as plt

print('Hello World')

def circumference(r):
    
	c = 2*np.pi*r
	return c

<<<<<<< HEAD
def circle_area(r):
	return np.pi*r**2
=======
def plotcircle(r):
    theta = np.linspace(0,2*pi,200)
    x = np.sin(theta)
    y = np.cos(theta)
    plt.plot(x,y)
    plt.show()
>>>>>>> 9eb495e53b5eb1755a02e31d9952a6415a914cb8

print(circumference(6))
