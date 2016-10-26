import numpy as np
import matplotlib.pyplot as plt

print('Hello World')

def circumference(r):
    
	c = 2*np.pi*r
	return c

def area(r):
    pi = 3.14
    a = pi*r**2
    return a

print('circuference:', circumference(6))
print('area:', area(6))

def circle_area(r):
	return np.pi*r**2
def plotcircle(r):
    theta = np.linspace(0,2*pi,200)
    x = np.sin(theta)
    y = np.cos(theta)
    plt.plot(x,y)
    plt.show()

print(circumference(6))

print('I hate Norbert and James')
