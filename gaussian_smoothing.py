#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 12:43:08 2016

@author: jamesfuller
"""

import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
import numpy
from PIL import Image

im = Image.open('image8.jpg')
img = ndimage.imread('image8.jpg')
newImg = numpy.zeros((512,512))

plt.imshow(img, interpolation='nearest')
plt.show()

img = ndimage.gaussian_laplace(img, sigma=3.2)
                    
plt.imshow(img, interpolation='nearest')
plt.show()

for x in range(512):
    for y in range(512):
        newImg[x, y] = img[x,y,1]

#plt.savefig('testplot3.png')

def _image_to_molecule_locations(

    imageIn, 
    #The image in 2d array form
    
    xyShape,
    #Shape of calibration stack used to localise particles in image
    
    numSTD=4,
    #Default = 4
    #'numSTD' is the number of standard deviations of brightness a particle must 
    #rise above the image mean to be considered a particle
    ):
    
    """
    
    Given a 2d array 'imageIn', finds the bright (or changed) regions
    
    of the image that we think are single particles.
    
    
    'xyShape' is a 2-tuple giving the XY shape of the calibration
    
    stack used to localize particles in the image. 'numSTD' is the
    
    number of standard deviations of brightness a particle must rise
    
    above the image mean to be considered a particle. 'showSteps'
    
    displays some of the particle selection process, and can be useful
    
    for debugging and choosing other parameters.
    
    
    """
    
    import scipy
    
    
    """Groundwork:"""
    
    calibrationShape = scipy.asarray(xyShape)
    #Set array of calibration shape as defined above
    #user defined as size of shape round molecule
    
    imageIn = scipy.asarray(imageIn)
    #Set image in as an array

    locs, avg, std, thresh = [], [], [], []
        
    avg.append(imageIn.mean()) #Image average over 3 frames
    
    std.append(imageIn.std()) #Image standard deviation over 3 frames
    
    thresh.append(imageIn > (avg[-1] + numSTD*std[-1])) #Brightness threshold
    
    locs.append([])

    """Zero the image, except for the bright or changed spots:"""

    peaksImage = imageIn * thresh[-1]

    """Chop out the bright spots one at a time:"""

    while peaksImage.max() > 0:
        #Rest of image is zeroed so this will only be bright spots

        peakLocation = scipy.unravel_index(

            peaksImage.argmax(),

            peaksImage.shape)
        #get location of peak found

        """The lower left corner of the chop region:"""

        LLcorner = scipy.asarray(peakLocation - calibrationShape//2) 
        #// = integer division
        appendMolecule = True

        """Don't include molecules that touch the image edge:"""

        if (LLcorner <= 0).any():

            appendMolecule = False

            LLcorner = LLcorner * (LLcorner >= 0)
        #Reset lower left corner if less than 0

        if ((LLcorner + calibrationShape) >= imageIn.shape).any():

            appendMolecule = False
        #if right corner greater than image then ignore molecule
            
        molX = slice(LLcorner[0],(LLcorner[0] + calibrationShape[0]))
        #set x-distance for molecule

        molY = slice(LLcorner[1],(LLcorner[1] + calibrationShape[1]))
        #set y-distance for molecule

        if appendMolecule:

            locs[-1].append((molX, molY))
            #set values into locations array                
            
        """Zero out the chopped region:"""

        peaksImage[molX, molY] = 0
        #zero bright spot to continue on with process

    brights = locs[0]

    return (brights)
    
def show_locations(brights):
    
    maxPixels = [] #empty array to append max locations to
    
    for loc in brights: #for each bright spot
        im = Image.open('image8.jpg')
        im = im.convert('L')
        im = im.crop(((loc[1].start), (loc[0].start), (loc[1].stop), (loc[0].stop)))
        #open image, convert to greyscale and crop to location of bright spot
        minima, maxima = im.getextrema()
        #get value of maximum pixel
        
        for width in range(im.size[0]):
            for height in range(im.size[1]):
                if im.getpixel((width, height)) == maxima:
                    maxPixels.append(((width + loc[1].start), (height + loc[0].start)))
        #when the pixel in the image matches values with max pixel value
        #append it to array in terms of global picture
        
    finalImg = Image.new('RGBA', (512,512), "black") 
    new_colour = (255,0,0,1) #red 
    #create new image to plot on to
    
    for each in maxPixels:
        finalImg.putpixel(each,new_colour) #Changes Pixel Colour to red
    #plot each point in user defined colour
    
    finalImg.show() #show image
    return
    
brights = _image_to_molecule_locations(imageIn=newImg, xyShape=[20,20])

show_locations(brights)