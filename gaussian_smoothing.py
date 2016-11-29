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
i = 0
j = 0

plt.imshow(img, interpolation='nearest')
plt.show()

img = ndimage.gaussian_laplace(img, sigma=3.2)
                    
plt.imshow(img, interpolation='nearest')
plt.show()

for x in range(512):
    for y in range(512):
        newImg[x, y] = img[x,y,1]

print(newImg.shape)

#plt.savefig('testplot3.png')

def _image_to_molecule_locations(

    imageIn, 
    #The image in 2d array form
    
    image_num,
    #Image number
    
    xyShape,
    #Shape of calibration stack used to localise particles in image
    
    previousFrame=None,
    #Default = none
    
    unfilteredImage=None,
    #Default = none
    
    unfilteredPreviousFrame=None,
    #Default = none
    
    numSTD=4,
    #Default = 4
    #'numSTD' is the number of standard deviations of brightness a particle must 
    #rise above the image mean to be considered a particle
    
    numSTD_changed=None,
    #Default = none
    
    showResults=False,
    #Default = none
    
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
    
    if numSTD_changed is None:
    
        numSTD_changed = numSTD
        #set numSTD to default value 
    
    if previousFrame is None:
    
        imDiff = scipy.zeros(imageIn.shape)
        #set image difference to be 0
    
    else:
    
        imDiff = imageIn - previousFrame
        #calculate image difference with previous frame
    
    if showResults:
    
        if unfilteredImage is None:
    
            unfilteredImage = scipy.zeros(imageIn.shape)
            #Set unfiltered image to be zeros in shape of image input
    
            unfilteredDiff = scipy.zeros(imageIn.shape)
            #Set unfiltered difference to be zeros in shape of image input
    
        else:
    
            if unfilteredPreviousFrame is None:
    
                unfilteredDiff = scipy.zeros(imageIn.shape)
                #Set unfiltered difference to be zeros in shape of image input
    
            else:
    
                unfilteredDiff = unfilteredImage - unfilteredPreviousFrame
                #Calculate unfiltered difference from image - previous frame

    locs, avg, std, thresh = [], [], [], []
    
    for (im, num) in (
    
        (imageIn, numSTD),
    
        (imDiff, numSTD_changed),
    
        (-imDiff, numSTD_changed)):
    
        avg.append(im.mean()) #Image average over 3 frames
    
        std.append(im.std()) #Image standard deviation over 3 frames
    
        thresh.append(im > (avg[-1] + num*std[-1])) #Brightness threshold
    
        locs.append([])
    
        """Zero the image, except for the bright or changed spots:"""
    
        peaksImage = im * thresh[-1]
    
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
    
    if showResults:
        #Plot results
    
        import pylab
    
        pylab.suptitle('Image %i. numSTD: %.2f, %.2f'%(
            image_num, numSTD, numSTD_changed))
        #show image number, std and std changed
    
        for i in range(2):
    
            if unfilteredPreviousFrame is None and i > 0:
            #no unfiltered previous frame and second iteration
    
                continue
    
            pylab.subplot(2, 2, i+1)
            #create subplots 2x2 and plot first 2 images as unfiltered
    
            pylab.imshow(
        
                     (unfilteredImage, unfilteredDiff)[i],
    
                     interpolation='nearest', cmap=pylab.cm.gray)
            #show unfiltered image / unfiltered diff for 2 images (current and previous)
    
            pylab.colorbar(pad=0,shrink=0.6)
    
            pylab.title(("Unfiltered image", "Differential image")[i])
        
        for i in range(2):
            #second 2 images produced (filtered and filtered differential image)
    
            if previousFrame is None and i > 0:
    
                continue
    
            (normIm, taggedIm) = _spots_and_slices(
    
                (imageIn, imDiff)[i], avg[i], std[i],
    
                thresh[i], locs[i], ([],locs[2])[i])
    
            pylab.subplot(2, 2, i+3)
    
            pylab.imshow(normIm, interpolation='nearest', cmap=pylab.cm.gray)
    
            pylab.colorbar(pad=0, shrink=0.6)
    
            pylab.imshow(taggedIm, interpolation='nearest')
            #taggedIm is simple bright spots image
    
            pylab.xlabel(
    
                    'Filtered' + ('',' differential')[i] +
    
                    ' image.\nAvg:%.1f SD:%.2f num:%i'%(
    
                    avg[i], std[i], len(locs[i])))
            
            pylab.savefig('final.png')
    
    
    brights = locs[0]
    
    births = locs[1]
    
    deaths = locs[2]

    return (brights, births, deaths)
    
def _spots_and_slices(im, av, sd, thresh, locs, darklocs):
    #im = (image in, image diff)
    #av = average
    #sd = standard deviation
    #thresh = threshold
    #locs = locations of bright points
    #darklocs = locations of spots turned into darkness
    
    """Utility function for _image_to_molecule_locations()"""
    
    import scipy
    
    normIm = (im - av) * 1.0 / sd 
    #normalised image

    taggedIm = scipy.zeros((im.shape[0],im.shape[1],3))
    #set tagged image to be array of zeros of shape size with each having 3 numbers associated
    
    taggedIm[:,:,0] = (im - im.min()) * 1.0 /(im.max() - im.min())
    #first number of each point is (point - minimum) / (max - minimum)

    taggedIm[:,:,1] = taggedIm[:,:,0] * (1 - thresh)
    #second number of each point is first number multiplied by 1 - threshold
    
    taggedIm[:,:,2] = taggedIm[:,:,0] * (1 - thresh)
    #third number of each point is first number multiplied by 1 - threshold
    
    for (molX, molY) in locs:
        #for each location tag numbers as 1
        
        taggedIm[molX.start, molY, 1:2] = 1

        taggedIm[molX.stop, molY, 1:2] = 1

        taggedIm[molX, molY.start, 1:2] = 1

        taggedIm[molX, molY.stop, 1:2] = 1

    for (molX, molY) in darklocs:
        #for each dark location tag numbers as 0
        
        taggedIm[molX.start, molY, 1:2] = 0

        taggedIm[molX.stop, molY, 1:2] = 0

        taggedIm[molX, molY.start, 1:2] = 0

        taggedIm[molX, molY.stop, 1:2] = 0

    return (normIm, taggedIm)
    #returns normal image and simple tagged image in terms of 1's and 0's
    
(brights, births, deaths) = _image_to_molecule_locations(imageIn=newImg, image_num=1, xyShape=[20,20], showResults=True)
#print("brights" + str(brights))
#print(births)
#print(deaths)

maxPixels = []
im = im.convert('LA')

minMax = im.getextrema()
maxPixels.append(minMax[1])
im[(minMax[1][0]-10):(minMax[1][0]+10), (minMax[1][1]-10):(minMax[1][1]+10)] = (0,0,0)
    
#trying to find each maxima then set pixels around to black and repeat (not yet working)
print(maxPixels)


#candList = []
#i=0
#for cands in brights:  
#    candList.append({
#                    'x_slice': cands[0],
#                    'y_slice': cands[1]})
#    img.putpixel((cands[1].start + 10, cands[0].start + 10), new_colour)
#    i += 1
#print i
#img.show()
#print(candList)
#