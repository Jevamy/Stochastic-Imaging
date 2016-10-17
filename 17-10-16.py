# -*- coding: utf-8 -*-
"""
Created on Mon Oct 03 10:55:57 2016

@author: py13jej
"""


from PIL import Image
#from scipy.stats import norm
#import matplotlib.pyplot as plt
#import matplotlib.patches as circle
import numpy as np
#from scipy import asarray as exp
#from scipy.optimize import curve_fit
import random 


def makeGaussian(size, fwhm = 3, center=None):
    """ Make a square gaussian kernel.

    size is the length of a side of the square
    fwhm is full-width-half-maximum, which
    can be thought of as an effective radius.
    """
    newgauss = []
    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]

    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]

    gauss = 256*np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2)

    for i in gauss:
        for num in i:
            newgauss.append(int(num))
    
    return newgauss
makeGaussian(5,3,)


              
def Plot_Max(num_points): #Input number of random pixels and detect them
    img = Image.new( 'RGBA', (512,512), "black") # create a new black image
    pixels = img.load() # create the pixel map    
    width, height = img.size
    
    Coords_of_cntre = []
    new_colour = (255,255,255,1) #white 
    num_its = 0
    gaussianList = makeGaussian(5,3,)

    while num_its <= num_points: #iterate through number of points and randomly plot them
        x = random.randint(1,512)
        y = random.randint(1,512)
        img.putpixel((x,y),new_colour) #Changes Pixel Colour to white
        num_its += 1 #increase count by one
        if num_its == num_points:#break out statement
            break
    
    for i in range(width): #for each pixel
        for j in range(height):
            if pixels[i,j] == (255,255,255,1):   #check if pixel is max point
                Loc_of_point = (i,j) #locate position
                Coords_of_cntre.append(Loc_of_point) #add coordinates to list
                    
    for coord in (Coords_of_cntre): #for each maximum 
        index = 0
        for x in range(coord[0]-2, coord[0]+3, 1): # 5 pixels in x and y direction
            for y in range(coord[1]-2, coord[1]+3, 1):
                if ((x & y) <= 512) & ((x & y) >= 0): # boundary limits
                    if index < len(gaussianList): # keep index with list values

                        img.putpixel((x,y), (gaussianList[index],gaussianList[index],gaussianList[index],1)) # change colour of pixel
                        
                        index = index + 1 #count through gaussian list
            
    print('There are' ,num_points, 'maximum points. At the following locations :-' ,Coords_of_cntre ) 
    
    img.show()          
Plot_Max(5)
 # apply matrix to pixels surrounding centre point to create gaussian distribution
  

""" 
To do list:
- Randomize Gaussian function so different sizes and intensities can appear
- create another Python program to interpret the image created
"""