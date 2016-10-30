# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from PIL import Image, ImageDraw
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

    gauss = 256*np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2) # scales Gaussian to 255 colour range

    for i in gauss: # creates list of gaussian values
        for num in i:
            newgauss.append(int(num))

    return newgauss

def Plot_Shapes(num_points, shape): #Input number of random pixels and detect them, 
    # shape = triangle, square or all
    img = Image.new( 'RGBA', (512,512), "black") # create a new black image
    pixels = img.load() # create the pixel map    
    width, height = img.size

    
    
    if shape.upper() in ("TRIANGLE","ALL"):     
        """
        Plot Gaussian distribution at random locations in a triangle
        """
        tri_its = 0
        tri_colour = (255,0,0,1) #red 
        
        x = 250 # positions of inital points
        y = 180
        tri_size = 75
        triangle_coord_list = []
        numpoints_coord_list = []
        for count, checker in enumerate(range(tri_size)): # Create right angle triangle 
            triangle_coord_list.append((x+count,y+count)) #hypotenuse
            
            if checker == len(range(tri_size))-1:
                
                for count2, checker2 in enumerate(range(tri_size)): # horizontal line
                    triangle_coord_list.append((x+count2,y))
                    
                    if checker2 == len(range(tri_size))-1:
                        
                         for count3 in range(tri_size): # vertical line
                             triangle_coord_list.append(((x+len(range(tri_size)),y+count3)))
        
        while tri_its <= num_points: #iterate through number of points and randomly plot them
            randomInt = random.randint(0,len(triangle_coord_list)-1) #find random index in square array
            point = triangle_coord_list[randomInt] #assign coords to random index       
            numpoints_coord_list.append(point)
            img.putpixel(point,tri_colour) #Changes Pixel Colour
            tri_its += 1 #increase count by one
            if tri_its == num_points:#break out statement
                break
                              
        for tri_coord in (numpoints_coord_list): #for each maximum 
            makeGaussian(random.randint(3,9),random.randint(2,4),)  #call function to make individual guassian distributions for each point
            gaussianList = newgauss
            tri_index = 0 # count through gauss list
            if (tri_coord[0]-lowerlimit >= 0) & (tri_coord[0]+upperlimit <= width): #checks to see gaussians lie within pixel map
                if (tri_coord[1]-lowerlimit >= 0) & (tri_coord[1]+upperlimit <= height):
           
                    for hor in range(tri_coord[0]-lowerlimit, tri_coord[0]+upperlimit, 1): # size of distribution in x and y direction
                        for ver in range(tri_coord[1]-lowerlimit, tri_coord[1]+upperlimit, 1):
                            
                                if tri_index < len(gaussianList): # keep index with list values
                                    
                                    tri_gauss_change = float((pixels[hor,ver][0] + gaussianList[tri_index])) # divided by too for average and too avoid over saturation
                                    if tri_gauss_change >= 255:
                                        tri_new_colour = 255
                                    else:
                                        tri_new_colour = tri_gauss_change
                                    
                                    img.putpixel((hor,ver), int(tri_new_colour)) # change colour of pixel

                                    tri_index = tri_index + 1 #next gaussian list value
                else:
                    print("Y coordinate Gaussian values lie outside of image map", tri_coord , lowerlimit, upperlimit)
            else : 
                print("X coordinate Gaussian values lie outside of image map", tri_coord , lowerlimit, upperlimit)
        print('There are' ,num_points, 'maximum points on the triangle. At the following locations :-' ,numpoints_coord_list)
                
   
    
    if shape.upper() in ("SQUARE","ALL"):     
            
        """
        plot random gaussian distributions around square
        """
        x = 200 # positions of inital points
        y = 200
        square_size = 100
        square_coord_list = []
        numsquare_coord_list = []
        num_sq_its = 0
        square_colour = (0,255,0,1)
        
        for count_square, checker_square in enumerate(range(square_size)): # Create right angle triangle 
            square_coord_list.append((x+count_square,y))                                    #horizontal lower line
            
            if checker_square == len(range(square_size))-1:                                 #last element check
                
                for count_square2, checker_square2 in enumerate(range(square_size)):        # vertical left line
                    square_coord_list.append((x,y+count_square2))
                    
                    if checker_square2 == len(range(square_size))-1:
                        
                         for count_square3, checker_square3 in enumerate(range(square_size)):   # horizontal upper line                        
                             square_coord_list.append((x+count_square3,y+count_square2))
                             
                             if checker_square3 == len(range(square_size))-1:
                        
                                 for count_square4 in range(square_size):                       # vertical right line
                                     square_coord_list.append(((x+count_square3,y+count_square4)))
                                     
                                     
        while num_sq_its <= num_points: #iterate through number of points and randomly plot them
              randomInt = random.randint(0,len(square_coord_list)-1) #find random index in square array
              square_point = square_coord_list[randomInt] #assign coords to random index
              numsquare_coord_list.append(square_point)
              img.putpixel(square_point,square_colour) #Changes Pixel Colour
              num_sq_its += 1 #increase count by one
              if num_sq_its == num_points:#break out statement
                  break
                    
        for sq_coord in (numsquare_coord_list): #for each maximum 
            makeGaussian(random.randint(3,9),random.randint(2,4),)  #call function to make individual guassian distributions for each point
            gaussianList = newgauss
            sq_index = 0
            for sq_x in range(sq_coord[0]-lowerlimit, sq_coord[0]+upperlimit, 1): # 5 pixels in x and y direction
                for sq_y in range(sq_coord[1]-lowerlimit, sq_coord[1]+upperlimit, 1):
                    if (((sq_x <= width) & sq_y <= height)) & ((sq_x & sq_y) >= 0): # boundary limits
                        if sq_index < len(gaussianList): # keep index with list values
                        
                            sq_gauss_change = float((pixels[sq_x,sq_y][0] + gaussianList[sq_index]))
                            
                            if sq_gauss_change >= 255:
                                sq_new_colour = 255
                            else:
                                sq_new_colour = sq_gauss_change                           
                            img.putpixel((sq_x,sq_y), int(sq_new_colour)) # change colour of pixel
                            
                            sq_index = sq_index + 1 #count through gaussian list
         
        print('There are' ,num_points, 'maximum points on the square. At the following locations :-' ,numsquare_coord_list)
                            
                            
                            
        
        
    img.show()
#    # Create Circle
#    """
#    Credit to John La rooy http://stackoverflow.com/questions/2980366/python-draw-a-circle-with-pil
#    """
#    xc = 300
#    yc = 330
#    r = 50
#    draw = ImageDraw.Draw(img)
#    draw.ellipse((xc-r, yc-r, xc+r, yc+r))
    
          
Plot_Shapes(50, "all")
