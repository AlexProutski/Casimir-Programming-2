import numpy as np

def circumference(r):
    
	c = 2*np.pi*r
	return c

def circle_area(r):
	return np.pi*r**2

print(circumference(6))
