# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 14:20:42 2017

@author: py13jej
"""

from PIL import Image
import os.path

filepath = raw_input("Input your filepath:")
#James's filepath: /Users/jamesfuller/Desktop/Project/final/images/

if filepath == '':
    filepath = 'E:\\Stochastic Imaging Project\\testImages\\' 
    #set default location
              
if os.path.exists(filepath):    
    iterationCount = 0
    aggImg = Image.new('RGBA', (1920,1080), "black") 
    #create new image
    
    for imgName in os.listdir(filepath): 
        if not imgName.startswith('.'): # ignore hidden files
            iterationCount += 1
            print("Iteration - " ,iterationCount)
            im = Image.open(filepath+imgName)

            impixels = im.load() #load pixels from input img
            pixels = aggImg.load() #load picels from output img
            width, height= im.size #get input img size
            
            for hor in range(width):
                for ver in range(height):
                    col_change_red = float((impixels[hor,ver][0] + pixels[hor,ver][0]))
                    col_change_green = float((impixels[hor,ver][1] + pixels[hor,ver][1]))
                    col_change_blue = float((impixels[hor,ver][2] + pixels[hor,ver][2]))
                    #for each point get RGB values
                   
                    aggImg.putpixel((hor+600,ver+300), (int(col_change_red),int(col_change_green),int(col_change_blue))) 
                    # updates aggImg each iteration for colours found in previous images
            
    aggImg.save("aggImage.png")
    #save image
else:
    print('ERROR: Filepath does not exist - '+ filepath)
#catch error statement


