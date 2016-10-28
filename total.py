# -*- coding: utf-8 -*-
"""
Created on Mon Oct 03 10:55:57 2016

@author: py13jej
"""


from PIL import Image
import math
#from scipy.stats import norm
#import matplotlib.pyplot as plt
#import matplotlib.patches as circle
import numpy as np
#from scipy import asarray as exp
#from scipy.optimize import curve_fit
import random
import os

def makeGaussian(size, fwhm, center=None):
    """JEJ changes 24/10/16 
    add flexibility for size of gaussian"""
    gsize = size
    global lowerlimit, upperlimit, newgauss
    lowerlimit = math.floor(gsize/2)
    upperlimit = math.ceil(gsize/2)
   
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
  
def Plot_Max(num_points): #Input number of random pixels and detect them
    img = Image.new( 'RGBA', (512,512), "black") # create a new black image
    pixels = img.load() # create the pixel map    
    width, height = img.size
    
    Coords_of_cntre = []
    new_colour = (255,255,255,1) #white 
    num_its = 0
   

    while num_its <= num_points: #iterate throug h number of points and randomly plot them
        x = random.randint(1,width)
        y = random.randint(1,height)
        if (((x < width) & y < height)) & ((x & y) > 0):
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
        makeGaussian(random.randint(3,9),random.randint(2,4),)  #call function to make individual guassian distributions for each point
        gaussianList = newgauss
        index = 0 # count through gauss list
        if (coord[0]-lowerlimit >= 0) & (coord[0]+upperlimit <= width): #checks to see gaussians lie within pixel map
            if (coord[1]-lowerlimit >= 0) & (coord[1]+upperlimit <= height):
       
                for hor in range(coord[0]-lowerlimit, coord[0]+upperlimit, 1): # size of distribution in x and y direction
                    for ver in range(coord[1]-lowerlimit, coord[1]+upperlimit, 1):
                        #if (((hor <= width) & ver <= height)) & ((hor & ver) >= 0): # boundary limits
                            if index < len(gaussianList): # keep index with list values
                                img.putpixel((hor,ver), (gaussianList[index],gaussianList[index],gaussianList[index],1)) # change colour of pixel
                                index = index + 1 #count through gaussian list
            else:
                print("Gaussian Distribution lies outside of image map")
        else : 
            print("Gaussian Distribution lies outside of image map")
    print('There are' ,num_points, 'maximum points. At the following locations :-' ,Coords_of_cntre ) 
    
    img.show()          
Plot_Max(100)
 # apply matrix to pixels surrounding centre point to create gaussian distribution


 
def Plot_Square(number):
    img = Image.new('RGBA', (512,512), "black") # create a new black image
    pixels = img.load() # create the pixel map    
    width, height = img.size
    
    num_points = random.randint(1,5) #set number of random points wanted
     
    #Create empty arrays for each side of the square
    topArray = []
    rightArray = []
    leftArray = []
    bottomArray = []
    i = 0
    
    #define the points in each side of the square (10px apart around centre of image)
    while (i < 20):
        topArray.append(((156 + (i*10)),156))
        rightArray.append((356,(156 + (i*10))))
        leftArray.append((156, (156 + (i*10))))
        bottomArray.append(((156 + (i*10)),356))
        i += 1
        
    #concatenate all of the sides into one array
    totalArray = np.concatenate((topArray, rightArray, leftArray, bottomArray))

    Coords_of_cntre = []
    new_colour = (255,255,255,1) #white 
    num_its = 0
    gaussianList = makeGaussian(5,3,)
    
    while num_its <= num_points: #iterate through number of points and randomly plot them
        randomInt = random.randint(0,75) #find random index in square array
        point = totalArray[randomInt] #assign coords to random index
        img.putpixel(point,new_colour) #Changes Pixel Colour to white
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
        for x in range(coord[0]-lowerlimit, coord[0]+upperlimit, 1): # 5 pixels in x and y direction
            for y in range(coord[1]-lowerlimit, coord[1]+upperlimit, 1):
                if (((x <= width) & y <= height)) & ((x & y) >= 0): # boundary limits
                    if index < len(gaussianList): # keep index with list values

                        img.putpixel((x,y), (gaussianList[index],gaussianList[index],gaussianList[index],1)) # change colour of pixel
                        
                        index = index + 1 #count through gaussian list
            
    print('There are' ,num_points, 'maximum points. At the following locations :-' ,Coords_of_cntre ) 

    #try to save image in folder defined if it doesn't already exist
    if not os.path.exists(r'folder/' + str(number) + '.jpg'):
        img.save("/home/pi/Desktop/folder/" + str(number) + ".jpg", 'JPEG')
    #if it does exist add 5000 to number to make it new
    else:
        img.save("/home/pi/Desktop/folder/" + str(number + 5000) + ".jpg", 'JPEG')

def Run_Multiple(howMany):
    #create directory named 'folder'
    newpath = r'folder'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    #run square how many times wanted
    for i in range(howMany):
        Plot_Square(i)

Run_Multiple(5)


    

""" 
To do list:
- Randomize Gaussian function so different sizes and intensities can appear
  ^ Different intensities and spreads ^
- Pixels close to each other in one image
- Modify code so that pixels form shape at random
- Overlay images?

- create another Python program to interpret the image created
"""
